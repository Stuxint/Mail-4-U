from tkinter import *
from tkinter import ttk, messagebox
import os, sys
import time
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
    update_progress()
    status_label.config(text="Status: Ready")

def update_progress():
    progress_bar['value'] = progress_var.get()
    progress_bar.update()
    progress_text.config(text=f"{progress_var.get()}%")

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
            time.sleep(3)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(1)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(1)
            actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
            time.sleep(0.5)

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
            time.sleep(0.5)

            progress_var.set(int(((i + 1) / number) * 100))
            update_progress()
    except Exception as e:
        messagebox.showerror("Reply Error", f"Failed during replying emails: {e}")

#-----------------MAIN FUNCTION-----------------
def open_app():
    try:
        name_entry.config(state=DISABLED)
        email_entry.config(state=DISABLED)
        password_entry.config(state=DISABLED)
        count_entry.config(state=DISABLED)
        status_label.config(text="Status: Starting...")

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

        status_label.config(text="Status: Opening Chrome...")
        web = uc.Chrome()

        status_label.config(text="Status: Signing in...")
        sign_in(web, email, password)

        genai.configure(api_key="Your API Key")
        model = genai.GenerativeModel('gemini-2.0-flash')

        status_label.config(text="Status: Replying emails...")
        reply_email(web, name, number, model)

        web.quit()
        reset_fields()

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        reset_fields()

#-----------------MODERN GUI SETUP-----------------
root = Tk()
root.geometry("600x500")
root.configure(background="#1E1E2F")
root.resizable(False, False)
root.title("Mail 4 U")

# Title
title = Label(root, text="Mail 4 U", font=("Segoe UI", 24, "bold"), fg="#7B61FF", bg="#1E1E2F")
title.pack(pady=15)

# Entry Frame
frame = Frame(root, bg="#1E1E2F")
frame.pack(pady=20)

def create_label_entry(frame, text, row, show=None):
    Label(frame, text=text, font=("Segoe UI", 12, "bold"), fg="white", bg="#1E1E2F").grid(row=row, column=0, sticky=W, pady=10)
    entry = Entry(frame, width=30, font=("Segoe UI", 11), bg="#2E2E3F", fg="white", bd=0, insertbackground="white", show=show)
    entry.grid(row=row, column=1, padx=5)
    entry.config(highlightthickness=2, highlightbackground="#7B61FF", highlightcolor="#7B61FF")
    return entry

name_entry = create_label_entry(frame, "Name:", 0)
email_entry = create_label_entry(frame, "Gmail:", 1)
password_entry = create_label_entry(frame, "Password:", 2, show="*")
count_entry = create_label_entry(frame, "# Emails:", 3)

name_entry.focus_set()

# Progress bar with text overlay
progress_var = IntVar()
progress_bar_frame = Frame(root, bg="#1E1E2F")
progress_bar_frame.pack(pady=20)
progress_bar = ttk.Progressbar(progress_bar_frame, maximum=100, variable=progress_var, length=400)
progress_bar.pack()
progress_text = Label(progress_bar_frame, text="0%", font=("Segoe UI", 10, "bold"), fg="white", bg="#1E1E2F")
progress_text.pack(pady=5)

# Status label
status_label = Label(root, text="Status: Ready", font=("Segoe UI", 12, "bold"), fg="white", bg="#1E1E2F")
status_label.pack(pady=5)

# Modern button
def on_enter(e):
    run_button['bg'] = "#6CFF8F"
def on_leave(e):
    run_button['bg'] = "#7B61FF"

run_button = Button(root, text="Run", font=("Segoe UI", 14, "bold"), fg="white", bg="#7B61FF", activebackground="#6CFF8F", width=12, height=1, bd=0, command=open_app)
run_button.pack(pady=15)
run_button.bind("<Enter>", on_enter)
run_button.bind("<Leave>", on_leave)

root.mainloop()
