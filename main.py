from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from math import floor

'''
Instructions:
    1. Save the watermark you wish to use in the same directory main.py is. 
    2. Rename the watermark png to 'watermark.png'.
    3. Run the Program
        3a. Click on Browse Image, Browse for the png you would like to use.
        3b. Click on Watermark for the watermark to appear.
        3c. Adjust watermark size via the entry boxes up top as needed.
        3d. Click on the red APPLY WATERMARK button. 
    The file should now show up on this directory.
    ONLY SUPPORTED IMAGE TYPE IS .PNG.
'''


class Panel(Tk):
    def __init__(self):
        super(Panel, self).__init__()
        # setup window
        self.title("Image Watermarker")
        self.minsize(500, 500)
        # Make Canvas fit all the empty space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # init canvas
        self.canvas = Canvas(self, width=100, height=100)
        self.canvas.grid(row=1, column=0, sticky="nesw")

        # Buttons and their respective labels
        self.browse_image = Button(text="browse image", command=self.image_browser)
        self.browse_image.grid(column=0, row=2, sticky="w", padx=50)

        self.browse_wm = Button(text="Watermark", command=self.apply_watermark)
        self.browse_wm.grid(column=0, row=2, padx=50)

        self.merge_images_button = Button(text="APPLY WATERMARK", command=self.merge_images, background="red")
        self.merge_images_button.grid(column=0, row=2, sticky="e", padx=50)

        self.edit_wm_size = Button(text="Change watermark size", command=self.change_watermark_size)
        self.edit_wm_size.grid(column=0, row=0)

        # Entries and their labels
        self.height_label = Label(text="Height")
        self.height_label.grid(column=0, row=0, sticky="w", padx=60)

        self.wm_height = Entry(width=8)
        self.wm_height.grid(column=0, row=0, sticky="w", padx=100)

        self.width_label = Label(text="Width")
        self.width_label.grid(column=0, row=0, sticky="e", padx=100)

        self.wm_width = Entry(width=8)
        self.wm_width.grid(column=0, row=0, sticky="e", padx=50)

        # Bind Watermark image to the mouse to move it on the canvas
        self.canvas.bind('<B1-Motion>', self.move_watermark)

        # initialise variables to prevent tkinter garbage collection
        self.img = None
        self.background = None
        self.foreground = None
        self.pos_x = 0
        self.pos_y = 0
        self.watermark_this_img = None
        self.image_watermark = None
        self.img_list = []

    def image_browser(self):
        # Browse image that you would like to watermark
        self.img = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("png files", "*.png"),
                                                                                                ("all files", "*.*")))
        # Put image on canvas and set min canvas size to accommodate picture
        self.watermark_this_img = PhotoImage(file=self.img)
        pil_img = Image.open(self.img)
        self.minsize(pil_img.width + 50, pil_img.height + 50)

        if len(self.img_list) == 0:
            self.img_list.append(self.canvas.create_image(0, 0, anchor='nw', image=self.watermark_this_img))
        else:
            self.img_list[0] = self.canvas.create_image(0, 0, anchor='nw', image=self.watermark_this_img)

        # Lower img so the watermark could rest on top
        self.canvas.tag_lower(self.img_list[0])

    def apply_watermark(self):

        # Find the Dimensions of the image you would like to watermark and save to a variable.
        pil_img = Image.open(self.img)
        max_wid = pil_img.width
        max_height = pil_img.height
        pil_img.close()

        # Set the dimensions of the watermark image and make it smaller than the background image dimensions
        watermark = Image.open("watermark.png")
        if watermark.width >= max_wid:
            width = max_wid
        else:
            width = watermark.width
        if watermark.height >= max_height:
            height = max_height
        else:
            height = watermark.height

        resized = watermark.resize((width, height))
        # Add the resized image to the canvas
        self.image_watermark = ImageTk.PhotoImage(resized)
        if len(self.img_list) == 1:
            self.img_list.append(self.canvas.create_image(0, 0, anchor='nw', image=self.image_watermark))
        elif len(self.img_list) == 2:
            self.img_list[1] = self.canvas.create_image(0, 0, anchor='nw', image=self.image_watermark)
        else:
            messagebox.showinfo("Error", "Please choose an image to watermark first.")

        # insert the resized dimensions into the entry boxes at the top
        self.wm_height.delete(0, END)
        self.wm_height.insert(0, f"{height}")
        self.wm_width.delete(0, END)
        self.wm_width.insert(0, f"{width}")

    def change_watermark_size(self):
        try:
            # Get height of the entry boxes at the top
            height = int(self.wm_width.get())
            width = int(self.wm_height.get())

            watermark = Image.open("watermark.png")

            # Resize the watermark to the dimensions saved in the entry boxes at the top
            resized = watermark.resize((height, width))

            self.image_watermark = ImageTk.PhotoImage(resized)
            if len(self.img_list) == 1:
                messagebox.showinfo("Error", "Please insert a watermark first.")
            elif len(self.img_list) == 2:
                self.img_list[1] = self.canvas.create_image(0, 0, anchor='nw', image=self.image_watermark)
            else:
                messagebox.showinfo("Error", "Please choose an image to watermark first.")

            # insert the new dimensions into the top boxes
            self.wm_height.delete(0, END)
            self.wm_height.insert(0, f"{height}")
            self.wm_width.delete(0, END)
            self.wm_width.insert(0, f"{width}")

        except ValueError:
            # If no value or a string in the entry boxes, give error message.
            messagebox.showinfo("Error", "Please only insert numbers into the height and width box,"
                                         " Do not leave blank")

    def move_watermark(self, event):
        try:
            # Get height of the entry boxes at the top
            height = int(self.wm_width.get())
            width = int(self.wm_height.get())
            # Resize the watermark according to the entry boxes at the top again
            watermark = Image.open("watermark.png")
            resized = watermark.resize((height, width))
            self.image_watermark = ImageTk.PhotoImage(resized)
            # event.x returns the position of where you click on the canvas.
            self.pos_x = event.x
            self.pos_y = event.y

            if len(self.img_list) == 1:
                messagebox.showinfo("Error", "Please insert a watermark first.")
            elif len(self.img_list) == 2:
                # set pos_x and pos_y as the co-ordinates for the location of the canvas to move it around
                self.img_list[1] = self.canvas.create_image(self.pos_x, self.pos_y, image=self.image_watermark)
            else:
                messagebox.showinfo("Error", "Please choose an image to watermark first.")

        except ValueError:
            # Pass if there is a string or if the entry boxes are empty
            pass

    def merge_images(self):
        # Save images
        if self.watermark_this_img is not None and self.image_watermark is not None:
            # Open the background img
            base_image = Image.open(self.img)

            watermark_width = int(self.wm_width.get())
            watermark_height = int(self.wm_height.get())
            # Open watermark with the resizes in the entry boxes
            watermark_image = Image.open("watermark.png")
            resized_watermark_image = watermark_image.resize((watermark_width, watermark_height))

            # If position is default then don't change, but if it has been affected by co-ords then change
            if self.pos_x == 0 and self.pos_y == 0:
                x_position = self.pos_x
                y_position = self.pos_y
            else:
                x_position = self.pos_x - floor(watermark_width/2)  # Adjust this as needed
                y_position = self.pos_y - floor(watermark_height/2)  # Adjust this as needed

            # Paste the watermark over the base image
            base_image.paste(resized_watermark_image, (x_position, y_position), resized_watermark_image)

            # Save the merged image
            base_image.save("merged_image.png")


window = Panel()

window.mainloop()