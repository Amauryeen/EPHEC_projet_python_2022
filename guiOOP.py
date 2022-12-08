import _tkinter
from tkinter import *
from tkinter import ttk
from kotcount import *
from tkinter.messagebox import showinfo
import os


class App(Tk):
    def __init__(self):
        super().__init__()
        # configure the window
        self.title("KotCount")
        self.minsize(width=400, height=400)
        self.path_db = "koters.json"
        if os.path.exists(self.path_db):
            self.create_welcome_frame()
        else:
            with open(self.path_db, "w+") as json_file:
                data = {"kot_name": "", "koters_list": [], "koters_balance": [], "common_pot": 0, "list_meal": []}
                json.dump(data, json_file, indent=4)
            self.create_welcome_frame()

    @staticmethod
    def get_kot(self):
        with open("koters.json", 'r') as json_r:
            data = json.load(json_r)
            self.kot = Kot(data["kot_name"])
            for person in data["koters_list"]:
                Person(person)

    def hide_all_frames(self):
        for widget in App.winfo_children(self):
            widget.destroy()
        for widget in KotFrame.winfo_children(self):
            widget.destroy()
        for widget in MealFrame.winfo_children(self):
            widget.destroy()
        for widget in ListMealFrame.winfo_children(self):
            widget.grid_forget()

    def create_menu(self):
        self.menubar = Menu(self)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.kot_menu = Menu(self.menubar, tearoff=0)
        self.meal_menu = Menu(self.menubar, tearoff=0)
        self.list_meal_menu = Menu(self.menubar, tearoff=0)
        self.info_menu = Menu(self.menubar, tearoff=0)
        self.config(menu=self.menubar)

        self.menubar.add_cascade(label="Application", menu=self.file_menu)
        self.file_menu.add_command(label="Accueil", command=self.create_welcome_frame)
        self.file_menu.add_command(label="Quitter", command=self.destroy)

        self.menubar.add_cascade(label="Kot", menu=self.kot_menu)
        self.kot_menu.add_command(label="Modifier", command=self.create_kot_frame)

        self.menubar.add_cascade(label="Repas", menu=self.meal_menu)
        self.meal_menu.add_command(label="Créer", command=self.create_meal_frame)
        self.meal_menu.add_command(label="Voir l'historique", command=self.create_list_meal_frame)

        self.menubar.add_cascade(label="Information", menu=self.info_menu)
        self.info_menu.add_command(label="Ouvrir", command=self.create_info_frame)

    def create_kot_frame(self):
        self.hide_all_frames()
        kot_frame = KotFrame(self)
        kot_frame.pack()
        self.create_menu()
        kot_frame.koters_list = []
        kot_frame.get_data_from_json()
        Label(app, text="Membres du Kot :", font='Calibri 14 underline').pack()
        for v in kot_frame.koters_list:
            Label(self, text=v).pack()

    def create_meal_frame(self):
        self.hide_all_frames()
        meal_frame = MealFrame(self)
        meal_frame.pack()
        self.create_menu()

    def create_list_meal_frame(self):
        self.hide_all_frames()
        list_meal_frame = ListMealFrame(self, None)
        list_meal_frame.pack()
        self.create_menu()

    def create_info_frame(self):
        self.hide_all_frames()
        info_frame = InfoFrame(self)
        info_frame.pack()
        self.create_menu()

    def reset_kot(self):
        with open("koters.json", "r") as json_r:
            data = json.load(json_r)
            with open("koters.json", "w") as json_w:
                data.clear()
                data = {"kot_name": "", "koters_list": [], "koters_balance": [], "common_pot": 0, "list_meal": []}
                json.dump(data, json_w, indent=4)
        self.create_welcome_frame()

    def create_welcome_frame(self):
        self.hide_all_frames()
        # label on main Frame
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            if data["kot_name"] == "":
                welcome_label = Label(self, text="Bienvenue sur KotCount", font="Calibri 15")
                welcome_label.pack()
                welcome_button = ttk.Button(self, text="Créer un kot", command=self.create_kot_frame)
                welcome_button.pack(expand=True)
                self.create_menu()
            else:
                welcome_label = Label(self, text=f"Bienvenue dans le kot {data['kot_name']}", font="Calibri 15")
                welcome_label.pack(expand=True)
                reset_kot = ttk.Button(self, text=f"Reset le Kot", command=self.reset_kot)
                reset_kot.pack(expand=True)
                self.create_menu()


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
        app.hide_all_frames()
        app.create_menu()
        meal_frame = MealFrame(app)
        meal_frame.pack()

    def add_koter(self):
        self.add_koter_to_json(self.koters_name.get())
        show_koter = Label(app, text=self.koters_name.get())
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
                    data["list_meal"].append(
                        {"Cuisinier": self.selected_cook.get(),
                         "Inscrits": inscrits,
                         "Date/Type": f"{datetime.date.today()} / {self.selected_meal.get()}",
                         "PrixTotal": len(inscrits) * self.selected_price.get(),
                         "PrixCourse": 0,
                         "State_count": False
                         })
                    for v in data["koters_balance"]:
                        name = list(v.keys())[0]
                        balance = list(v.values())[0]
                        balance += self.dict_inscription[name]
                        v.update({name: balance})
                    json.dump(data, json_w, indent=4)
            app.hide_all_frames()
            app.create_menu()
            list_meal_frame = ListMealFrame(app, dict(copy_dict_inscription))
            list_meal_frame.pack()


class ListMealFrame(ttk.Frame):
    def __init__(self, container, list_inscription):
        super().__init__(container)
        self.inscription = list_inscription
        self.create_widgets()

    def create_widgets(self):
        # headers
        Label(self, text='Inscrits').grid(row=0, column=1, padx=10)
        Label(self, text='Cuisinier').grid(row=0, column=2, padx=10)
        Label(self, text='Date/Type').grid(row=0, column=3, padx=10)
        Label(self, text='Prix total').grid(row=0, column=4, padx=10)
        Label(self, text='Prix Course').grid(row=0, column=5, padx=10)
        Label(self, text='Calcule').grid(row=0, column=6, padx=10)
        # body
        with open("koters.json", "r") as json_r:
            data = json.load(json_r)
            with open("koters.json", "w") as json_w:
                for i, v in enumerate(data["koters_balance"]):
                    name = list(v.keys())[0]
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
                json.dump(data, json_w, indent=4)


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


if __name__ == "__main__":
    import datetime
    import json

    app = App()
    app.mainloop()
