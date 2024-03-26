from tkinter import *
from tkinter.ttk import Progressbar
from threading import Thread
import math
import fitz


class RenderPdf:
    pdf_converted_img = []

    def view_pdf(self, master, width=1200, height=600, pdf_location="", bar=True, load="after"):

        frame = Frame(master, width=width, height=height, bg="white")

        scroll_y = Scrollbar(frame, orient="vertical")
        scroll_x = Scrollbar(frame, orient="horizontal")

        scroll_x.pack(fill="x", side="bottom")
        scroll_y.pack(fill="y", side="right")

        if bar is True and load == "after":
            display_msg = Label(frame)
            display_msg.pack(pady=10)

            show_loading_bar = Progressbar(frame, orient=HORIZONTAL, length=100, mode='determinate')
            show_loading_bar.pack(side=TOP, fill=X)

        text = Text(frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, width=width,
                    height=height)
        text.pack(side="left")

        scroll_x.config(command=text.xview)
        scroll_y.config(command=text.yview)

        def render_pdf_image():
            initial_percentage = 0
            try:
                doc = fitz.open(pdf_location)
                # a
                zoom_x = 2.0
                zoom_y = 2.0
                mat = fitz.Matrix(zoom_x, zoom_y)
                # b
                for page in doc:
                    # pix = page.get_pixmap() # Use it by eliminating the code between a and b!
                    pix = page.get_pixmap(matrix=mat)  # And then you need to comment this! Rest; remains the same...
                    imgdata = pix.tobytes("ppm")
                    tkimg = PhotoImage(data=imgdata)
                    self.pdf_converted_img.append(tkimg)
                    if bar is True and load == "after":
                        initial_percentage += 1
                        percentage_view = (initial_percentage / len(doc)) * 100
                        show_loading_bar['value'] = percentage_view
                        display_msg.config(
                            text=f"Please wait while your pdf is loading {int(math.floor(percentage_view))}%")
                if bar is True and load == "after":
                    show_loading_bar.pack_forget()
                    display_msg.pack_forget()

                for i in self.pdf_converted_img:
                    text.image_create(END, image=i)
                    text.insert(END, "\n\n")
                text.configure(state="disabled")
            except Exception as e:
                print(f"An error occurred while loading the PDF: {e}")

        def start_thread():
            thread = Thread(target=render_pdf_image)
            thread.start()

        if load == "after":
            master.after(250, start_thread)
        else:
            start_thread()

        return frame


def main():
    root = Tk()
    root.geometry("700x780")
    d = RenderPdf().view_pdf(root, pdf_location="", width=50, height=200)
    # Enter the pdf_location='C:\PC\Users\User\...', if you want to use this script exclusively! Else it throws error!
    d.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
