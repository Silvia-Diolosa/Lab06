import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analizza vendite", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW 1
        self.anno = ft.Dropdown(label="anno",
                                options=[ft.dropdown.Option(key="None", text="Nessun filtro")],
                                on_change=self._controller.selezionaAnno)# on change sul dropdown, scatta quando l’utente cambia la selezione del menu
                                # quindi quando cambia chiamiamo questa funzione che legge il valore selezionato
                                # solo il valore, su dropdown
                                # Le singole voci della Dropdown non hanno un “cambiamento”: una voce non cambia mai, viene solo scelta o cliccata.
                                # self.anno quindi prende il value che ottiene al momento di on_change
                                # (self.anno ha una label, ha un valore (assegnato con on change), ha delle opzioni (assegnate funzione sotto)
                                # Dropdown (il menu intero) ha lo stato value che cambia quando scegli una voce, e per questo esiste on_change.
                                # Option (la singola voce) non ha uno stato che cambia. Può solo essere cliccata, e per questo ha on_click.

        #questo metodo è chiamato qui, e viene creato ed usato nel controller per popolare la dropdown (le option)
        self._controller.mostraListaAnno()

        self.brand = ft.Dropdown(label="brand",
                                 options=[ft.dropdown.Option(key="None", text="Nessun filtro")],
                                on_change=self._controller.selezionaBrand)
        self._controller.mostraListaBrand()

        self.retailer = ft.Dropdown(label="retailer",
                        options=[ft.dropdown.Option(key="None", text="Nessun filtro", data=None, on_click=self._controller.selezionaRetailer)])
                        # perchè qui usiamo on_click sulla Option (e sopra on_change su dropdown) ??
                        # Con on_change sul menu dropdown si ha accesso solo a e.control.value, cioè alla chiave, e non all’oggetto
                        # siccome qui stiamo usando un oggetto e non un semplice valore
                        # on_change ti dice che la scelta è cambiata,
                        # on_click ti dà quale voce è stata cliccata, con i suoi dati.
                        # on_click è su ogni singola option, quindi quando clicchiamo su quell'option ce la salva
        self._controller.mostraListaRetailer()

        row1 = ft.Row([self.anno, self.brand, self.retailer], alignment=ft.MainAxisAlignment.CENTER)


        #ROW 2
        self.btnTopVendite = ft.ElevatedButton(text="Top vendite",
                                               on_click=self._controller.topVendite)
        self.btnAnalizzaVendite = ft.ElevatedButton(text="Analizza vendite",
                                                    on_click=self._controller.analizzaVendite)

        row2 = ft.Row([self.btnTopVendite, self.btnAnalizzaVendite], alignment=ft.MainAxisAlignment.CENTER)


        self._page.add(row1, row2)

        # List View where the reply is printed
        self.lvOut = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.lvOut)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
