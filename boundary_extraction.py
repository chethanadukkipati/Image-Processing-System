import numpy as np
from erosion import *
from otsu import *
def boundary_extraction(inp_image,array,size):
    #The input image MUST be binary. So convert greyscale image to binary before passing
    inp_image=threshold(inp_image)
    boundary_image = np.zeros(inp_image)
    eroded_image = erosion(inp_image,array,size)  #Insert the name of binary erosion function here. The shape and size of structuring element should not matter.
    boundary_image = inp_image - eroded_image
    return boundary_image