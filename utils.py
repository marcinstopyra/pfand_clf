from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

def crop_image(img, new_size):
    
        width, height = img.size   # Get dimensions
                
        left = (width - new_size)/2
        right = (width + new_size)/2
        top = (height - new_size)/2
        bottom = (height + new_size)/2
        cropped_img = img.crop((left, top, right, bottom))
        
        return cropped_img

    
def resize_image(img, resize_factor):    
    new_width = int(img.size[0] * resize_factor)
    new_height = int(img.size[1] * resize_factor)
#     print(f"new_width: {new_width}\nnew_height: {new_height}")
    reduced_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    return reduced_img    

    
def display_image(img):
    plt.imshow(reduced_img)
    plt.show()
    
def preprocess_images(load_dir, save_dir, ready_dir, resize_factor, new_size, grayscale=False):
    # iterate over files in
    # that directory
    for i, filename in enumerate(os.listdir(load_dir)):
        f = os.path.join(load_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
    #         print(f)
            # some bug
            if f == load_dir + "\desktop.ini":
                continue
                
            img = Image.open(f)
            # rotate image if needed
            width, height = img.size
            if height < width:
                img = img.rotate(angle=-90, 
                                 expand=True)
            if grayscale == True:
                img = ImageOps.grayscale(img)
            img = resize_image(img, resize_factor)
            img = crop_image(img, new_size)        
            img.save(save_dir + "img" + str(f[-20:-4]) + ".png")
        
            # move the raw image file to ready directory
            shutil.move(f, ready_dir)