from tkinter import *


class EntryId(Entry):
    def __init__(self, container, id_entry):
        super().__init__(container)
        self.id = id_entry
