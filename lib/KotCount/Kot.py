class Kot:
    def __init__(self, kot_name, koters=[]):
        self.kot_name = kot_name
        self.koters = koters

    def add_koter_to_list(self, koter):
        """
        Method that adds a koter to the list of koters.

        PRE: The parameter koter should be specified.

        POST: koter will be added to the list of koters so the value of koters changes.
        """
        self.koters.append(koter)

    def print_koters_balance(self):
        """
          Method that display the balance of the koters
          PRE:

          POST:
          """
        for v in self.koters:
            print(f"""          {v.name} : {v.balance}€""")
