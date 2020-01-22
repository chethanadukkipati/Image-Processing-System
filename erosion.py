import cv2
import numpy
import time

def erosion (image, str_ele, str_ele_shape):
    """
    THE ALGORITHM EXCPECTS BACKGROUND TO BE DARKER THAN THE FORGROUND / OBJECT \n
    perform erosion on given image with given structuring element: \n
    image: input image \n
    str_ele: numpy 1/2D array \n
    str_ele_shape: 'square' iff str ele square, positive odd dim, filled with 1 and NaN.\n
    'cross' iff str ele cross, positive odd dim, filled with 1 and NaN.\n
    leave empty otherwise. may be very slow.
    other supported str_eles: any shape/size with values(weights) between 0-1, & NaN.
    output: eroded image \n
    """

    str_ele_center_y = int(str_ele.shape[0]/2)
    str_ele_center_x = int(str_ele.shape[1]/2)

    #number of pixels the image needs to be padded
    top_padding = str_ele_center_y
    left_padding = str_ele_center_x
    bottom_padding = str_ele.shape[0] - str_ele_center_y - 1
    right_padding = str_ele.shape[1] - str_ele_center_x - 1

    #separate image into channels
    #c channels, m x n image
    #image_channels.shape() = (c,m,n)
    image_channels = cv2.split(image)
    eroded_image = numpy.copy(image)
    eroded_image_channels = numpy.copy(image_channels)

    #pad channels with NaN
    for i in range(len(image_channels)):
        image_channels[i] = numpy.pad(image_channels[i].astype(float), [(top_padding, bottom_padding), (left_padding, right_padding)], mode='constant',constant_values=(numpy.nan,))
    
    #not sure how to explain
    #some help: https://stackoverflow.com/questions/53472236/numpy-vectorize-more-efficient-for-loop/53472873#53472873
    
    for c in range(len(image_channels)):

        arr = [image_channels[c][top_padding : top_padding + image.shape[0], left_padding : left_padding + image.shape[1]]]

        #cross str_ele
        if (str_ele_shape == 'cross'):
            
            for x in range(len(str_ele)//2):
                
                arr.append(image_channels[c][top_padding + x + 1 : top_padding + x + 1 + image.shape[0], left_padding : -right_padding])
                arr.append(image_channels[c][top_padding + x - 1 : top_padding + x - 1 + image.shape[0], left_padding : -right_padding])
                arr.append(image_channels[c][top_padding : -bottom_padding, left_padding + x + 1 : left_padding + x + 1 + image.shape[1]])
                arr.append(image_channels[c][top_padding : -bottom_padding, left_padding + x - 1 : left_padding + x - 1 + image.shape[1]])

            eroded_image_channels[c] = numpy.full_like(eroded_image_channels[c], fill_value=0, dtype=numpy.uint8)
            eroded_image_channels[c][:, :] = numpy.nanmin(numpy.stack(arr,axis = 0), axis=0)

        #square
        elif(str_ele_shape == 'square'):
            if (str_ele.shape[0] > 1):
                for y in range(image.shape[0]):
                    for x in range(image.shape[1]):
                        arr.append(image_channels[c][y:y+image.shape[0],x:x+image.shape[1]])
            
            eroded_image_channels[c] = numpy.full_like(eroded_image_channels[c], fill_value=0, dtype=numpy.uint8)
            eroded_image_channels[c][:, :] = numpy.nanmin(numpy.stack(arr,axis = 0), axis=0)

        #otherwise
        else:
            for y in range(len(eroded_image_channels[c])):
                for x in range(len(eroded_image_channels[c][0])):
                    eroded_image_channels[c][y][x] = numpy.nanmin(str_ele*image_channels[c][y:y+len(str_ele),x:x+(len(str_ele[0]))])

    eroded_image = cv2.merge(eroded_image_channels)

    return (eroded_image)