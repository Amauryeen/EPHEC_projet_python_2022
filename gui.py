from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

# root configuration
root = Tk()
root.title("Kotcount")
root.resizable(False, False)
root.attributes('-alpha', 0.97)


def add_koter():
    msg = f'You entered: {koters_name.get()}'
    koters_list.append(koters_name.get())
    showinfo(title='Information', message=f"{msg} {koters_list}")


def create_kot():
    hide_all_frames()
    kot_config.pack(fill="both", expand=1)


def hide_all_frames():
    kot_config.pack_forget()
    welcome_label.pack_forget()


welcome_label = Label(root, text="Bienvenue sur kotcount")
welcome_label.pack()
# create a menu
menubar = Menu(root)
root.config(menu=menubar)
file_menu = Menu(menubar, tearoff=0)
kot_menu = Menu(menubar, tearoff=0)

# add a menu item to the menu
file_menu.add_command(label='Exit', command=root.destroy)
# add the menu to the menubar
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Kot", menu=kot_menu)
kot_menu.add_command(label="Créer le kot", command=create_kot)
# window size
window_width = 720
window_height = 720

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

koters_name = StringVar()
koters_list = []


kot_config = Frame(root)
name_label = Label(kot_config, text="Ajoute un koteur")
name_label.pack()
name_entry = Entry(kot_config, textvariable=koters_name)
name_entry.pack()

add_button = ttk.Button(kot_config, text="Add", command=add_koter)
add_button.pack(pady=10)

root.mainloop()