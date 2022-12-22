from tkinter import *
from tkinter import ttk
from lib.GUI.entry_id import EntryId
from lib.GUI.InfoFrame import InfoFrame
import json


class ListMealFrame(ttk.Frame):
    def __init__(self, container, list_inscription):
        super().__init__(container)
        self.inscription = list_inscription
        self.grocery_prices = []
        self.btn_list = []
        self.app = container
        self.create_widgets()

    def calculate(self, id_meal):
        with open("koters.json", "r") as json_r:
            data = json.load(json_r)
            with open("koters.json", "w") as json_w:
                for price in self.grocery_prices:
                    if id_meal == price.id:
                        grocery_price = int(price.get())
                for meal in data["list_meal"]:
                    if meal["id"] == id_meal:
                        meal["grocery_price"] = grocery_price
                        total = meal["total_price"] - meal["grocery_price"]
                        if total > 0:
                            data["common_pot"] += total
                        meal["state_count"] = True
                json.dump(data, json_w, indent=4)
            self.children[str(id_meal)].destroy()
            self.create_widgets()

    def create_widgets(self):
        # headers
        Label(self, text='Inscrits').grid(row=0, column=1, padx=10)
        Label(self, text='Cuisinier').grid(row=0, column=2, padx=10)
        Label(self, text='Date/Type').grid(row=0, column=3, padx=10)
        Label(self, text='Prix Total').grid(row=0, column=4, padx=10)
        Label(self, text='Prix Course').grid(row=0, column=5, padx=10)
        Label(self, text='Calcul').grid(row=0, column=6, padx=10)
        counter_row = 0
        # body
        with open("koters.json", "r") as json_r:
            data = json.load(json_r)
            with open("koters.json", "w") as json_w:
                for x, item in enumerate(data["list_meal"]):
                    if item["state_count"]:
                        Label(self, text="OK").grid(row=counter_row + 1, column=6)
                    else:
                        btn = ttk.Button(self, text="calculer", name=str(item["id"]),
                                         command=lambda: self.calculate(item["id"]))
                        self.btn_list.append(btn)
                        btn.grid(row=counter_row + 1, column=6)
                    for i, v in enumerate(data["koters_balance"]):
                        name = v["name"]
                        Label(self, text=name).grid(row=counter_row + i + 1, column=0)
                        if name in item["inscription"]:
                            Label(self, text="Oui").grid(row=counter_row + i + 1, column=1)
                        else:
                            ttk.Button(self, text="S'inscrire").grid(row=counter_row + i + 1, column=1)
                        if item["cook"] == name:
                            Label(self, text="*").grid(row=counter_row + i + 1, column=2)
                    Label(self, text=item['date/type']).grid(row=counter_row + 1, column=3)
                    Label(self, text=f"{item['total_price']}€").grid(row=counter_row + 1, column=4)
                    en = EntryId(self, id_entry=item["id"])
                    self.grocery_prices.append(en)
                    en.grid(row=counter_row + 1, column=5)
                    Label(self,
                          text="---------------------------------------------------------------------------------------------------------------------------------------").grid(
                        row=counter_row + len(data["koters_balance"]) + 1, columnspan=8)
                    counter_row += len(data["koters_balance"]) + 1
                final_button = ttk.Button(self, text="faire les comptes", command=self.reimburse, padding=10)
                final_button.grid(row=counter_row + len(data["koters_balance"]) + 3, column=5, columnspan=4)
                final_button.grid_configure(padx=25, pady=15)
                json.dump(data, json_w, indent=4)

    def reimburse(self):
        self.app.hide_all_frames()
        self.app.create_menu()
        info_frame = InfoFrame(self.app)
        info_frame.pack()

