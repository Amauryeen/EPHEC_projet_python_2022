from tkinter import *
from tkinter import ttk


class App(Tk):
    def __init__(self):
        super().__init__()
        # configure the window
        self.title("kotcount")
        self.resizable(width=False, height=True)
        # window size
        self.window_width = 400
        self.window_height = 400

        # get the screen dimension
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.create_welcome_frame()

    def hide_all_frames(self):
        for widget in App.winfo_children(self):
            widget.destroy()
        for widget in KotFrame.winfo_children(self):
            widget.destroy()
        for widget in MealFrame.winfo_children(self):
            widget.destroy()

    def create_menu(self):
        self.menubar = Menu(self)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.kot_menu = Menu(self.menubar, tearoff=0)
        self.meal_menu = Menu(self.menubar, tearoff=0)
        self.config(menu=self.menubar)
        self.file_menu.add_command(label="Acceuil", command=self.create_welcome_frame)
        self.file_menu.add_command(label='Exit', command=self.destroy)
        self.menubar.add_cascade(label="App", menu=self.file_menu)
        self.menubar.add_cascade(label="Kot", menu=self.kot_menu)
        self.kot_menu.add_command(label="Créer le kot", command=self.create_kot_frame)

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

    def create_welcome_frame(self):
        self.hide_all_frames()
        # label on main Frame
        self.welcome_label = Label(self, text="Bienvenue sur kotcount")
        self.welcome_label.place(y=125, x=125)
        self.welcome_button = ttk.Button(self, text="Créer un kot", command=self.create_kot_frame)
        self.welcome_button.place(y=150, x=150)
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

    def add_koter_to_json(self, koter):
        with open("koters.json", "r") as r_json:
            data = json.load(r_json)
        with open("koters.json", "w") as w_json:
            data["koters_list"].append(koter)
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
        self.dict_inscription = {}
        self.create_widget()

    def create_widget(self):
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            ttk.Combobox(self, textvariable=self.selected_cook, values=data["koters_list"], state="readonly").pack()
            Label(self, text="Repas").pack()
            ttk.Combobox(self, textvariable=self.selected_meal, values=("Matin", "Midi", "Soir"),
                         state="readonly").pack()
            Label(self, text="S'inscrire : ", font='Calibri 14 underline').pack()
            for v in data["koters_list"]:
                self.dict_inscription[v] = StringVar()
                ttk.Checkbutton(self, text=v, variable=self.dict_inscription[v]).pack()
            ttk.Button(self, text="Finaliser le repas", command=self.get_inscription).pack()

    def get_inscription(self):
        for v, name in zip(self.dict_inscription.values(), self.dict_inscription.keys()):
            self.dict_inscription[name] = v.get()
        print(self.dict_inscription)


if __name__ == "__main__":
    import json

    app = App()
    app.mainloop()
