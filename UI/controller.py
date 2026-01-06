import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.categoriaScelta = None
        self.nodoStart = None
        self.nodoEnd = None

    def riempi_ddcategory(self):
        categorie = self._model.getAllCategorie()
        for categoria in categorie:
            self._view._ddcategory.options.append(ft.dropdown.Option(data=categoria,
                                                                     text = categoria.category_name,
                                                                     on_click = self.pickCategoriaScelta))
    def pickCategoriaScelta(self,e):
        self.categoriaScelta = e.control.data
        print(self.categoriaScelta.category_name, self.categoriaScelta.category_id)
        print(type(self.categoriaScelta))

    def handleCreaGrafo(self, e):
        if self.categoriaScelta is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona una categoria prima di creare il grafo"))
            self._view.update_page()
            return

        if self._view._dp1.value == None or self._view._dp2.value == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona una data di inizio e fine prima di creare il grafo"))
            self._view.update_page()
            return

        self._model.creaGrafo(self.categoriaScelta.category_id, self._view._dp1.value, self._view._dp2.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date selezionate"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {self._view._dp1.value}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {self._view._dp2.value}"))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato: "))
        nNodi, nArchi = self._model.getInfoGrafo()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi {nNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi {nArchi}"))

        self._view.update_page()



        self._view.update_page()

    def handleBestProdotti(self, e):
        nodi = self._model.getProdottiPiuVenduti()
        self._view.txt_result.controls.append(ft.Text(f"I 5 prodotti più venduti sono"))
        for nodo in nodi:
            self._view.txt_result.controls.append(ft.Text(f"{nodo[0]} with score {nodo[1]}"))

        self._view.update_page()
        self.riempi_ddProd()

    def riempi_ddProd(self):
        # _ddProdStart _ddProdEnd
        nodi = self._model.getNodiGrafo()
        for nodo in nodi:
            self._view._ddProdStart.options.append(ft.dropdown.Option(data=nodo,
                                                                     text=nodo.product_name,
                                                                     on_click=self.pickNodoStart))
            self._view._ddProdEnd.options.append(ft.dropdown.Option(data=nodo,
                                                                      text=nodo.product_name,
                                                                      on_click=self.pickNodoEnd))

        self._view.update_page()

    def pickNodoStart(self, e):
        self.nodoStart = e.control.data
        print(self.nodoStart)
        print(type(self.nodoStart))

    def pickNodoEnd(self,e):
        self.nodoEnd = e.control.data
        print(self.nodoEnd)
        print(type(self.nodoEnd))

    def handleCercaCammino(self, e):
        if self._view._txtInLun.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire lunghezza del cammino"))
            self._view.update_page()
            return
        try:
            lun = int(self._view._txtInLun.value)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Valore inserito non numerico"))
            self._view.update_page()
            return

        path, score = self._model.migliorCammino(lun, self.nodoStart, self.nodoEnd)
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino migliore:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.txt_result.controls.append(ft.Text(f"Score: {score}"))
        self._view.update_page()


    def setDates(self):
            first, last = self._model.getDateRange()

            self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
            self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
            self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

            self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
            self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
            self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
