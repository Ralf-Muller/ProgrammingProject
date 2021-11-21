# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 12:21:39 2021

@author: Rachel
"""

import tkinter as tk
from tkinter import ttk


class ChooseStock:
    def __init__(self, master):
        self.master = master

        master.title("Stock Analyser")
        
        master.geometry('660x400')
        
        self.heading_font = ("Lato", 12, "bold")
        self.button_font = ("Lato", 11)
        self.text_font = ("Lato", 11)
        

        
        self.greet = tk.Label(master, text="Welcome to the Stocks Analyser.", font = self.heading_font)
        self.greet.grid(row=1,column=2)

        self.find = tk.Button(master, width = 20, text="Find Company Symbol", font = self.button_font).grid(row=2,column=2)

        self.enter = tk.Button(master, width = 20, text="Enter Company Symbol", font = self.button_font).grid(row=3,column=2)
        
        self.h_sep = ttk.Separator(master, orient='horizontal').grid(row=6, column = 0, columnspan = 5,sticky= 'we', pady=10,padx=10)

        self.heading_1 = tk.Label(master, text="Descriptive Analytics", font = self.heading_font).grid(row=8,column=1, pady=10, padx=10)
        
        self.descr = tk.Button(master, width = 20, text="Company Description", font = self.button_font).grid(row=9,column=1,pady=10,padx=10)

        self.v_sep = ttk.Separator(master,orient='vertical').grid(row=7,column=2,rowspan=100,sticky='ns')

        self.heading_2 = tk.Label(master, text="Predictive Analytics", font = self.heading_font).grid(row=8,column=3)
        self.ols = tk.Button(master, width = 20, text="OLS", font=self.button_font).grid(row=9,column=3)

if __name__ == "__main__":
    root = tk.Tk()
    ChooseStock(root)
    root.mainloop()