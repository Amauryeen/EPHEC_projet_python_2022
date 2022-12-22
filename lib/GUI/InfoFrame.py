from tkinter import *
from tkinter import ttk
import json


class InfoFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.app = container
        self.create_widgets()

    @staticmethod
    def get_min_balance_positive(list_balance):
        """
        get the minimum positive balance from a list

        PRE: need a list of person and their balance
        POST: return a list containing the name and the balance which is the lowest in the positive
        """
        min_balance = 999999
        min_person = ""
        for each in list_balance:
            if each["balance"] > 0:
                if each["balance"] <= min_balance:
                    min_balance = each["balance"]
                    min_person = each["name"]
        return [min_person, min_balance]

    @staticmethod
    def get_min_balance_negative(list_balance):
        """
        get the minimum negative balance from a list

        PRE:need a list of person and their balance
        POST: return a list containing the name and the balance which is the lowest in the negative
        """
        min_negative_balance = -99999
        min_negative_person = ""
        for each in list_balance:
            if each["balance"] < 0:
                if each["balance"] >= min_negative_balance:
                    min_negative_balance = each["balance"]
                    min_negative_person = each["name"]
        return [min_negative_person, min_negative_balance]

    def check_to_balance(self, list_person_and_balance):
        """
        make a checkout to reimburse everyone

        PRE: list of person and their balance
        POST: return a list containing strings that says who needs to reimburse who
        """
        person_and_balance: list = list_person_and_balance
        list_of_reimbursement = []
        while len(person_and_balance) != 0:
            if len(person_and_balance) == 1:
                break
            min_pos = self.get_min_balance_positive(person_and_balance)
            min_neg = self.get_min_balance_negative(person_and_balance)
            if (min_pos[1] + min_neg[1]) == 0:
                for v in person_and_balance:
                    if min_neg[0] in v.values():
                        person_and_balance.remove(v)
                    elif min_pos[0] in v.values():
                        person_and_balance.remove(v)
                list_of_reimbursement.append(f"{min_pos[0]} doit {min_pos[1]}€ à {min_neg[0]}")
            elif (min_pos[1] + min_neg[1]) < 0:
                for v in person_and_balance:
                    if min_neg[0] in v.values():
                        v.update({"balance": min_pos[1] + min_neg[1]})
                    elif min_pos[0] in v.values():
                        person_and_balance.remove(v)
                list_of_reimbursement.append(f"{min_pos[0]} doit {min_pos[1]}€ à {min_neg[0]}")
            elif (min_pos[1] + min_neg[1]) > 0:
                for v in person_and_balance:
                    if min_neg[0] in v.values():
                        person_and_balance.remove(v)
                    elif min_pos[0] in v.values():
                        v.update({"balance": min_pos[1] + min_neg[1]})
                list_of_reimbursement.append(f"{min_pos[0]} doit {abs(min_neg[1])}€ à {min_neg[0]}")
        return list_of_reimbursement

    def create_widgets(self):
        """
        Method that creates the widgets

        PRE:The file koter.json should exist.
        POST:The state of self changes and the layout of the app.
        """
        Label(self, text='Virement à effectuer', font="Calibri 14 underline").grid(row=0, column=1, padx=10)
        Label(self, text="Pot Commun", font="Calibri 14 underline").grid(row=0, column=3, padx=10)
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            Label(self, text=f"{data['common_pot']} €").grid(row=1, column=3)
            for i, v in enumerate(self.check_to_balance(data["koters_balance"])):
                Label(self, text=v).grid(row=i + 1, column=1)
            reset_btn = ttk.Button(self, text="reset le remboursement", command=self.reimburse_reset, padding=15)
            reset_btn.grid(row=len(data["koters_list"]) + 1, columnspan=3)

    def reimburse_reset(self):
        """
        reset the balance and meal history from koters.json

        PRE: Should have koters.json
        POST: return to welcome frame
        """
        with open("koters.json", "r") as json_f:
            data = json.load(json_f)
            with open("koters.json", "w") as json_w:
                for each in data["koters_balance"]:
                    each["balance"] = 0
                data["list_meal"] = []
                json.dump(data, json_w, indent=4)
        self.app.create_welcome_frame()





