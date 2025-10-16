#-----------------I MADE AN APP WHICH REPLIES EMAILS FOR YOU!!!---------------------------------
from tkinter import *
from tkinter import PhotoImage
import undetected_chromedriver as uc
from tkinter import messagebox
import os, sys
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import google.generativeai as genai
import time
import pyperclip


#-----------DEFINING FUNCTIONS FOR ELEMENTS IN GUI-------------------
def open():
    ea.config(state=DISABLED)
    e.config(state=DISABLED)
    e2.config(state=DISABLED)
    e3.config(state=DISABLED)

    #Part to get number of emails to reply to
    try:
        first= e3.get("1.0", 'end-1c').strip() 
        second = int(first)
        third = second - 1
    except ValueError:
        messagebox.showerror("Error", "Please Provide A Valid Number!!!")
        ea.config(state=NORMAL)
        e.config(state=NORMAL)
        e2.config(state=NORMAL)
        e3.config(state=NORMAL)
        ea.delete("1.0", "end")
        e.delete("1.0", "end")
        e2.delete("1.0", "end")
        e3.delete("1.0", "end")
    
    #Variables
    name = ea.get("1.0", 'end-1c').strip()
    email = e.get("1.0", 'end-1c').strip()
    password = e2.get("1.0", 'end-1c').strip()
    number = third
    
    #Actual Logic
    if email == '' or password == '' or number == '':
        messagebox.showerror("Error", "Please Specify Everything!!!")
        e.config(state=NORMAL)
        e2.config(state=NORMAL)
        e3.config(state=NORMAL)
        e.delete("1.0", "end")
        e2.delete("1.0", "end")
        e3.delete("1.0", "end")

    elif number == 1:
        web = uc.Chrome()
        web.get("https://mail.google.com/mail/u/0/#sent")

        genai.configure(api_key="Your API Key")
        model = genai.GenerativeModel('gemini-2.0-flash')

        #SIGN IN PART
        usern = web.find_element('xpath', '//*[@id="identifierId"]')
        usern.send_keys(f'{email}')
        usern.send_keys(Keys.ENTER)

        passw= WebDriverWait(web, 20).until(
                        EC.presence_of_element_located(('xpath', '//*[@id="password"]/div[1]/div/div[1]/input'))
                    )
        passw.send_keys(f'{password}')
        passw.send_keys(Keys.ENTER)

        #REPLYING PART
        actions = ActionChains(web)

        time.sleep(4)
        actions.send_keys(Keys.ENTER).perform()

        time.sleep(2)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()

        time.sleep(2)
        actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

        time.sleep(2)
        actions.key_down(Keys.SHIFT).send_keys('a').key_up(Keys.SHIFT).perform()

        og_email = pyperclip.paste()

        prompt = f"""
        Generate email replying to what the sender wrote here {og_email}. Make it long enuf, and make it's style suits that of what the sender wrote.
        End the reply with a sign-off appropriate to the established tone (e.g., "Best regards," "Cheers," "Talk soon") followed by {name}.
        P.S: DO NOT add else to the reply. Simply give the reply. Nothing else, please!
        And DO NOT add a subject line(like, 'Subject Re:'). Provide only the email body.
        """

        answer = model.generate_content([prompt], stream=False)
        response = answer.text.strip()

        time.sleep(1)
        actions.send_keys(f'{response}').perform()

        time.sleep(1)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()

        time.sleep(0.5)
        actions.send_keys('e').perform()

    else:
        web = uc.Chrome()
        web.get("https://mail.google.com/mail/u/0/#sent")

        genai.configure(api_key="Your API Key")
        model = genai.GenerativeModel('gemini-2.0-flash')

        #SIGN IN PART
        usern = web.find_element('xpath', '//*[@id="identifierId"]')
        usern.send_keys(f'{email}')
        usern.send_keys(Keys.ENTER)

        passw= WebDriverWait(web, 20).until(
                        EC.presence_of_element_located(('xpath', '//*[@id="password"]/div[1]/div/div[1]/input'))
                    )
        passw.send_keys(f'{password}')
        passw.send_keys(Keys.ENTER)

        #REPLYING PART
        actions = ActionChains(web)

        time.sleep(4)
        actions.send_keys(Keys.ENTER).perform()

        time.sleep(2)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()

        time.sleep(2)
        actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

        time.sleep(2)
        actions.key_down(Keys.SHIFT).send_keys('a').key_up(Keys.SHIFT).perform()

        og_email = pyperclip.paste()

        prompt = f"""
        Generate email replying to what the sender wrote here {og_email}. Make it long enuf, and make it's style suits that of what the sender wrote.
        End the reply with a sign-off appropriate to the established tone (e.g., "Best regards," "Cheers," "Talk soon") followed by {name}.
        P.S: DO NOT add else to the reply. Simply give the reply. Nothing else, please!
        And DO NOT add a subject line(like, 'Subject Re:'). Provide only the email body.
        """

        answer = model.generate_content([prompt], stream=False)
        response = answer.text.strip()

        time.sleep(1)
        actions.send_keys(f'{response}').perform()

        time.sleep(1)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()

        time.sleep(0.5)
        actions.send_keys('e').perform()

        for x in range(number):
            time.sleep(4)
            actions.send_keys(Keys.ENTER).perform()

            time.sleep(2)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()

            time.sleep(2)
            actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

            time.sleep(2)
            actions.key_down(Keys.SHIFT).send_keys('a').key_up(Keys.SHIFT).perform()

            og_email2 = pyperclip.paste()

            prompt2 = f"""
        Generate email replying to what the sender wrote here {og_email2}. Make it long enuf, and make it's style suits that of what the sender wrote.
        End the reply with a sign-off appropriate to the established tone (e.g., "Best regards," "Cheers," "Talk soon") followed by {name}.
        P.S: DO NOT add else to the reply. Simply give the reply. Nothing else, please!
        And DO NOT add a subject line(like, 'Subject Re:'). Provide only the email body.
        """

            answer2 = model.generate_content([prompt2], stream=False)
            response2 = answer2.text.strip()

            time.sleep(1)
            actions.send_keys(f'{response2}').perform()

            time.sleep(1)
            actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()

            time.sleep(0.5)
            actions.send_keys('e').perform()

            time.sleep(3)

        web.quit()
        ea.config(state=NORMAL)
        e.config(state=NORMAL)
        e2.config(state=NORMAL)
        e3.config(state=NORMAL)
        ea.delete("1.0", "end")
        e.delete("1.0", "end")
        e2.delete("1.0", "end")
        e3.delete("1.0", "end")
        

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # For development, use the current working directory
        base_path = os.path.abspath(".")

    # Construct the full path to the resource
    return os.path.join(base_path, relative_path)


