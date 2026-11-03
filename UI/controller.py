import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._annoSelezionato = None
        self._brandSelezionato = None
        self._retailerSelezionato = None


    def mostraListaAnno(self):
        for anno in self._model.mostraAnni():
            self._view.anno.options.append(ft.dropdown.Option(str(anno))) # qui anno non è un oggetto, ma un semplice numero
        self._view.update_page()


    def selezionaAnno(self, e):
        if e.control.value == "None":
            self._annoSelezionato = None
        else:
            self._annoSelezionato = int(e.control.value) # value che viene salvato con on_change, nel momento in cui cambiamo selezione



    def mostraListaBrand(self):
        for brand in self._model.mostraBrand():
            self._view.brand.options.append(ft.dropdown.Option(brand))
        self._view.update_page()

    def selezionaBrand(self, e):
        if e.control.value == "None":
            self._brandSelezionato = None
        else:
            self._brandSelezionato = e.control.value



    def mostraListaRetailer(self):
        for retailer in self._model.mostraRetailer():
            self._view.retailer.options.append(ft.dropdown.Option(key=str(retailer.Retailer_code),
                                                                  text=retailer.Retailer_name,
                                                                  data=retailer,
                                                                  on_click=self.selezionaRetailer))
                                                                #qui retailer è un oggetto, quindi salvo sia l'oggeto (in data), che il valore che mi serve(in key)
                                                                # che il valore che verrà mostrato (in text)
        self._view.update_page()

    def selezionaRetailer(self, e):
        if e.control.data is None: # qui stiamo salvando l'oggetto intero (in data), quindi non c'è value
            self._retailerSelezionato = None
        else:
            self._retailerSelezionato = e.control.data.Retailer_code



    def topVendite(self, e):
        self._view.lvOut.controls.clear()

        vendite = self._model.topVendite(self._annoSelezionato,
                                         self._brandSelezionato,
                                         self._retailerSelezionato)
        if len(vendite) == 0:
            self._view.lvOut.controls.append(ft.Text("Nessuna vendita trovata"))
        for v in vendite:
            self._view.lvOut.controls.append(ft.Text(v))
        self._view.update_page()

    #sistema
    def analizzaVendite(self, e):
        self._view.lvOut.controls.clear()

        vendite_statistiche = self._model.analizzaVendite(self._annoSelezionato, self._brandSelezionato, self._retailerSelezionato)
        self._view.lvOut.controls.append(ft.Text("Satistiche vendite:"))
        self._view.lvOut.controls.append(ft.Text(f"Giro d'affari: {vendite_statistiche[0]}"))
        self._view.lvOut.controls.append(ft.Text(f"Numero vendite: {vendite_statistiche[1]}"))
        self._view.lvOut.controls.append(ft.Text(f"Numero retailers coinvolti: {vendite_statistiche[2]}"))
        self._view.lvOut.controls.append(ft.Text(f"Numero prodotti coinvolti: {vendite_statistiche[3]}"))
        self._view.update_page()
