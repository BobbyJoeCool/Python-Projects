# The module controls the UI for the Blackjack Program

import tkinter as tk
from tkinter import ttk, messagebox
import game, classes

class GUI:
    def beginGame(self, playerName, decks):
            if decks in ["1", "2", "3", "4", "5", "6"]:
                game.newGame(playerName, decks)
            else:
                messagebox.showwarning("Warning", "Number of Decks must be 1-6.")

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack!")
        self.root.geometry("+500+200")
        style = ttk.Style()
        style.theme_use("aqua")
        

        playerName = tk.StringVar()
        decks = tk.StringVar()
    

        # Create the Welcome Frame
        self.welcomeFrame = ttk.Frame(self.root)
        self.welcomeLabel = ttk.Label(self.welcomeFrame, text="""Welcome to BlackJack!
Programmed by Robert Breutzmann
as part of continued learning of Python.
    
Dealer hits until they have 17.
Dealer hits on soft 17
    
Blackjack pays 1.5x the bet (Rounded Down)."""
                                      , justify="center")
        self.nameLabel = ttk.Label(self.welcomeFrame, text="What is your Name:", justify="right")
        self.nameEntry = ttk.Entry(self.welcomeFrame, textvariable=playerName)
        self.decksLabel = ttk.Label(self.welcomeFrame, text="How many Decks do you want to play with?", justify="right")
        self.decksEntry = ttk.Entry(self.welcomeFrame, textvariable=decks)
        self.startGame = ttk.Button(self.welcomeFrame, command=lambda: self.beginGame(playerName.get(), decks.get()), text="Start Game")
        self.quit = ttk.Button(self.welcomeFrame, command=self.root.destroy, text="Quit")
        self.welcomeFrame.pack()
        self.welcomeLabel.grid(column=0, row=0, columnspan=2)
        self.nameLabel.grid(column=0, row=1)
        self.nameEntry.grid(column=1, row=1)
        self.decksLabel.grid(column=0, row=2)
        self.decksEntry.grid(column=1, row=2)
        self.startGame.grid(column=0, row=3)
        self.quit.grid(column=1, row=3)

        self.root.mainloop()

if __name__== "__main__":
    GUI()
