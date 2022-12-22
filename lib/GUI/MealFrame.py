from tkinter import *
import _tkinter
from tkinter import ttk
import json
from tkinter.messagebox import showinfo
import datetime
from lib.GUI.ListMealFrame import ListMealFrame


class MealFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.cook_label = Label(self, text="Cuisinier")
        self.cook_label.pack()
        self.selected_cook = StringVar()
        self.selected_meal = StringVar()
        self.selected_price = IntVar(value=3)
        self.groceries_cost = IntVar()
        self.dict_inscription = {}
        self.create_widget()
        self.app = container

    def create_widget(self):
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            ttk.Combobox(self, textvariable=self.selected_cook, values=data["koters_list"], state="readonly").pack()
            Label(self, text="Repas").pack()
            ttk.Combobox(self, textvariable=self.selected_meal, values=("Matin", "Midi", "Soir"),
                         state="readonly").pack()
            Label(self, text="Prix").pack()
            ttk.Entry(self, textvariable=self.selected_price).pack()
            Label(self, text="Inscription des membres : ", font='Calibri 14 underline').pack()
            for v in data["koters_list"]:
                self.dict_inscription[v] = IntVar()
                ttk.Checkbutton(self, text=v, variable=self.dict_inscription[v], offvalue=0, onvalue=1).pack(anchor="w",
                                                                                                             padx=50)
            ttk.Button(self, text="Finaliser le repas", command=self.get_inscription).pack(pady=5)

    def get_inscription(self):
        try:
            if self.selected_cook.get() == '' or self.selected_meal.get() == '' or self.selected_price.get() == "":
                showinfo(title="Attention", message="Veuillez remplir toutes les cases")
                return ""
        except _tkinter.TclError:
            showinfo(title="Attention", message="Veuillez remplir toutes les cases")
            return ""
        copy_dict_inscription = {}
        is_cook_inscription = self.dict_inscription[self.selected_cook.get()].get()
        if self.selected_price.get() <= 0:
            showinfo(title="Attention", message="Le prix du repas doit être un entier positif")
        else:
            self.dict_inscription[self.selected_cook.get()] = 0
            copy_dict_inscription[self.selected_cook.get()] = [is_cook_inscription, 'cook']
            for v, name in zip(self.dict_inscription.values(), self.dict_inscription.keys()):
                if self.selected_cook.get() == name:

                    continue
                elif v.get() == 1:
                    self.dict_inscription[name] = v.get() * self.selected_price.get()
                    self.dict_inscription[self.selected_cook.get()] -= self.selected_price.get()
                    copy_dict_inscription[name] = [v.get(), 'not_cook']
                else:
                    self.dict_inscription[name] = v.get()
                    copy_dict_inscription[name] = [v.get(), 'not_cook']

            with open("koters.json", "r") as json_r:
                data = json.load(json_r)
                inscrits = [name for name in data["koters_list"] if copy_dict_inscription[name][0] == 1]
                with open("koters.json", "w") as json_w:
                    data["list_meal"].append({
                         "id": len(data["list_meal"]),
                         "cook": self.selected_cook.get(),
                         "inscription": inscrits,
                         "date/type": f"{datetime.date.today()} / {self.selected_meal.get()}",
                         "total_price": len(inscrits) * self.selected_price.get(),
                         "grocery_price": 0,
                         "state_count": False
                         })
                    for v in data["koters_balance"]:
                        v["balance"] += self.dict_inscription[v["name"]]
                    json.dump(data, json_w, indent=4)
            self.app.hide_all_frames()
            self.app.create_menu()
            list_meal_frame = ListMealFrame(self.app, dict(copy_dict_inscription))
            list_meal_frame.pack()
