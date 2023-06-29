import tkinter as tk
from tkinter import Canvas, PhotoImage
import requests
from PIL import Image, ImageTk
import io
import random

class ShoeSwiper:
    def __init__(self, data):
        self.root = tk.Tk()
        self.root.title("Shoe Swipe")
        self.data = data
        self.id = random.randint(0,len(self.data)-1)
        self.like = {}
        self.dislike = []
        self.create_widgets()
        self.load_image()
        
    def create_widgets(self):
        # Create and configure the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)
        
        # Create the logo canvas
        self.logo_canvas = tk.Canvas(self.main_frame, width=400, height=93)
        self.logo_canvas.grid(row=0, column=0, columnspan=2)
        
        # Load and display the logo image
        self.logo = PhotoImage(file="Nike Price Notifier/shoe-swipe-low-resolution-logo-black-on-transparent-background.png")
        self.logo_canvas.create_image(200, 46, image=self.logo)

        # Name of Shoe Label
        self.shoe_name = tk.Label(self.main_frame, text= self.data.loc[self.id]['Name'])
        self.shoe_name.grid(row=1, column=0, columnspan=2)

        # Create the image canvas
        self.canvas = tk.Canvas(self.main_frame, width=400, height=500, highlightthickness=0, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=2)
        
        # Create the maximum price label
        self.max_price_label = tk.Label(self.main_frame, text="Max Price: ")
        self.max_price_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
        
        # Create the current price label
        self.current_price_label = tk.Label(self.main_frame, text="Current Price: ")
        self.current_price_label.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Create the discount label (if applicable)
        self.discount_label = tk.Label(self.main_frame, text="DISCOUNT", fg="red", font=("Arial", 12, "bold"))
        self.discount_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Create the Like and Dislike buttons
        self.like_button = tk.Button(self.main_frame, text="Like", command=self.like_shoe)
        self.like_button.grid(row=5, column=0, padx=10, pady=10)
        
        self.dislike_button = tk.Button(self.main_frame, text="Dislike", command=self.dislike_shoe)
        self.dislike_button.grid(row=5, column=1, padx=10, pady=10)
        
    def like_shoe(self):
        print("Liked shoe")
        self.like[self.data.loc[self.id]['Name']] = self.data.loc[self.id]['url']
        self.data = self.data.drop(self.id)
        self.id = random.randint(0,len(self.data)-1)
        self.load_image()
        
    def dislike_shoe(self):
        print("Disliked shoe")
        self.data = self.data.drop(self.id)
        self.id = random.randint(0,len(self.data)-1)
        print(len(self.data))
        self.load_image()
        
    def run(self):
        self.root.mainloop()

    def save_liked_shoes(self):
        with open("Nike Price Notifier/liked_shoes.txt", "w") as file:
            for url in self.like:
                file.write(f'{url}: {self.like[url]}\n')

    def load_image(self):
        # Get the image URL from the entry field
        image_url = self.data.loc[self.id]['image-link']
        max_price = self.data.loc[self.id]['MaxPrice']
        current_price = self.data.loc[self.id]['CurrentPrice']

        try:
            # Fetch the image from the URL
            response = requests.get(image_url)
            image_data = response.content

            # Create a PhotoImage object from the image data
            image = Image.open(io.BytesIO(image_data))
            # image = image.resize((400, 500))  # Resize the image if needed
            photo_image = ImageTk.PhotoImage(image)

            # Clear the canvas and display the new image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
            self.canvas.image = photo_image  

            # Update the maximum price label
            self.max_price_label.configure(text=f"Max Price: {max_price}")

            # Update the current price label
            self.current_price_label.configure(text=f"Current Price: {current_price}")

            # Update the name label
            self.shoe_name.configure(text = self.data.loc[self.id]['Name'])

            # Show or hide the discount label
            if current_price < max_price:
                self.discount_label.grid()
            else:
                self.discount_label.grid_remove()

        except Exception as e:
            print("Error loading image:", str(e))

