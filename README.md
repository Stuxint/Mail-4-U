# Mail 4 U – Your Smart Email Assistant

Hi there! 👋  

After seeing how many people struggled with the overwhelming number of emails they had to reply to, I decided to build a solution: **Mail 4 U** – an app that automatically helps you reply to your emails.  

I’m continuously improving it, so if you have any suggestions, feel free to share. Thank you and good luck! 😄  

---

## ⚡ Features

- Automatically generates replies to your emails using AI  
- Handles multiple emails efficiently  
- Modern and user-friendly GUI with a dark theme  
- Real-time progress tracking with percentage display  
- Run & Cancel buttons for better control  

---

## 📝 Note

When running the app, try **not to copy anything manually**, as the app uses the clipboard to read email contents and generate replies. Copying other text may cause it to respond incorrectly.  

I’m working on a solution to make this even smoother, and I appreciate your understanding.  

---

## 🚀 Getting Started

1. Install the required Python packages:

``` bash
pip install tkinter pyperclip undetected-chromedriver selenium google-generativeai
```

## Configure your Google API Key in the script

``` bash
genai.configure(api_key="Your API Key")
```
## Run the app

``` bash
python main.py 

or run exe file
```