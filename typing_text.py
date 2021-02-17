import keyboard
import tkinter as tk



def typeText(text):
    keyboard.write(text[0].upper()+text[1:]+' ')