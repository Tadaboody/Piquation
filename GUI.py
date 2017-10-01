from extractor import *
import Tkinter as tk  # python 2
import tkFont as tkfont  # python 2
from tkFileDialog import askopenfilename, asksaveasfilename
from tkMessageBox import askquestion
import cv2
import Inputs
from PiquationUtil import solve_equation

global_image = None


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, EquationPage, ResourcePage, ResultsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name, param=None):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.on_appear(param)


class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def switch_page_to(self, page_name, param):
        self.controller.show_frame(page_name, param)

    def on_appear(self, param):
        pass


class StartPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="From Source",
                            command=self.pick_image_from_source)
        button2 = tk.Button(self, text="Webcam",
                            command=self.pick_image_from_camera)
        button1.pack()
        button2.pack()
        self.filename = ""

    def pick_image_from_source(self):
        self.filename = askopenfilename(title="Select image",
                                        filetypes=[("Image Files", ("*.jpg", "*.png"))])
        # self.filename = askopenfilename(initialdir="/", title="Select global_image")
        if self.filename != "":
            image = Image(self.filename)
            self.use_image(image)

    def pick_image_from_camera(self):
        retake = 'yes'
        while retake == 'yes':
            image = Inputs.take_pic()
            retake = askquestion("Retake", "Retake Picture?")
        source = "Source/webcam.png"
        if askquestion("save", "Would you like to save this image?") == 'yes':
            source = asksaveasfilename(filetypes=[("Png File", "*.png")])
        cv2.imwrite(source.strip(".png") + ".png", image)
        cv2.destroyWindow("Camera")
        self.use_image(Image(source))

    def use_image(self, image):
        global global_image
        r = cv2.selectROI(img=image.color_image, showCrosshair=False)
        cv2.destroyAllWindows()
        image.crop(r)
        image.draw_components()
        image.imshow()
        global_image = image
        next_page = askquestion("Intent", "Is the picture an equation?")
        print next_page
        if next_page == 'yes':
            self.controller.show_frame("EquationPage", image)
        else:
            self.controller.show_frame("ResourcePage", image)

            # imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]


class ResourcePage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.image = global_image
        self.entry = tk.Entry(self)
        self.entry.pack()
        label = tk.Label(self, text="What character to save as?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Save Resources", command=self.save_resources)
        button.pack()

    def on_appear(self, image):
        global global_image
        self.image = ResourceImage.from_image(image)

    def save_resources(self):
        self.image.save_resources(self.entry.get())
        self.switch_page_to("StartPage", None)


class EquationPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.image = global_image
        self.entry = tk.Entry(self)
        label = tk.Label(self, text="Please Correct The equation:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Equation is correct", command=self.fix_equation)
        button.pack()
        button2 = tk.Button(self, text="Components are wrong", command=self.fix_components)

    def fix_components(self):
        pass

    def on_appear(self, image):
        self.image = EquationImage.from_image(image)
        self.image.label_components()
        self.image.imshow()
        self.entry.insert(0, self.image.equation_string())
        self.entry.update()
        self.entry.pack()

    def fix_equation(self):
        if askquestion("Save", "Add to resources?") == 'yes':
            print self.entry.get()
            self.image.correct_string(self.entry.get())
        self.switch_page_to("ResultsPage", self.entry.get())


class ResultsPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.result = ""

    def on_appear(self, string):
        label = tk.Label(self, text=solve_equation(string.lower()))
        label.pack(side="top", fill="x", pady=10)


app = SampleApp()
app.mainloop()
