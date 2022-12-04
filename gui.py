import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo

# root configuration
root = tkinter.Tk()
root.title("Kotcount")
root.configure(bg="#c2c0c0")
root.resizable(False, False)
root.attributes('-alpha', 0.97)

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

koters_name = tkinter.StringVar()
koters_list = []

def add_koter():
    """ callback when the login button clicked
    """
    msg = f'You entered: {koters_name.get()}'
    koters_list.append(koters_name.get())
    showinfo(
        title='Information',
        message=f"{msg} {koters_list}"
    )



kot_config = ttk.Frame(root)
kot_config.pack(padx=10, pady=10)
name_label = ttk.Label(kot_config, text="Ajoute un koteur")
name_label.pack()
name_entry = ttk.Entry(kot_config, textvariable=koters_name)
name_entry.pack()

login_button = ttk.Button(kot_config, text="Add", command=add_koter)
login_button.pack(fill='x', expand=True, pady=10)

root.mainloop()