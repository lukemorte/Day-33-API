# API day 32

import tkinter
import requests


def get_quote():
    pass


# code


window = tkinter.Tk()
window.title("Kanye Rest")
window.configure(padx=50, pady=50)

canvas = tkinter.Canvas(width=300, height=414)
background_img = tkinter.PhotoImage(file="background.png")
canvas.create_image(150, 207, image=background_img)
quote_text = canvas.create_text(150, 207, text="Kanye Quote goes HERE", fill="white", width=250, font=("Arial", 30, "bold"))
canvas.grid(column=0, row=0)

kanye_img = tkinter.PhotoImage(file="kanye.png")
kanyeButton = tkinter.Button(image=kanye_img, highlightthickness=0, relief="flat", command=get_quote)

kanyeButton.grid(column=0, row=1)



window.mainloop()
