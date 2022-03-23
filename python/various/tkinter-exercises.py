import tkinter as tk
import tkinter.messagebox as tkMessageBox

#Greeting function.
def greeting():
    tkMessageBox.showinfo(
        'Window greeting',
        'This box is a greeting from hell.'
)

#The window variable was created.
window = tk.Tk()

#text_widget is a text widget.
text_widget = tk.Label(
        text = 'This is text.',
        foreground = 'white',
        background = 'grey'
)
text_widget.pack()

#button_widget is a button widget.
button_widget = tk.Button(
        text = 'This is a button',
        foreground = 'white',
        background = 'grey',
        command = greeting
)
button_widget.pack()

#entry_widget is a entry widget.
entry_widget = tk.Entry(
        textvariable = 'One line.',
        bd = 5,
        show = '*'
)
entry_widget.pack()

#Create a loop for listen for user events.
window.mainloop()
