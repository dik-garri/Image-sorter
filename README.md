## Image Sorter App

Image Sorter is a simple Python script that allows you to view and manage images in a given directory. You can navigate through the images using arrow keys and rotate them with up and down keys. You can also move images to predefined folders using custom keyboard shortcuts.

## Requirements

- Python 3.x If you do not have it installed, download and install it from the official website: https://www.python.org/downloads/
- PIL (Python Imaging Library) `pip3 install Pillow`
- tkinter `pip3 install tkinter`

## Getting Started

- Clone this repository. Download the program files from the Github repository or by using the git clone command
- Open your terminal or command prompt and navigate to the cloned repository directory.
- Run `python image_sorter.py <folder_path>` where <folder_path> is the path to the folder containing the images you want to process. For example: `python image_sorter.py C:\Users\your_username\Desktop\Pictures`

## Usage

Once the script is running, you can use the following keyboard shortcuts:

- Left Arrow: View the previous image
- Right Arrow: View the next image
- Up Arrow: Rotate the current image 90 degrees clockwise
- Down Arrow: Rotate the current image 90 degrees counterclockwise
- Custom shortcuts: Move the current image to a predefined folder. The shortcuts and their associated folders are defined in the mapping.txt file.

# Customizing Shortcuts

To customize the keyboard shortcuts, you can modify the mapping.txt file. The file contains a list of keyboard keys and their associated folders. Each line of the file should be in the format key:folder, where key is the keyboard key and folder is the name of the folder to move images to. For example:

- a: Archive
- f: Family
- d: Delete

# Limitations

The script currently only supports .jpg and .png image files.
