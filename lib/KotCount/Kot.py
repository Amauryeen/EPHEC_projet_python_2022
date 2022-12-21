class Kot:
    def __init__(self, kot_name, koters=[]):
        self.kot_name = kot_name
        self.koters = koters

    def add_koter_to_list(self, koter):
        self.koters.append(koter)

    def print_koters_balance(self):
        for v in self.koters:
            print(f"""          {v.name} : {v.balance}€""")
