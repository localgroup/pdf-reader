from tkinter import *
from tkinter import filedialog, messagebox
import pdfreader as pdf


def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        v1 = pdf.RenderPdf()
        v2 = v1.view_pdf(root, pdf_location=file_path)
        v2.grid(row=0, column=0, sticky="nsew")
    else:
        messagebox.showinfo("Info", "No PDF file selected.")


root = Tk()
root.geometry("1200x700+200+30")

open_button = Button(root, text="Open PDF", command=open_pdf, bg='seagreen')
open_button.grid(row=1, column=0, padx=10, pady=10)

quit_button = Button(root, text="Quit", command=root.destroy, bg='red')
quit_button.grid(row=1, column=3, padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
