import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from classes import Musiksammlung, Track, Album

class MusiksammlungGUI:
    def __init__(self,root):
        self.root = root
        self.root.title("Musiksammlung Verwaltung")

        self.musiksammlung = Musiksammlung() # Musiksammlung Objekt wird erstellt
