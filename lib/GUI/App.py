from tkinter import *
from tkinter import ttk
import json
from lib.KotCount.Kot import Kot
from lib.KotCount.Person import Person
from lib.GUI.KotFrame import KotFrame
from lib.GUI.MealFrame import MealFrame
from lib.GUI.ListMealFrame import ListMealFrame
from lib.GUI.InfoFrame import InfoFrame


class App(Tk):
    def __init__(self):
        super().__init__()
        # configure the window
        self.title("KotCount")
        self.minsize(width=400, height=400)
        self.create_welcome_frame()

    @staticmethod
    def get_kot(self):
        """
        get the info for the kot from the koters.json
        PRE: need the koters.json file
        POST: create instance of person from the class Person
        """
        with open("koters.json", 'r') as json_r:
            data = json.load(json_r)
            self.kot = Kot(data["kot_name"])
            for person in data["koters_list"]:
                Person(person)

    def hide_all_frames(self):
        """
        hide all frames

        PRE:
        POST: Hide all frames and destroy them
        """
        for widget in App.winfo_children(self):
            widget.destroy()
        for widget in KotFrame.winfo_children(self):
            widget.destroy()
        for widget in MealFrame.winfo_children(self):
            widget.destroy()
        for widget in ListMealFrame.winfo_children(self):
            widget.grid_forget()

    def create_menu(self):
        """
        Create the menubar

        PRE:
        POST: create the menubar and add it to the frame
        """
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
        """
        create the kot creation frame

        PRE:
        POST:show the kot frame
        """
        self.hide_all_frames()
        kot_frame = KotFrame(self)
        kot_frame.pack()
        self.create_menu()
        kot_frame.koters_list = []
        kot_frame.get_data_from_json()
        Label(self, text="Membres du Kot :", font='Calibri 14 underline').pack()
        for v in kot_frame.koters_list:
            Label(self, text=v).pack()

    def create_meal_frame(self):
        """
        create the meal creation frame

        PRE:
        POST: show the meal frame
        """
        self.hide_all_frames()
        meal_frame = MealFrame(self)
        meal_frame.pack()
        self.create_menu()

    def create_list_meal_frame(self):
        """
        create the list meal frame which display the history of meals of the kot
        PRE:
        POST: create the list meal frame
        """
        self.hide_all_frames()
        list_meal_frame = ListMealFrame(self, None)
        list_meal_frame.pack()
        self.create_menu()

    def create_info_frame(self):
        """
        create the info frame which show the common pot and the reimbursement of the koters

        PRE:
        POST: create the info frame
        """
        self.hide_all_frames()
        info_frame = InfoFrame(self)
        info_frame.pack()
        self.create_menu()

    def reset_kot(self):
        """
        button event to totally reset the kot
        PRE: need koters.json
        POST: reset the info in koters.json
        """
        with open("koters.json", "r") as json_r:
            data = json.load(json_r)
            with open("koters.json", "w") as json_w:
                data.clear()
                data = {"kot_name": "", "koters_list": [], "koters_balance": [], "common_pot": 0, "list_meal": []}
                json.dump(data, json_w, indent=4)
        self.create_welcome_frame()

    def create_welcome_frame(self):
        """
        create the welcome frame

        PRE:
        POST: create the welcome frame
        """
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
