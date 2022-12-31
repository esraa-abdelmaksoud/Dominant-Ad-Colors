from dominants import *

path = input("Please enter the folder path. \n")
multiple = input("Process all images in path? [y/n] \n")

if multiple == "y" or multiple == "Y":
    process_multiple_imgs(path)
elif multiple == "n" or multiple == "N":
    file = input("Please enter full file name with the extension. \n")
    _, hex_rgb = process_single_img(path, file)
    print(hex_rgb)
else:
    raise ValueError("Please use y for multiple images and n for single images.")

print("Output successfully saved on the same image path.")

