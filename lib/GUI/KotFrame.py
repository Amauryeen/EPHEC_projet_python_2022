from tkinter import *
from tkinter import ttk
import json
from lib.GUI.MealFrame import MealFrame


class KotFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.koters_name = StringVar()
        self.koter_to_delete = StringVar()
        self.kot_name = StringVar()
        self.koters_list = []
        self.kot_name_label = Label(self, text="Nom du kot")
        self.kot_name_label.grid(column=0, row=0)
        self.kot_name_entry = ttk.Entry(self, textvariable=self.kot_name)
        self.kot_name_entry.grid(column=0, row=1)
        self.name_label = Label(self, text="Ajouter un membre")
        self.name_label.grid(column=0, row=2)
        self.name_entry = ttk.Entry(self, textvariable=self.koters_name)
        self.name_entry.grid(column=0, row=3)
        self.add_button = ttk.Button(self, text="Ajouter", command=self.add_koter)
        self.add_button.grid(column=3, row=3, padx=5)
        self.koter_to_delete_label = Label(self, text="Supprimer un membre")
        self.koter_to_delete_label.grid(column=0, row=4)
        self.koter_to_delete_entry = ttk.Entry(self, textvariable=self.koter_to_delete)
        self.koter_to_delete_entry.grid(column=0, row=5)
        self.delete_button = ttk.Button(self, text="Supprimer", command=self.delete_koter)
        self.delete_button.grid(column=3, row=5, padx=5)
        self.create_button = ttk.Button(self, text="Créer", command=self.create_kot)
        self.create_button.grid(column=3, row=1, padx=5)
        self.app = container

    def get_data_from_json(self):
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            for v in data["koters_list"]:
                self.koters_list.append(v)

    @staticmethod
    def add_koter_to_json(koter):
        with open("koters.json", "r") as r_json:
            data = json.load(r_json)
        with open("koters.json", "w") as w_json:
            data["koters_list"].append(koter)
            data["koters_balance"].append({koter: 0})
            json.dump(data, w_json, indent=4)

    def create_kot(self):
        with open("koters.json", "r") as r_json:
            data = json.load(r_json)
        with open("koters.json", "w") as w_json:
            data["kot_name"] = self.kot_name.get()
            json.dump(data, w_json, indent=4)
        self.app.hide_all_frames()
        self.app.create_menu()
        meal_frame = MealFrame(self.app)
        meal_frame.pack()

    def add_koter(self):
        self.add_koter_to_json(self.koters_name.get())
        show_koter = Label(self.app, text=self.koters_name.get())
        show_koter.pack()
        self.name_entry.delete(0, END)

    def delete_koter(self):
        self.delete_koter_from_json(self.koter_to_delete.get())
        self.koter_to_delete_entry.delete(0, END)
        app.create_kot_frame()

    @staticmethod
    def delete_koter_from_json(koter):
        with open("koters.json", "r") as r_json:
            data = json.load(r_json)
        with open("koters.json", "w") as w_json:
            try:
                data["koters_list"].remove(koter)
                json.dump(data, w_json, indent=4)
            except ValueError:
                json.dump(data, w_json, indent=4)
