from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open('data.json', 'w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def find_password():
    website = website_entry.get().title()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No data file found')
    else:
        try:
            email = data[website]['email']
            password = data[website]['password']
            pyperclip.copy(password)
            messagebox.showinfo(title='Password Found', message=f"Email: {email}\nPassword: {password}\n\n[Password"
                                                                f" Copied To Clipboard!]")
        except KeyError:
            messagebox.showinfo(title='Error', message=f"{website} details does not exist")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=2, row=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=1, row=2)
email_label = Label(text="Email/Username:")
email_label.grid(column=1, row=4)
password_label = Label(text="Password:")
password_label.grid(column=1, row=5)

# Entries
website_entry = Entry(width=30)
website_entry.grid(row=2, column=2, columnspan=2)
website_entry.focus()
email_entry = Entry(width=30)
email_entry.grid(row=4, column=2, columnspan=2)
email_entry.insert(0, "dassayan375@gmail.com")
password_entry = Entry(width=30)
password_entry.grid(row=5, column=2, columnspan=2)

# Buttons
search_button = Button(text='Search For Password', width=25, command=find_password)
search_button.grid(row=3, column=2, columnspan=2)
generate_password_button = Button(text="Generate Password", command=generate_password, width=25)
generate_password_button.grid(row=6, column=2, columnspan=2)
add_button = Button(text="Add", width=25, command=save)
add_button.grid(row=7, column=2, columnspan=2)

window.mainloop()
