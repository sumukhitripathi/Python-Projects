from tkinter import *
import random, string
import pyperclip

root = Tk()
root.geometry("600x500")
root.resizable(False, False)
root.title("Password Generator")

#Theme Colors
bg_color = "#ffe6f0"       
frame_color = "#fff5fa"    
btn_color = "#ff99cc"      
btn_hover = "#ff80bf"

root.configure(bg=bg_color)

#Main Frame
main_frame = Frame(root, bg=frame_color, bd=2, relief="ridge")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=360)

#Heading
heading = Label(
    main_frame,
    text="🌸 PASSWORD GENERATOR 🌸",
    font=("Helvetica", 18, "bold"),
    bg=frame_color,
    fg="#cc0066"
)
heading.pack(pady=20)

#Password Length
pass_label = Label(
    main_frame,
    text="Select Password Length",
    font=("Helvetica", 11),
    bg=frame_color
)
pass_label.pack(pady=5)

pass_len = IntVar()

length = Spinbox(
    main_frame,
    from_=8,
    to_=32,
    textvariable=pass_len,
    width=10,
    font=("Helvetica", 12),
    justify="center"
)
length.pack(pady=5)

#Password display
pass_str = StringVar()

password_entry = Entry(
    main_frame,
    textvariable=pass_str,
    font=("Courier", 14),
    width=25,
    justify="center",
    bd=2,
    relief="groove"
)
password_entry.pack(pady=20)

#Password Generator
def Generator():
    password = ''
    for x in range(0, 4):
        password = (
            random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_lowercase)
            + random.choice(string.digits)
            + random.choice(string.punctuation)
        )

    for y in range(pass_len.get() - 4):
        password = password + random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        )

    pass_str.set(password)

generate_btn = Button(
    main_frame,
    text="Generate Password",
    command=Generator,
    bg=btn_color,
    fg="white",
    font=("Helvetica", 11, "bold"),
    padx=10,
    pady=5,
    relief="flat",
    cursor="hand2"
)
generate_btn.pack(pady=5)

def Copy_password():
    pyperclip.copy(pass_str.get())  #pyperclip to copy the password to clipboard


copy_btn = Button(
    main_frame,
    text="Copy to Clipboard",
    command=Copy_password,
    bg="#ffb3d9",
    fg="white",
    font=("Helvetica", 11, "bold"),
    padx=10,
    pady=5,
    relief="flat",
    cursor="hand2"
)
copy_btn.pack(pady=10)

root.mainloop()