from tkinter import *
from PIL import Image
import pyautogui
import pytesseract
import datetime
import pyperclip
pytesseract.pytesseract.tesseract_cmd = r'tesseract.exe'
class Application():
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        root.geometry('500x200+200+200')
        root.title('Snip To Text (V0.03)')
        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES)
        root.iconphoto(False, PhotoImage(file='icon.png'))
        self.snipButton = Button(self.menu_frame, width=20, height=2, command=self.createScreenCanvas, background="white", text='Snip', activebackground='lightgrey')
        self.snipButton.pack()

        self.snipText = Label(self.menu_frame, text='Snip to text tool.\n⚬ Will replace this text with snipped text and copy text to clipboard.\n⚬ May not be entirely accurate.\n⚬ Supports letters A-Z, all numbers, and most symbols.', height=11, justify=LEFT)
        self.snipText.pack(fill=BOTH, expand=YES)

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.picture_frame = Frame(self.master_screen)
        self.picture_frame.pack(fill=BOTH, expand=YES)
    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        im.save("snip" + ".png")
        image = pytesseract.image_to_string(Image.open('snip.png'))
        self.snipText.config(text=image)
        pyperclip.copy(image)

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        if self.start_x <= self.curX and self.start_y <= self.curY:
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        return event

    def exitScreenshotMode(self):
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        root.quit()

    def on_button_press(self, event):
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='black', width=3, fill="grey")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()