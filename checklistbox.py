# Based on code from https://stackoverflow.com/questions/50398649/python-tkinter-tk-support-checklist-box

from typing import Dict

import tkinter as tk

class ChecklistBox(tk.Frame):
    def __init__(self, parent, choices, selected, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self._entries = {}
        bg = self.cget("background")
        for choice in choices:
            self._entries[choice] = tk.StringVar(value=choice if choice in selected else "")
            cb = tk.Checkbutton(self, var=self._entries[choice], text=choice,
                                onvalue=choice, offvalue="",
                                anchor="w", width=20, background=bg,
                                relief="flat", highlightthickness=0, font=tk.Label().cget("font")
            )
            cb.pack(side="top", fill="x", anchor="w")

    @property
    def entries(self) -> Dict[str, bool]:
        return self._entries

    def getCheckedItems(self):
        return [value for key, value in self._entries if value]