#-----------DEFINING SPECIAL ELEMENTS FOR GUI-------------------
root = Tk()
root.geometry("550x400")
root.configure(background="#26366E")
root.resizable(False, False)
root.title("Mail 4 U")

 
# Set the window's icon to the logo
logo_file_path = resource_path('Path to logo')
logo = PhotoImage(file=logo_file_path)  
# Set the window's icon to the logo
root.iconphoto(False, logo)

#-----------DEFINING ELEMENTS IN GUI-------------------
title = Label(root, text="Mail 4 U", font=("Arial", 18, 'bold'), fg='white', bg='#26366E', justify=LEFT)
title.pack(pady=10)

#frame 1
frame = Frame(root, bg="#26366E")
frame.pack(anchor=W, padx=110, pady=20) 
Label(frame, text="Name: ",font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)

ea = Text(frame,borderwidth=2,bg="#9EB0F3",font=("courier", 11),fg='black', height=1, width=28)
ea.pack(side=LEFT, fill=X, expand=True)
ea.focus_set()

#frame 2
frame1 = Frame(root, bg="#26366E")
frame1.pack(anchor=W, padx=110, pady=1) 
Label(frame1, text="Gmail: ",font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)

e = Text(frame1,borderwidth=2,bg="#9EB0F3",font=("courier", 11),fg='black', height=1, width=28)
e.pack(side=LEFT, fill=X, expand=True)


# frame3 
frame2 = Frame(root, bg="#26366E")
frame2.pack(anchor=W, padx=110, pady=15)
Label(frame2, text="Password: ",font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)

e2 = Text(frame2,borderwidth=2,bg="#9EB0F3",font=("courier", 11),fg='black', height=1, width=24)
e2.pack(side=LEFT, fill=X, expand=True)

# frame4
frame3 = Frame(root, bg="#26366E")
frame3.pack(anchor=W, padx=110, pady=8)
Label(frame3, text="# Of Emails To Reply To: ",font=("Arial", 13, 'bold'), fg='white', bg='#26366E').pack(side=LEFT)

e3 = Text(frame3,borderwidth=2,bg="#9EB0F3",font=("courier", 11),fg='black', height=1, width=12)
e3.pack(side=LEFT, fill=X, expand=True)

#Run button
run = Button(root, text="Run", font=("Courier", 13, 'bold'), fg='black', bg='lightgreen', justify=CENTER, width=12, height=1)
run.pack(pady=28)
run.config(command=open)


root.mainloop()
