class Kot:
    def __init__(self, kot_name, koters=[]):
        self.kot_name = kot_name
        self.koters = koters

    def add_koter_to_list(self, koter):
        self.koters.append(koter)

    def print_koters_balance(self):
        for v in self.koters:
            print(f"""          {v.name} : {v.balance}€""")


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




