import numpy
from morphology.erosion import erosion
from morphology.dilation import dilation

def binary_skeletonize (image, str_ele, str_ele_shape):
    """
    only binary images supported.
    only binary str_ele supported(1 or NaN).
    don't forget to specify str_ele_shape.
    """
    
    skeleton = numpy.full_like(image,0)
    
    #convert any binary(0-255) to
    #supported binary(0-1)
    max = numpy.max(image)
    image[image == max] = 1
    
    while(numpy.nanmax(image) != 0):
        #replace with open if you have parrallel implementation
       
        #b = NOT[OPEN(Image,str_ele)]
        a = erosion(image,str_ele,str_ele_shape)
        b = dilation(a,str_ele,str_ele_shape)
        
        #swapping 1's and 0's. (binary not).
        b = b - 1
        b[b==255] = 1
        
        #Sn = Image Λ b 
        Sn = b * image
        
        skeleton = skeleton + Sn
        
        # image = ERODE(image)
        image = a
        
    skeleton[skeleton == 1] = 255
    
    return skeleton