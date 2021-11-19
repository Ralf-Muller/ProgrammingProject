# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 17:29:36 2021

@author: Rachel
"""

#key: 7QJ0OD6RU5IEVRO4

import tkinter as tk
import requests
import numpy as np
import pandas as pd
import datetime
import stk_requests_GUI as stk

       
if __name__ == "__main__":
    root = tk.Tk()
    stk.ChooseStock(root)
    root.mainloop()

stock = stk.s_dict
