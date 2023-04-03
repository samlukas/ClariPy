"""
CSC111 Winter 2023 Project: ClariPy

This module contains the visualizer for the project
"""
import tkinter as tk
from tkinter import filedialog
import visualizer


def pick_file() -> None:
    """
    Prompts the user to select a file and runs the corresponding visualizers based on if the file is a python file
    or a text file
    """
    try:
        p = filedialog.askopenfilename(
            initialdir='/',
            title='Select file',
            filetypes=(('python files', '*.py'), ('txt files', '*.txt'), ('all files', '*.*'))
        )
        if '.py' in p:
            visualizer.python_to_english(p)
        else:
            visualizer.english_to_python(p)
    except FileNotFoundError:
        print('Please select a valid file')
    except UnicodeDecodeError:
        print('Please select a valid file type, either .py or a text file')


window = tk.Tk()
window.title('ClariPy')
window.geometry('200x50')
pick_file()

btn = tk.Button(window, text='Pick a New File', command=lambda: pick_file())
btn_close = tk.Button(window, text='Quit', command=lambda: window.destroy())
btn.pack()
btn_close.pack()

window.mainloop()
