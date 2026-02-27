from tkinter import *
from tkinter import messagebox
import calendar

#calendar function definition
def showCalendar():
    try:
        year = int(year_field.get())

        top = Toplevel(root)
        top.title(f"Calendar - {year}")
        top.geometry("1050x1000")
        top.configure(bg="#1e1e2f")

        cal_content = calendar.calendar(year)

        Label(top,
              text=f"Calendar for {year}",
              font=("Segoe UI", 18, "bold"),
              bg="#1e1e2f",
              fg="white").pack(pady=10)

        Label(top,
              text=cal_content,
              font=("Consolas", 10),
              bg="#2b2b3c",
              fg="#00ffcc",
              justify=LEFT).pack(padx=20, pady=10)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid year!")

#Main Window
root = Tk()
root.title("Calendar App")
root.geometry("400x300")
root.configure(bg="#1e1e2f")

#Main Frame
frame = Frame(root, bg="#2b2b3c", bd=0)
frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=320, height=220)

Label(frame,
      text="Calendar Generator",
      font=("Segoe UI", 18, "bold"),
      bg="#2b2b3c",
      fg="white").pack(pady=15)

Label(frame,
      text="Enter Year",
      font=("Segoe UI", 12),
      bg="#2b2b3c",
      fg="#cccccc").pack()

year_field = Entry(frame,
                   font=("Segoe UI", 12),
                   justify=CENTER,
                   bd=2,
                   relief=FLAT)
year_field.pack(pady=10)

Button(frame,
       text="Show Calendar",
       font=("Segoe UI", 11, "bold"),
       bg="#00adb5",
       fg="white",
       activebackground="#007f86",
       activeforeground="white",
       bd=0,
       padx=10,
       pady=5,
       command=showCalendar).pack(pady=5)

Button(frame,
       text="Exit",
       font=("Segoe UI", 10),
       bg="#ff4d4d",
       fg="white",
       bd=0,
       padx=10,
       pady=5,
       command=root.destroy).pack(pady=5)

root.mainloop()