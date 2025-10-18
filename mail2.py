from tkinter import *
from tkinter import PhotoImage, messagebox, ttk
import os, sys, time
import pyperclip
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import google.generativeai as genai

#-----------------HELPER FUNCTIONS-----------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def reset_fields():
    name_entry.config(state=NORMAL)
    email_entry.config(state=NORMAL)
    password_entry.config(state=NORMAL)
    count_entry.config(state=NORMAL)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)
    count_entry.delete(0, END)
    progress_var.set(0)
    progress_bar.update()
    status_label.config(text="Status: Ready")

def generate_reply(model, email_text, name):
    prompt = f"""
    Generate email replying to what the sender wrote here {email_text}. Make it long enough, and make its style match the sender.
    End the reply with a sign-off appropriate to the established tone followed by {name}.
    P.S: DO NOT add anything else. Only provide the email body.
    """
    try:
        answer = model.generate_content([prompt], stream=False)
        return answer.text.strip()
    except Exception as e:
        messagebox.showerror("AI Error", f"Failed to generate reply: {e}")
        return ""

def sign_in(driver, email, password):
    try:
        driver.get("https://mail.google.com/mail/u/0/#inbox")
        usern = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(('xpath', '//*[@id="identifierId"]'))
        )
        usern.send_keys(email)
        usern.send_keys(Keys.ENTER)

        passw = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(('xpath', '//*[@id="password"]/div[1]/div/div[1]/input'))
        )
        passw.send_keys(password)
        passw.send_keys(Keys.ENTER)
    except Exception as e:
        raise RuntimeError(f"Login failed: {e}")

def reply_email(driver, name, number, model):
    try:
        actions = ActionChains(driver)
        for i in range(number):
            time.sleep(4)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(2)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(2)
            actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
            time.sleep(1)

            email_text = pyperclip.paste()
            if len(email_text) < 5:
                messagebox.showwarning("Warning", "Clipboard seems empty or invalid!")
                continue

            response = generate_reply(model, email_text, name)
            if not response:
                continue

            actions.send_keys(response).perform()
            time.sleep(1)
            actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
            time.sleep(0.5)
            actions.send_keys('e').perform()
            time.sleep(1)

            progress_var.set(int(((i + 1) / number) * 100))
            progress_bar.update()

    except Exception as e:
        messagebox.showerror("Reply Error", f"Failed during replying emails: {e}")

#-----------------MAIN FUNCTION FOR GUI-----------------
def open_app():
    try:
        name_entry.config(state=DISABLED)
        email_entry.config(state=DISABLED)
        password_entry.config(state=DISABLED)
        count_entry.config(state=DISABLED)

        try:
            number = int(count_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please provide a valid number!")
            reset_fields()
            return

        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password or number <= 0:
            messagebox.showerror("Error", "Please specify all fields correctly!")
            reset_fields()
            return

        try:
            status_label.config(text="Status: Opening Chrome...")
            web = uc.Chrome()
        except Exception as e:
            messagebox.showerror("Browser Error", f"Failed to open Chrome: {e}")
            reset_fields()
            return

        try:
            status_label.config(text="Status: Signing in...")
            sign_in(web, email, password)
        except RuntimeError as e:
            messagebox.showerror("Login Error", str(e))
            web.quit()
            reset_fields()
            return

        genai.configure(api_key="Your API Key")
        model = genai.GenerativeModel('gemini-2.0-flash')

        status_label.config(text="Status: Replying emails...")
        reply_email(web, name, number, model)

        web.quit()
        reset_fields()

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        reset_fields()

#-----------------GUI SETUP-----------------
root = Tk()
root.geometry("550x450")
root.configure(background="#26366E")
root.resizable(False, False)
root.title("Mail 4 U")

# Logo
logo_file_path = resource_path('Path to logo')
if os.path.exists(logo_file_path):
    logo = PhotoImage(file=logo_file_path)
    root.iconphoto(False, logo)

# Title
title = Label(root, text="Mail 4 U", font=("Arial", 20, 'bold'), fg='white', bg='#26366E')
title.pack(pady=10)

# Style for ProgressBar
style = ttk.Style(root)
style.theme_use('clam')
style.configure("TProgressbar", thickness=20, troughcolor="#9EB0F3", background="#7B61FF")

# Frame for Entries
frame = Frame(root, bg="#26366E")
frame.pack(pady=20)

# Name
Label(frame, text="Name:", font=("Arial", 12, 'bold'), fg='white', bg='#26366E').grid(row=0, column=0, sticky=W, pady=5)
name_entry = Entry(frame, width=30, font=("Courier", 11))
name_entry.grid(row=0, column=1, pady=5)
name_entry.focus_set()

# Gmail
Label(frame, text="Gmail:", font=("Arial", 12, 'bold'), fg='white', bg='#26366E').grid(row=1, column=0, sticky=W, pady=5)
email_entry = Entry(frame, width=30, font=("Courier", 11))
email_entry.grid(row=1, column=1, pady=5)

# Password
Label(frame, text="Password:", font=("Arial", 12, 'bold'), fg='white', bg='#26366E').grid(row=2, column=0, sticky=W, pady=5)
password_entry = Entry(frame, width=30, font=("Courier", 11), show="*")
password_entry.grid(row=2, column=1, pady=5)

# Number of emails
Label(frame, text="# of Emails:", font=("Arial", 12, 'bold'), fg='white', bg='#26366E').grid(row=3, column=0, sticky=W, pady=5)
count_entry = Entry(frame, width=10, font=("Courier", 11))
count_entry.grid(row=3, column=1, pady=5, sticky=W)

# Progress bar
progress_var = IntVar()
progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var, length=400)
progress_bar.pack(pady=15)

# Status label
status_label = Label(root, text="Status: Ready", font=("Arial", 12, 'bold'), fg='white', bg='#26366E')
status_label.pack(pady=5)

# Run button
run_button = Button(root, text="Run", font=("Courier", 13, 'bold'), fg='black', bg='lightgreen', width=12, height=1, command=open_app)
run_button.pack(pady=10)

root.mainloop()
