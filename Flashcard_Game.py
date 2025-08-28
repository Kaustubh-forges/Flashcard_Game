#-------------------- Flashcard Game---------------------

#-------------------- MODULES IMPORTED-------------------
from tkinter import *
from data_extraction import select_random_word
import random
import pandas

#-------------------- CONSTANTS-------------------
BACKGROUND_COLOR = "#B1DDC6"

# Functions for enabling + disabling tick and cross buttons
def disable_tick_button():
    Tick_mark_button.configure(state="disabled")
def enable_tick_button():
    Tick_mark_button.configure(state="normal")
def disable_cross_button():
    Cross_mark_button.configure(state="disabled")
def enable_cross_button():
    Cross_mark_button.configure(state="normal")

def cleanup(Lable1,Label2):
    Lable1.destroy()
    Label2.destroy()
    message()

def message():
    Label3 = Label(text="Press tick button if you got the right answer;\ncross button if you got it wrong")
    Label3.configure(font=("Ariel", 25, "normal"))
    Label3.place(x=180, y=200)
    Window.after(3000, remove_message, Label3)

def remove_message(Label3):
    Label3.destroy()
    enable_tick_button()
    enable_cross_button()
# Aesthetics for the English word card
def english_card(Label1,Label2,english_word):
    Canvas1.itemconfigure(photo_on_canvas,image=Card_Back)
    Label1.configure(text="English",font=("Ariel",40,"italic"),foreground="white",background=BACKGROUND_COLOR)
    Label2.configure(text=english_word,font=("Ariel",60,"bold"),foreground="white",background=BACKGROUND_COLOR)
    Window.after(3000,cleanup,Label1,Label2)
# Changes display from French card to English card after 3 seconds
def change(Label1,Label2,english_word):
    Window.after(3000,english_card,Label1,Label2,english_word)


def start_game():
    start_button.destroy()
    intro_label.destroy()
    Canvas1.itemconfigure(photo_on_canvas,image=Card_Front)
    dict_for_word=select_random_word() # Receives a list with dictionaries containing all the French words and their English translations
    random_number=random.randint(0,100)
    french_word=dict_for_word[random_number]["French"] # Picks a random French word from the list
    english_word=dict_for_word[random_number]["English"] # Picks a random corresponding English word from the list
    Label1 = Label(text="French", font=("Ariel", 40, "italic"), background="white")
    Label1.place(x=400, y=150)
    Label2= Label(text=french_word, font=("Ariel", 60, "bold"), background="white")
    Label2.place(x=400, y=263)
    change(Label1,Label2,english_word)

def store_data_and_show_new_card():
    try:
        with open("score.txt", "r") as file:
            score = int(file.read())

    except FileNotFoundError:
        score=1 # Score is initialized to 1 because this part of the function is only accessed when user has guessed correct for the first time and "score.txt" file has not been made yet
        words_guessed_label = Label(text=f"Words guessed: {score}/100", font=("Ariel", 24, "bold"))
        words_guessed_label.place(x=350, y=50)
    else:
        score = score + 1 # Updates stored score by adding another point for correct guess
        words_guessed_label = Label(text=f"Words guessed: {score}/100", font=("Ariel", 24, "bold"))
        words_guessed_label.place(x=350, y=50)
    finally:
        with open("score.txt","w") as file:
            file.write(str(score))
    Canvas1.itemconfigure(photo_on_canvas, image=Card_Front)

    dict_for_french_word = select_random_word()
    random_number=random.randint(0,len(dict_for_french_word)-1)
    french_word=dict_for_french_word[random_number]["French"]
    english_word=dict_for_french_word[random_number]["English"]

    Label1 = Label(text="French", font=("Ariel", 40, "italic"), background="white")
    Label1.place(x=400, y=150)
    Label2 = Label(text=french_word, font=("Ariel", 60, "bold"), background="white")
    Label2.place(x=400, y=263)

    new_list=[d for d in dict_for_french_word if d["French"]!=french_word] # List comprehension to access list of dictionaries which does not contain the currently displayed word
    # We are doing this to save the "not-guessed" words in a separate file
    df=pandas.DataFrame(new_list)
    df.to_csv("words_to_learn.csv",index=False)

    disable_tick_button()
    disable_cross_button()
    change(Label1, Label2, english_word) # Switches to English card after 3 seconds

def show_new_card_only():
    Canvas1.itemconfigure(photo_on_canvas, image=Card_Front)
    dict_for_french_word = select_random_word()
    random_number = random.randint(0, len(dict_for_french_word) - 1)
    french_word = dict_for_french_word[random_number]["French"]
    english_word = dict_for_french_word[random_number]["English"]
    Label1 = Label(text="French", font=("Ariel", 40, "italic"), background="white")
    Label1.place(x=400, y=150)
    Label2 = Label(text=french_word, font=("Ariel", 60, "bold"), background="white")
    Label2.place(x=400, y=263)
    disable_tick_button()
    disable_cross_button()
    change(Label1, Label2, english_word)
#--------------------- AESTHETICS WINDOW---------------------
Window=Tk()
Window.title("Flashy")
Window.minsize(height=720,width=1000)
Window.configure(background=BACKGROUND_COLOR,pady=50)

#---------------------- CANVAS SETUP---------------------
Canvas1=Canvas(Window, height=526, width=800,background=BACKGROUND_COLOR,highlightthickness=0)
Card_Front=PhotoImage(file="images/card_front.png")
photo_on_canvas=Canvas1.create_image(400, 263, image=Card_Front)
Canvas1.pack()

Card_Back=PhotoImage(file="images/card_back.png")

#-------------------- BUTTONS + IMAGES------------------
start_button=Button(text="Start", font=("Ariel",40,"bold"), command=start_game)
start_button.place(x=400,y=350)
intro_label=Label(text="Welcome to the flashcard game for learning french!",font=("Georgia",24,"normal"))
intro_label.place(x=130,y=150)

Tick_mark_image=PhotoImage(file="images/right.png")
Tick_mark_button=Button(image=Tick_mark_image,highlightthickness=0,command=store_data_and_show_new_card)
Tick_mark_button.place(x=200,y=510)

Cross_mark_image=PhotoImage(file="images/wrong.png")
Cross_mark_button=Button(image=Cross_mark_image,highlightthickness=0,command=show_new_card_only)
Cross_mark_button.place(x=655,y=510)

disable_tick_button()
disable_cross_button()

Window.mainloop()

