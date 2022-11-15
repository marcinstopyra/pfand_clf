from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

def display_image(img):
    """
    args:
        img
    """
    
    plt.imshow(img)
    plt.show()


def normalize_size(img_size, default_raw_size=[6000, 8000]):
    """ Normalizes size so that the ratio is the same as of the photos used in training dataset
    ---
    args:
        img_size:            current image size
        default_raw_size:    image size of the raw images used in training dataset
    ---
    returns:
        new_size:    normalised size
            
    """
    goal_ratio = default_raw_size[0] / default_raw_size[1]
#     print(goal_ratio)
    
    initial_ratio = img_size[0] / img_size[1]
#     print(initial_ratio)
    
    if initial_ratio < goal_ratio:
        new_width = img_size[0]
        new_height = int(img_size[0] / goal_ratio)
        new_size = [new_width, new_height]
        # For tests
#         new_ratio = new_width / new_height
#         print(new_size)
#         print(new_ratio)
    elif initial_ratio > goal_ratio:
        new_width = int(img_size[1] * goal_ratio)
        new_height = img_size[1]
        new_size = [new_width, new_height]
        # For tests
#         new_ratio = new_width / new_height
#         print(new_size)
#         print(new_ratio)

    return new_size

def resize_image(img, new_size):
    """ Resizes an image to desired size using Antialias algorithm. NO CROPPING -> if the original ratioo is different to the new ratio the image will be squeezed
    ---
    args:
        img:        image to be resized
        new_size:   final size
    ---
    returns:
        reduced_img:  image after resizing
    """
    
    new_width = new_size[0]
    new_height = new_size[1]
    
    print(f"new_width: {new_width}\nnew_height: {new_height}")
    reduced_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    return reduced_img

def crop_image(img, cropped_size):
    """ Crops image to desire dimension
    ---
    args:
        img:            image to be cropped
        cropped_size:   image size ater cropping
    ---
    returns:
        cropped_img
    """
    
    # check if the final cropped size is just int (square image)
    if type(cropped_size) == int:
        cropped_size = [cropped_size, cropped_size]
    
    width, height = img.size   # Get dimensions
            
    left = (width - cropped_size[0])/2
    right = (width + cropped_size[0])/2
    top = (height - cropped_size[1])/2
    bottom = (height + cropped_size[1])/2
    cropped_img = img.crop((left, top, right, bottom))
    
    return cropped_img



def preprocess_image(img, 
                      resize_factor=0.1, 
                      cropped_size=200, 
                      grayscale=False, 
                      default_raw_size=[6000, 8000]):
    """ Prepares image
    1. Rotates if needed (the image has to be vertical  
    2. Changes color to grayscale if needed
    3. Normalizes size so that the aspect ratio is the same as samples used in training datset (done by cropping one of the dimensions)  
    4. resizes image to lower resolution (by given resize_factor)  
    5. Crops image to final square containing only the needed object  
    ---
    args:
        img:                 image to be preprocessed
        resize_factor:       default=0.1, the resize factor of the resolution 
        cropped_size:        default=200, the dimension of the final, square sample
        grayscale:           default=False, indicates if the grayscale should be applied on the sample
        default_raw_size:    default=[6000, 8000],the size of the raw images used in the training dataset, 
                             used for reproduction of the preprocessing conditions on further samples
            
    ---
    returns:
        img:   preprocessed image
    """

    # rotate image if needed
    width, height = img.size
    if height < width:
        img = img.rotate(angle=-90, 
                         expand=True)
        width, height = height, width
    
    
#     display_image(img)

    if grayscale == True:
        img = ImageOps.grayscale(img)
    
    
    if [width, height] != default_raw_size:
        normalised_size = normalize_size([width, height], default_raw_size=default_raw_size)
        img = crop_image(img, cropped_size=normalised_size)
#         display_image(img)

    final_size = [int(default_raw_size[0]*resize_factor), int(default_raw_size[1]*resize_factor)]
    
    img = resize_image(img, new_size=final_size)
#     display_image(img)

    img = crop_image(img, cropped_size)  
    
    return img

def preprocess_images(load_dir, 
                       save_dir, 
                       ready_dir, 
                       resize_factor=0.1,
                       final_size=200,
                       default_raw_size=[6000,8000],
                       grayscale=False):
    """ Preprocess all images from given directory(load_dir), saves them in proper directory (save_dir), move ready raw images to backup directory (ready_dir).
    ---
    args:
        load_dir:    directory with raw images to be preprocessed
        save_dir:    target directory for ready preprocessed images
        ready_dir:   backup directory for raw images, which are already preprocessed
        
        resize_factor:       default=0.1, the resize factor of the resolution 
        final_size:          default=200, the dimension of the final, square sample
        grayscale:           default=False, indicates if the grayscale should be applied on the sample
        default_raw_size:    default=[6000, 8000],the size of the raw images used in the training dataset, 
                             used for reproduction of the preprocessing conditions on further samples
    """
    
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
            
            print(f"width: {img.size[0]}\nheight: {img.size[1]}")
            

            img = preprocess_image(img, 
                                    resize_factor=resize_factor,
                                    cropped_size=final_size,
                                    )

            img.save(save_dir + "img" + str(f[-20:-4]) + ".png")
            
            # display_image(img)
            # move the raw image file to ready directory
            shutil.move(f, ready_dir)