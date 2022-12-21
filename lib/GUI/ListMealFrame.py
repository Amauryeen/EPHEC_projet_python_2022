from tkinter import *
from tkinter import ttk
import json


class ListMealFrame(ttk.Frame):
    def __init__(self, container, list_inscription):
        super().__init__(container)
        self.inscription = list_inscription
        print(self.inscription)
        self.create_widgets()

    def create_widgets(self):
        # headers
        Label(self, text='Inscrits').grid(row=0, column=1, padx=10)
        Label(self, text='Cuisinier').grid(row=0, column=2, padx=10)
        Label(self, text='Date/Type').grid(row=0, column=3, padx=10)
        Label(self, text='Prix Total').grid(row=0, column=4, padx=10)
        Label(self, text='Prix Course').grid(row=0, column=5, padx=10)
        Label(self, text='Calcul').grid(row=0, column=6, padx=10)
        ttk.Button(self, text="calculez").grid(row=1, column=6)
        # body
        with open("koters.json", "r") as json_r:
            data = json.load(json_r)
            with open("koters.json", "w") as json_w:
                for i, v in enumerate(data["koters_balance"]):
                    name = v["name"]
                    Label(self, text=name).grid(row=i + 1, column=0)
                    if self.inscription is None:
                        continue
                    elif 'cook' in self.inscription[name]:
                        if self.inscription[name][0] == 1:
                            Label(self, text="Oui").grid(row=i + 1, column=1)
                        else:
                            ttk.Button(self, text="S'inscrire").grid(row=i + 1, column=1)
                    elif self.inscription[name][0] == 1:
                        Label(self, text="Oui").grid(row=i + 1, column=1)
                    elif self.inscription[name][0] == 0:
                        ttk.Button(self, text="S'inscrire").grid(row=i + 1, column=1)

                    if data['list_meal'][0]['Cuisinier'] == name:
                        Label(self, text="*").grid(row=i + 1, column=2)

                    Label(self, text=data['list_meal'][0]['Date/Type']).grid(row=i + 1, column=3)
                    Label(self, text=data["list_meal"][0]["PrixTotal"]).grid(row=i + 1, column=4)
                    Label(self, text=data['list_meal'][0]['PrixCourse']).grid(row=i + 1, column=5)

                json.dump(data, json_w, indent=4)
