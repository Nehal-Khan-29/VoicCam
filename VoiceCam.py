# Libraries
import cv2
import os
import time
import pyttsx3
import speech_recognition as sr
import random
import tkinter as tk
from PIL import ImageTk,Image

#.......................................................................................................................
#.......................................................................................................................



# Variables
cap=cv2.VideoCapture(0)
folder_path = "VoiceCam"
photo_value_path="VoiceCam/Photo_value.txt"

# Directory add
directory = os.getcwd()
folder_name = "VoiceCam"

if not os.path.exists(os.path.join(directory, folder_name)):
    os.makedirs(os.path.join(directory, folder_name))

# Photo_value
try:
    with open(photo_value_path) as save:
        photo_value = int(save.read())
except FileNotFoundError:
    photo_value = 1


#.......................................................................................................................
#.......................................................................................................................


# Speech recognition
r = sr.Recognizer()

def take_command():
    with sr.Microphone() as source:
        print("Listening....")
        speak("Listening....")
        r.pause_threshold= 0.5
        r.energy_threshold = 1000
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        speak("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n ")
    except Exception as e:
        print("Sorry, I didn't understand that")
        speak("Sorry, I didn't understand that")
        return "none"
    return query.lower()

# Text-to-speech

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')


def speak(text):
    engine.say(text)
    engine.runAndWait()



#.......................................................................................................................
#.......................................................................................................................



# Commands
    
def close_program():
    cap.release()
    cv2.destroyAllWindows()
    engine.setProperty('voice', voices[1].id)
    speak("Closing Voice Cam")


flipp=2

def take_photo():
    speak("Taking photo")
    global photo_value   
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    image_name = "Photo {}.png".format(photo_value)
    photo_value += 1
    with open(photo_value_path, "w") as save:
        save.write(str(photo_value))
    image_path = os.path.join(folder_path, image_name)
    cv2.imwrite(image_path, frame)
    speak("Photo taken")

def flip_camera():
    speak("camera flipped and taking Photo")
    global photo_value
    ret, frame = cap.read()
    image_name = "Photo {}.png".format(photo_value)
    photo_value += 1
    with open(photo_value_path, "w") as save:
        save.write(str(photo_value))
    image_path = os.path.join(folder_path, image_name)
    cv2.imwrite(image_path, frame)
    speak("Photo taken")   

#.......................................................................................................................
#.......................................................................................................................



# Main program loop

icon = tk.Tk()
icon.title('VoiceCam')
icon.iconbitmap("icon ico.ico")
image = Image.open("icon.png")
tk_image = ImageTk.PhotoImage(image)
image_label = tk.Label(icon, image=tk_image)
image_label.pack()
icon.update()
screen_width = icon.winfo_screenwidth()
screen_height = icon.winfo_screenheight()
window_width = 256  
window_height = 226  
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
icon.geometry("+{}+{}".format(x, y))
icon.after(5000, icon.destroy)
icon.mainloop()


#..........................................................................................................
#..........................................................................................................


run =True

def ru():
    fstop = tk.Tk()

    def force_stop():
        global run
        run = False
        fstop.destroy()

    force_stop_button = tk.Button(fstop, text="Force Stop", command=force_stop, bg='red', fg='white')
    force_stop_button.pack()


    image_path = "icon.png"
    try:
        image = Image.open(image_path)
        tk_image = ImageTk.PhotoImage(image)
        image_label = tk.Label(fstop, image=tk_image)
        image_label.pack()
    except Exception as e:
        print(f"Error loading image: {e}")


    fstop.title('Force stop')
    fstop.iconbitmap("icon ico.ico")
    screen_width = fstop.winfo_screenwidth()
    screen_height = fstop.winfo_screenheight()
    window_width = 300
    window_height = 300
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    fstop.geometry("+{}+{}".format(x, y))
    #run = True
    fstop.after(3000, fstop.destroy)
    fstop.mainloop()



#..........................................................................................................
#..........................................................................................................


engine.setProperty('voice', voices[1].id)
speak("Openning Voice Cam")
speak("The Functions that Voice Cam can do is")
speak("Take photo, Flip Camera horizontally, and close program")
speak("Please get yourselves ready in 5 seconds and then the cammands will start")
time.sleep(5)
engine.setProperty('voice', voices[0].id)




while run: 


    command = take_command()
    
    if "photo" in command:
        take_photo()

    elif "close" in command:
        close_program()
        break

    elif "flip camera"in command:
        flip_camera()

    ru()



    
        

