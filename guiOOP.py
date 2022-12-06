from tkinter import *
from tkinter import ttk
from kotcount import *
from tkinter.messagebox import showinfo


class App(Tk):
    def __init__(self):
        super().__init__()
        # configure the window
        self.title("kotcount")
        self.minsize(width=400, height=400)
        self.create_welcome_frame()

    @staticmethod
    def get_kot(self):
        with open("koters.json", 'r') as json_r:
            data = json.load(json_r)
            kot = Kot(data["kot_name"])
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
            widget.destroy()

    def create_menu(self):
        self.menubar = Menu(self)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.kot_menu = Menu(self.menubar, tearoff=0)
        self.meal_menu = Menu(self.menubar, tearoff=0)
        self.list_meal_menu = Menu(self.menubar, tearoff=0)
        self.info_menu = Menu(self.menubar, tearoff=0)
        self.config(menu=self.menubar)
        self.file_menu.add_command(label="Acceuil", command=self.create_welcome_frame)
        self.file_menu.add_command(label='Exit', command=self.destroy)
        self.menubar.add_cascade(label="App", menu=self.file_menu)
        self.menubar.add_cascade(label="Kot", menu=self.kot_menu)
        self.kot_menu.add_command(label="Créer le kot", command=self.create_kot_frame)
        self.menubar.add_cascade(label="Repas", menu=self.meal_menu)
        self.meal_menu.add_command(label="Ouvrir", command=self.create_meal_frame)
        self.menubar.add_cascade(label="Liste repas", menu=self.list_meal_menu)
        self.list_meal_menu.add_command(label="Ouvrir", command=self.create_list_meal_frame)
        self.menubar.add_cascade(label="Info",menu=self.info_menu)
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
        list_meal_frame = ListMealFrame(self)
        list_meal_frame.pack()
        self.create_menu()

    def create_info_frame(self):
        self.hide_all_frames()
        info_frame = InfoFrame(self)
        info_frame.pack()
        self.create_menu()

    def create_welcome_frame(self):
        self.hide_all_frames()
        # label on main Frame
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            if data["kot_name"] == "":
                welcome_label = Label(self, text="Bienvenue sur kotcount", font="Calibri 15")
                welcome_label.pack()
                welcome_button = ttk.Button(self, text="Créer un kot", command=self.create_kot_frame)
                welcome_button.pack(expand=True)
                self.create_menu()
            else:
                welcome_label = Label(self, text=f"Bienvenue dans le kot {data['kot_name']}", font="Calibri 15")
                welcome_label.pack(expand=True)
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
        self.name_label = Label(self, text="Ajoute un koteur")
        self.name_label.grid(column=0, row=2)
        self.name_entry = ttk.Entry(self, textvariable=self.koters_name)
        self.name_entry.grid(column=0, row=3)
        self.add_button = ttk.Button(self, text="Ajouter", command=self.add_koter)
        self.add_button.grid(column=3, row=3, padx=5)
        self.koter_to_delete_label = Label(self, text="Supprime un koteur")
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
    def add_koter_to_json(self, koter):
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
        self.add_koter_to_json(self, self.koters_name.get())
        show_koter = Label(app, text=self.koters_name.get())
        show_koter.pack()
        self.name_entry.delete(0, END)

    def delete_koter(self):
        self.delete_koter_from_json(self, self.koter_to_delete.get())
        self.koter_to_delete_entry.delete(0, END)
        app.create_kot_frame()

    @staticmethod
    def delete_koter_from_json(self, koter):
        with open("koters.json", "r") as r_json:
            data = json.load(r_json)
        with open("koters.json", "w") as w_json:
            try:
                data["koters_list"].remove(koter)
            except ValueError:
                json.dump(data, w_json, indent=4)


class MealFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.cook_label = Label(self, text="Choisir le cuisinier")
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
            Label(self, text="S'inscrire : ", font='Calibri 14 underline').pack()
            for v in data["koters_list"]:
                self.dict_inscription[v] = IntVar()
                ttk.Checkbutton(self, text=v, variable=self.dict_inscription[v], offvalue=0, onvalue=1).pack()
            ttk.Button(self, text="Finaliser le repas", command=self.get_inscription).pack(pady=5)

    def get_inscription(self):
        if self.selected_price.get() <= 0:
            showinfo(title="Attention", message="le prix du repas doivent être des entiers positifs")
        else:
            self.dict_inscription[self.selected_cook.get()] = 0
            for v, name in zip(self.dict_inscription.values(), self.dict_inscription.keys()):
                if self.selected_cook.get() == name:
                    continue
                elif v.get() == 1:
                    self.dict_inscription[name] = v.get() * self.selected_price.get()
                    self.dict_inscription[self.selected_cook.get()] -= self.selected_price.get()
                else:
                    self.dict_inscription[name] = v.get()
            with open("koters.json", "r") as json_r:
                data = json.load(json_r)
                with open("koters.json", "w") as json_w:
                    for v in data["koters_balance"]:
                        name = list(v.keys())[0]
                        balance = list(v.values())[0]
                        balance += self.dict_inscription[name]
                        v.update({name: balance})
                    json.dump(data, json_w, indent=4)
            app.hide_all_frames()
            app.create_menu()
            list_meal_frame = ListMealFrame(app)
            list_meal_frame.pack()


class ListMealFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.create_widgets()

    def create_widgets(self):
        # headers
        Label(self, text='Inscrits').grid(row=0, column=1, padx=10)
        Label(self, text='Cuisinier').grid(row=0, column=2, padx=10)
        Label(self, text='Prix total').grid(row=0, column=3, padx=10)
        Label(self, text='Prix Course').grid(row=0, column=4, padx=10)
        Label(self, text='Calcule').grid(row=0, column=5)

        # body
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            for i in enumerate(data["koters_list"]):
                Label(self, text=str(i[0]+1)).grid(row=i[0]+1, column=0)


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
                    Label(self, text=f"{name} €", foreground='red').grid(row=i + 1, column=1)
                    Label(self, text=f"{balance} €", foreground='red').grid(row=i + 1, column=2)
                else:
                    Label(self, text=f"{name} €", foreground='green').grid(row=i + 1, column=1)
                    Label(self, text=f"{balance} €", foreground='green').grid(row=i + 1, column=2)
            Label(self, text=f"{data['common_pot']} €").grid(row=4, column=3)


if __name__ == "__main__":
    import json

    app = App()
    app.mainloop()
