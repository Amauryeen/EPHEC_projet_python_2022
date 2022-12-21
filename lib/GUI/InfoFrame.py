from tkinter import *
from tkinter import ttk
import json


class InfoFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.create_widgets()

    def create_widgets(self):
        Label(self, text='Koteur', font="Calibri 14 underline").grid(row=0, column=1, padx=10)
        Label(self, text="Solde", font="Calibri 14 underline").grid(row=0, column=2, padx=10)
        Label(self, text="Pot Commun", font="Calibri 14 underline").grid(row=3, column=3, padx=10)
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            for i, v in enumerate(data["koters_balance"]):
                name = list(v.keys())[0]
                balance = list(v.values())[0]
                if balance < 0:
                    Label(self, text=f"{name}").grid(row=i + 1, column=1)
                    Label(self, text=f"{balance} €", foreground='red').grid(row=i + 1, column=2)
                else:
                    Label(self, text=f"{name}").grid(row=i + 1, column=1)
                    Label(self, text=f"{balance} €", foreground='green').grid(row=i + 1, column=2)
            Label(self, text=f"{data['common_pot']} €").grid(row=4, column=3)
