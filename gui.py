import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class DiscordCodeCheckerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Discord Code Checker")

        self.label = tk.Label(master, text="Output:")
        self.label.pack()

        self.output_text = ScrolledText(master, height=20, width=50)
        self.output_text.pack()

        self.check_button = tk.Button(master, text="Check Codes", command=self.check_codes)
        self.check_button.pack()

    def check_codes(self):
        # Clear previous output
        self.output_text.delete('1.0', tk.END)
        # Here you can add the logic to check codes and display the output in the GUI
        self.output_text.insert(tk.END, "This feature is not implemented yet.")

def main():
    root = tk.Tk()
    app = DiscordCodeCheckerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
