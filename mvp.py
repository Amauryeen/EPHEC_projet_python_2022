class Kot:
    def __init__(self, kot_name, koters=[]):
        self.kot_name = kot_name
        self.koters = koters

    def add_koter_to_list(self, koter):
        self.koters.append(koter)


class Person(Kot):
    def __init__(self, name):
        super().__init__(self)
        self.__name = name
        self.__balance = 0
        self.add_koter_to_list(self)

    def __str__(self):
        return f"{self.name}"

    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_balance):
        self.__balance = new_balance


def get_cook(koters):
    return koters[random.randint(0, len(koters) - 1)]


def print_koters_balance(kot):
    for v in kot:
        print(f"""          {v.name} : {v.balance}€""")


def main():
    args = argparse.ArgumentParser(description="Permet de calculer les dépenses de plusieurs membres d'un kot et ce que chacun doit au cuisinier.",
                                   epilog=f"example: {os.path.basename(__file__)} \"Sam Gratte\" \"Ray Zin\" \"Jean Tille\" -k \"Notre kot\" -p 3")
    args.add_argument("names", metavar="name", help="prénom et nom de chaque membre du kot au format \"Prénom Nom\"", nargs="+")
    args.add_argument("-k", "--kot_name", help="nom du kot", required=True)
    args.add_argument("-p", "--price", help="prix positif d'un repas unitaire (euros)", type=float, required=True)
    argument = args.parse_args()
    kot = Kot(argument.kot_name)

    if argument.price < 0:
        raise Exception(f"Le prix est un nombre négatif.")

    for v in argument.names:
        if " " in v:
            Person(v)
            continue
        raise Exception(f"\"{v}\" n'est pas composé d'un prénom et d'un nom.")

    cook = get_cook(kot.koters)
    print(f"============================================\n{cook.name} est le cuisinier de ce repas.\n============================================\n")

    inscription = []

    counter = 0
    while counter == 0:
        response = input(
            "Souhaitez-vous inscrire tous les membres au repas?   [O + Entrée] Oui   [N + Entrée] Non   [Q + Entrée] Quitter le programme : ")
        if response.lower() == "o":
            for v in kot.koters:
                if v == cook:
                    continue
                inscription.append(v)
            counter = 1
        if response.lower() == "n":
            for v in kot.koters:
                if v == cook:
                    continue

                counter = 0
                while counter == 0:
                    response = input(
                        f"Faut-il inscrire \"{v.name}\" au repas?   [O + Entrée] Oui   [N + Entrée] Non   [Q + Entrée] Quitter le programme : ")
                    counter = 0
                    if response.lower() == "o":
                        inscription.append(v)
                        counter = 1
                    if response.lower() == "n":
                        counter = 1

                    if response.lower() == "q":
                        print("Fermeture du programme.")
                        exit()
            counter = 1

        if response.lower() == "q":
            print("Fermeture du programme.")
            exit()

    for v in inscription:
        v.balance -= argument.price
        cook.balance += argument.price

    print(f"""
    ==============================
    Kot : {kot.kot_name}
    Prix par repas : {argument.price} €
    Cuisinier : {cook.name}
    ==============================
    Solde(s) : """)

    print_koters_balance(kot.koters)

    print("    ==============================")


if __name__ == "__main__":
    import random
    import argparse
    import os
    import math

    main()
