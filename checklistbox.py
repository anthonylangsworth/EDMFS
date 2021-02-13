# Based on code from https://stackoverflow.com/questions/50398649/python-tkinter-tk-support-checklist-box

from typing import Dict
import tkinter as tk
import myNotebook

class ChecklistBox(tk.Frame):
    def __init__(self, parent, choices, selected, **kwargs):
        super().__init__(parent, **kwargs)

        self._entries = {}
        bg = self.cget("background")
        for choice in choices:
            self._entries[choice] = tk.IntVar(value=1 if choice in selected else 0)
            cb = myNotebook.Checkbutton(self, var=self._entries[choice], text=choice,
                                onvalue=1, offvalue=0,
                                width=20, # anchor="w", background=bg, relief="flat", highlightthickness=0, font=tk.Label().cget("font")
            )
            cb.pack(side="top", fill="x", anchor="w")

    @property
    def entries(self) -> Dict[str, bool]:
        return self._entries

    def getCheckedItems(self):
        return [value for key, value in self._entries if value]
