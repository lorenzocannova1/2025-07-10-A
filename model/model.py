import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.prodotti = []
        self.idMapProdotti = {}

        self.bestCammino = None
        self.bestScore = 0


    def getDateRange(self):
        return DAO.getDateRange()

    def getAllCategorie(self):
        return DAO.getAllCategorie()

    def creaGrafo(self, idCategoria, da, a):
        self.prodotti = []
        self.prodotti = DAO.getProdottiByCategoria(idCategoria)
        for prodotto in self.prodotti:
            self.idMapProdotti[prodotto.product_id] = prodotto

        self.grafo.clear()
        self.grafo.add_nodes_from(self.prodotti)

        archi = DAO.getArchi(idCategoria, da, a, self.idMapProdotti)
        for arco in archi:
            self.grafo.add_edge(arco[0],arco[1],weight=arco[2])


    def getInfoGrafo(self):
        nNodi = len(self.grafo.nodes)
        nArchi = len(self.grafo.edges)

        return nNodi, nArchi

    def getProdottiPiuVenduti(self):

        res = []

        for nodo in self.grafo.nodes:
            cont = 0
            for e_out in self.grafo.out_edges(nodo, data=True):
                cont += e_out[2]["weight"]
            for e_in in self.grafo.in_edges(nodo, data=True):
                cont -= e_in[2]["weight"]

            res.append((nodo, cont))

        res.sort(key=lambda x: x[1], reverse=True)
        return res[0:5]

    def getNodiGrafo(self):
        return self.grafo.nodes

    def migliorCammino(self, lun, start, end):
        self.bestCammino = None
        self.bestScore = 0

        parziale = [start]
        self.ricorsione(parziale, lun, start, end)
        return self.bestCammino, self.bestScore

    def ricorsione(self, parziale, lun, start, end):
        if len(parziale) == lun:
            if parziale[-1] == end and self.getScore(parziale) > self.bestScore:
                self.bestScore = self.getScore(parziale)
                self.bestCammino = copy.deepcopy(parziale)
            return

        for n in self.grafo.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale, lun, start, end)
                parziale.pop()

    def getScore(self, parziale):
        score = 0
        for i in range(1, len(parziale)):
            score += self.grafo[parziale[i - 1]][parziale[i]]["weight"]
        return score


