from PIL import Image, ImageTk
import os
import sys
import shutil
import tkinter as tk

# Function to load the next image
def next_image():
    global index
    index = (index + 1) % len(image_list)
    load_image()

# Function to load the previous image
def prev_image():
    global index
    index = (index - 1) % len(image_list)
    load_image()

# Function to rotate the current image 90 degrees clockwise
def rotate_clockwise():
    global image_list, index
    image_path = image_list[index]
    image = Image.open(image_path)
    image = image.transpose(Image.ROTATE_90)
    image.save(image_path)
    load_image()

# Function to rotate the current image 90 degrees counterclockwise
def rotate_counterclockwise():
    global image_list, index
    image_path = image_list[index]
    image = Image.open(image_path)
    image = image.transpose(Image.ROTATE_270)
    image.save(image_path)
    load_image()

# Function to load the current image and its previews
def load_image():
    global image_list, index, image_label, prev_label, next_label, sequence_label
    image = Image.open(image_list[index])
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

    # Only display the preview label for the previous image if it exists
    if index > 0:
        prev_image = Image.open(image_list[index-1])
        prev_image.thumbnail((prev_size, prev_size))
        prev_photo = ImageTk.PhotoImage(prev_image)
        prev_label.config(image=prev_photo)
        prev_label.image = prev_photo
    else:
        prev_label.config(image='')
        
    # Only display the preview label for the next image if it exists
    if index < len(image_list)-1:
        next_image = Image.open(image_list[index+1])
        next_image.thumbnail((prev_size, prev_size))
        next_photo = ImageTk.PhotoImage(next_image)
        next_label.config(image=next_photo)
        next_label.image = next_photo
    else:
        next_label.config(image='')

    # Add the sequence number and total number, and the image file name as a label above the image
    sequence_text = f"{index+1} of {len(image_list)}, name: {os.path.basename(image_list[index])}"
    sequence_label.destroy()
    sequence_label = tk.Label(window, text=sequence_text, bg = "light green", font=("Arial", 12), )
    sequence_label.config(text=sequence_text)

    # update the position of the label based on the current text
    sequence_label.update_idletasks()  # ensure that the label has been fully rendered
    label_width = sequence_label.winfo_reqwidth()
    label_height = sequence_label.winfo_reqheight()
    x_pos = int(window_width * 0.5 - label_width / 2)
    y_pos = int(window_height * 0.05)
    sequence_label.place(x=x_pos, y=y_pos)
    
    # Adjust the size and placement of the image label and preview labels
    image_width, image_height = image.size
    image_label_width = int(window_width * 0.8)
    image_label_height = int(window_height * 0.8)
    prev_label_width = next_label_width = int(window_width * 0.1)
    prev_label_height = next_label_height = int(window_height * 0.1)
    image_label.config(width=image_label_width, height=image_label_height)
    prev_label.place(x=0, y=int(window_height * 0.1))
    next_label.place(x=int(window_width * 0.9), y=int(window_height * 0.1))
    if image_width > image_height:
        image = image.resize((image_label_width, int(image_label_width * image_height / image_width)))
    else:
        image = image.resize((int(image_label_height * image_width / image_height), image_label_height))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
    image_label.place(x=int(window_width * 0.1), y=int(window_height * 0.1))

# Function to move the image at the given index to the specified folder
def move_image_to_folder(folder_name, index):
    global image_list
    image_path = image_list[index]
    folder_path = os.path.join(os.path.dirname(image_path), folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    new_path = os.path.join(folder_path, os.path.basename(image_path))
    shutil.move(image_path, new_path)
    image_list.pop(index)
    if index == len(image_list):
        index = 0
    load_image()

# Load the list of images in the folder specified in the command-line argument
if len(sys.argv) < 2:
    print('Usage: python image_viewer.py <folder_path>')
    sys.exit(1)

folder_path = sys.argv[1]
if not os.path.isdir(folder_path):
    print(f'{folder_path} is not a directory')
    sys.exit(1)

image_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.jpg') or file.endswith('.png')]

# Set the index to 0
index = 0

# Create a window and add the image label and preview labels
window = tk.Tk()
window_width = window.winfo_screenwidth()
window_height = window.winfo_screenheight()
window.geometry("%dx%d" % (window_width, window_height))
prev_size = int(min(window_width, window_height) * 0.1)
image_label = tk.Label(window)
prev_label = tk.Label(window)
next_label = tk.Label(window)
sequence_label = tk.Label(window)
prev_label.pack()
image_label.pack()
next_label.pack()

# Read mapping from file
with open('mapping.txt', 'r') as f:
    mapping = {}
    for line in f:
        key, folder = line.strip().split(':')
        mapping[key] = folder

# Bind keys to functions dynamically based on mapping
for key, folder in mapping.items():
    window.bind(key, lambda event, folder=folder: move_image_to_folder(folder, index))

# Bind the left and right arrow keys to the next and previous image functions
window.bind('<Left>', lambda event: prev_image())
window.bind('<Right>', lambda event: next_image())
window.bind('<Up>', lambda event: rotate_clockwise())
window.bind('<Down>', lambda event: rotate_counterclockwise())

# Load the first image
load_image()

# Start the event loop
window.mainloop()