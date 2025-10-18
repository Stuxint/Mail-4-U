from tkinter import *
from tkinter import PhotoImage, messagebox
import os, sys, time
import pyperclip
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import google.generativeai as genai

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def reset_fields():
    ea.config(state=NORMAL)
    e.config(state=NORMAL)
    e2.config(state=NORMAL)
    e3.config(state=NORMAL)
    ea.delete("1.0", "end")
    e.delete("1.0", "end")
    e2.delete("1.0", "end")
    e3.delete("1.0", "end")

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
    except Exception as e:
        messagebox.showerror("Reply Error", f"Failed during replying emails: {e}")

#-----------------MAIN FUNCTION FOR GUI-----------------
def open_app():
    try:
        ea.config(state=DISABLED)
        e.config(state=DISABLED)
        e2.config(state=DISABLED)
        e3.config(state=DISABLED)

        try:
            number = int(e3.get("1.0", 'end-1c').strip())
        except ValueError:
            messagebox.showerror("Error", "Please provide a valid number!")
            reset_fields()
            return

        name = ea.get("1.0", 'end-1c').strip()
        email = e.get("1.0", 'end-1c').strip()
        password = e2.get("1.0", 'end-1c').strip()

        if not email or not password or number <= 0:
            messagebox.showerror("Error", "Please specify all fields correctly!")
            reset_fields()
            return

        try:
            web = uc.Chrome()
        except Exception as e:
            messagebox.showerror("Browser Error", f"Failed to open Chrome: {e}")
            reset_fields()
            return

        try:
            sign_in(web, email, password)
        except RuntimeError as e:
            messagebox.showerror("Login Error", str(e))
            web.quit()
            reset_fields()
            return

        genai.configure(api_key="Your API Key")
        model = genai.GenerativeModel('gemini-2.0-flash')

        reply_email(web, name, number, model)

        web.quit()
        reset_fields()

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        reset_fields()

#-----------------GUI SETUP-----------------
root = Tk()
root.geometry("550x400")
root.configure(background="#26366E")
root.resizable(False, False)
root.title("Mail 4 U")

logo_file_path = resource_path('Path to logo')
logo = PhotoImage(file=logo_file_path)  
root.iconphoto(False, logo)

title = Label(root, text="Mail 4 U", font=("Arial", 18, 'bold'), fg='white', bg='#26366E')
title.pack(pady=10)

# Frame 1
frame = Frame(root, bg="#26366E")
frame.pack(anchor=W, padx=110, pady=20)
Label(frame, text="Name: ", font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)
ea = Text(frame, borderwidth=2, bg="#9EB0F3", font=("courier", 11), fg='black', height=1, width=28)
ea.pack(side=LEFT, fill=X, expand=True)
ea.focus_set()

# Frame 2
frame1 = Frame(root, bg="#26366E")
frame1.pack(anchor=W, padx=110, pady=1)
Label(frame1, text="Gmail: ", font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)
e = Text(frame1, borderwidth=2, bg="#9EB0F3", font=("courier", 11), fg='black', height=1, width=28)
e.pack(side=LEFT, fill=X, expand=True)

# Frame 3
frame2 = Frame(root, bg="#26366E")
frame2.pack(anchor=W, padx=110, pady=15)
Label(frame2, text="Password: ", font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)
e2 = Text(frame2, borderwidth=2, bg="#9EB0F3", font=("courier", 11), fg='black', height=1, width=24)
e2.pack(side=LEFT, fill=X, expand=True)

# Frame 4
frame3 = Frame(root, bg="#26366E")
frame3.pack(anchor=W, padx=110, pady=8)
Label(frame3, text="# Of Emails To Reply To: ", font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)
e3 = Text(frame3, borderwidth=2, bg="#9EB0F3", font=("courier", 11), fg='black', height=1, width=12)
e3.pack(side=LEFT, fill=X, expand=True)

# Run button
run = Button(root, text="Run", font=("Courier", 13, 'bold'), fg='black', bg='lightgreen', width=12, height=1, command=open_app)
run.pack(pady=28)

root.mainloop()
