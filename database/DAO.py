from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategorie():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProdottiByCategoria(idCategoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.*
                    FROM products p, categories c 
                    WHERE p.category_id = c.category_id AND c.category_id = %s"""

        cursor.execute(query,(idCategoria,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(idCategoria, da, a, idMap):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.product_id as prodotto1, t2.product_id as prodotto2, n1+n2 as peso
                    FROM (SELECT p.product_id, COUNT(p.product_id) as n1
                    FROM products p, categories c, orders o, order_items oi 
                    WHERE p.category_id = c.category_id AND o.order_id = oi.order_id
                    AND oi.product_id = p.product_id AND c.category_id = %s
                    AND o.order_date BETWEEN %s AND %s
                    GROUP BY p.product_id, p.product_name 
                    ORDER BY p.product_id DESC) as t1,
                    (SELECT p.product_id, COUNT(p.product_id) as n2
                    FROM products p, categories c, orders o, order_items oi 
                    WHERE p.category_id = c.category_id AND o.order_id = oi.order_id
                    AND oi.product_id = p.product_id AND c.category_id = %s
                    AND o.order_date BETWEEN %s AND %s
                    GROUP BY p.product_id, p.product_name
                    ORDER BY p.product_id DESC) as t2
                    where t1.n1 >= t2.n2
                    and t1.product_id <> t2.product_id
                    order by peso desc, prodotto1 asc, prodotto2 asc"""

        cursor.execute(query,(idCategoria,da, a, idCategoria,da, a))

        for row in cursor:
            results.append(
                (idMap[row["prodotto1"]], idMap[row["prodotto2"]], row["peso"])
            )

        cursor.close()
        conn.close()
        return results

