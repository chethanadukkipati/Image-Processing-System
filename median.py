import numpy as np

class median:
    def median(self,inp_img, str_ele, size):
        median_img = np.zeros(inp_img)
        struct_element = str_ele
        window = [size * size]
        struct_center_x = int(size / 2)
        struct_center_y = int(size / 2)
        width, height = inp_img.shape
        for x in range(struct_center_x, (width - struct_center_x)):
            for y in range(struct_center_y, (height - struct_center_y)):
                i = 0
                for fx in range(0, size):
                    for fy in range(0,size):
                        window[i] = inp_img[x + fx - struct_center_x][y + fy -struct_center_y]
                        i = i + 1
                sorted_window = window.sort()
                median_img[x][y] = sorted_window[(size * size)/2]
        return median_img



