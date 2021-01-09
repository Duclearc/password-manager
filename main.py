from tkinter import Tk, PhotoImage, Canvas, Label, Entry, Button, END, messagebox
from characters import letters, numbers, symbols
from random import choice, randint, shuffle
from json import load, dump
import pyperclip

# CONSTANTS ------------------------------ #
WIDTH = 200
HEIGHT = 200
FONT = ('Arial', 20, 'normal')
DEFAULT_EMAIL = 'dan@duclearc.com'
DEFAULT_USERNAME = 'Duclearc'


# PASSWORD GENERATOR --------------------- #
def new_password():
    """clears password field and
    generates a new password between 25-40 chars long,
    composed of letters, numbers and symbols.
    The generated password is then copied to your clipboard"""
    entry_password.delete(0, END)
    random_letters = [choice(letters) for _ in range(randint(10, 16))]
    random_numbers = [choice(numbers) for _ in range(randint(10, 16))]
    random_symbols = [choice(symbols) for _ in range(randint(5, 11))]
    password_chars = random_letters + random_numbers + random_symbols
    shuffle(password_chars)
    final_password = ''.join(password_chars)
    pyperclip.copy(final_password)
    entry_password.insert(0, final_password)


# FORM ACTIONS --------------------------- #
def search_for_password():
    """searches for the password on the local file."""
    query = entry_website.get()
    if len(query) == 0:
        messagebox_title = "'Website' is required for search"
        messagebox_message = 'Please make sure you\'ve added a search term'
    else:
        try:
            with open('./passwords.json') as password_file:
                file_data = load(password_file)
        except FileNotFoundError:
            messagebox_title = 'No passwords on file'
            messagebox_message = 'No passwords have been found.'
        else:
            if query in file_data:
                query_data = file_data[query]
                messagebox_title = 'Password found!'
                messagebox_message = f"{query}\n\n" \
                                     f"EMAIL:\n{query_data['email']}\n\n" \
                                     f"USERNAME:\n{query_data['username']}\n\n" \
                                     f"PASSWORD:\n{query_data['password']}\n\n" \
                                     f"Password has been copied to your clipboard"
                pyperclip.copy(query_data['password'])
            else:
                messagebox_title = 'No passwords under that name'
                messagebox_message = 'No passwords have been found for this website.\n\n' \
                                     'Try retyping the URL exactly as you saved it'

    messagebox.showinfo(title=messagebox_title,
                        message=messagebox_message)


def get_data():
    """gets all data from input fields and returns it as a dictionary"""
    website = entry_website.get()
    email = entry_email.get()
    username = entry_username.get()
    password = entry_password.get()
    if username == '':
        username = '-'
    return {'website': website, 'email': email, 'username': username, 'password': password}


def is_valid(data):
    """checks that all input fields are filled and return True or False accordingly"""
    if len(data['website']) == 0 or len(data['email']) == 0 or len(data['password']) == 0:
        messagebox.showinfo(title="'Website', 'Email' and 'Password' are required",
                            message='Please make sure you\'ve filled all necessary fields')
        return False
    else:
        return True


def confirm_entries(data):
    """opens a message box displaying all data. Returns True if user clicks 'Ok' and False if 'Cancel'"""
    confirmation_message = f"{data['website']}\n\n" \
                           f"EMAIL:\n{data['email']}\n\n" \
                           f"USERNAME:\n{data['username']}\n\n" \
                           f"PASSWORD:\n{data['password']}\n\n\n" \
                           f"Proceed with data?"
    return messagebox.askokcancel(title=data['website'], message=confirmation_message)


def save_data(data):
    try:
        with open('./passwords.json') as passwords_file:
            file_data = load(passwords_file)
    except FileNotFoundError:
        with open('./passwords.json', 'w') as passwords_file:
            dump(data, passwords_file, indent=4)
    else:
        file_data.update(data)
        with open('./passwords.json', 'w') as passwords_file:
            dump(file_data, passwords_file, indent=4)
        messagebox.showinfo(title='Done',
                            message='Your password has been copied to your clipboard and saved on file')


def reset_form():
    """resets the website and password fields to blank"""
    entry_website.delete(0, END)
    entry_password.delete(0, END)


# SAVE PASSWORD -------------------------- #
def save_password():
    """if data is valid and confirmed, saves them as a new row in 'passwords.json'"""
    data = get_data()
    if is_valid(data):
        if confirm_entries(data):
            formatted_data = {
                data['website']: {
                    'email': data['email'],
                    'username': data['username'],
                    'password': data['password'],
                }
            }
            save_data(formatted_data)
            reset_form()


# UI SETUP ------------------------------- #
# WINDOW
window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=30)
window.minsize(width=3 * WIDTH, height=2 * HEIGHT)

# LOGO IMAGE
logo = PhotoImage(file='./logo.png')
canvas = Canvas(width=WIDTH, height=HEIGHT)
canvas.create_image(WIDTH / 2, HEIGHT / 2, image=logo)
canvas.grid(column=0, row=0, columnspan=4)

# FORM
# website
label_website = Label(text='Website:', font=FONT)
label_website.grid(column=0, row=1)
entry_website = Entry(width=30)
entry_website.focus()
entry_website.grid(column=1, row=1)
# search website button
search_website = Button(text='SEARCH  EXISTING  PASSWORD', width=32, fg='red', command=search_for_password)
search_website.grid(column=2, row=1, columnspan=2)
# email
label_email = Label(text='Email:', font=FONT)
label_email.grid(column=0, row=2)
entry_email = Entry(width=30)
entry_email.insert(0, DEFAULT_EMAIL)
entry_email.grid(column=1, row=2)
# username
label_username = Label(text='Username:', font=FONT)
label_username.grid(column=2, row=2)
entry_username = Entry(width=20)
entry_username.insert(0, DEFAULT_USERNAME)
entry_username.grid(column=3, row=2)
# password
label_password = Label(text='Password:', font=FONT)
label_password.grid(column=0, row=3)
entry_password = Entry(width=30)
entry_password.grid(column=1, row=3)
# generate password button
generate_password = Button(text='GENERATE  PASSWORD', width=32, fg='red', command=new_password)
generate_password.grid(column=2, row=3, columnspan=2)
# save button
save_password = Button(text='S A V E', width=48, font=FONT, fg='red', command=save_password)
save_password.grid(column=1, row=4, columnspan=3)

window.mainloop()
