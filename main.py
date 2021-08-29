from tkinter import *
from random import choice
import pandas as pd

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
# word_pair = {}
current_card = {}
try:
    data = pd.read_csv("data/words_to_learn.csv")
    word_list = [{row.French: row.English} for index, row in data.iterrows()]
except FileNotFoundError:
    # data = pd.read_csv("data/french_words.csv")
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
# finally:
# to_learn = data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- MECHANISM ------------------------------- #
def next_card():
    # global word_pair
    # word_pair = choice(word_list)
    # fr = list(word_pair.keys())[0]
    global current_card, timer
    window.after_cancel(timer)
    current_card = choice(to_learn)
    fr = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=fr, fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    timer = window.after(3000, func=flip_card)


def flip_card():
    # global word_pair
    # word_pair = choice(word_list)
    # en = list(word_pair.values())[0]
    global current_card
    current_card = choice(to_learn)
    en = current_card["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=en, fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


def known_card():
    to_learn.remove(current_card)
    df = pd.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=flip_card)
# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
# Buttons
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=known_card)
known_button.grid(row=1, column=0)
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=1)

next_card()

window.mainloop()
