#################################################################################
###                                                                           ###
### Date created - Monday, Nov 11, 2019                                       ###
### Author - Aditya Dutt  <adityadutt1996@gmail.com, aditya.dutt@ufl.edu >    ###
###                                                                           ###
#################################################################################

""" 
* This library is only made to work for binary images. The goal was to detect outer
boundary and loops in handwritten word images. Using this library, all edges, outer
boundary and loops can be quickly detected in a binary image. 

* The input is binary image.

* The output is a list of loops, edges, outer boundary in the same order as mentioned.
Each of the return value is an image with the same size as input image with relevant 
points marked as foreground. 
"""

import cv2, sys
import numpy as np
from scipy.ndimage import convolve


# Find 8 connected neighbors of a point
def GetNeighbors(row, col, x, y) :

    """ This function gives 8 connected neighbors of a pixel."""

    neighbors = [ [x-1,y-1], [x-1,y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]  ]
    neighbors = [[p,q] for p,q in neighbors if p>=0 and p<row and q >=0 and q<col  ]

    return neighbors



# Find 8 connected neighbors of a point which are foreground pixels
def GetForegroundNeighbors(Im, x, y) :

    """ This function gives 8 connected neighbors of a pixel which are foreground pixels."""
    
    row, col = Im.shape
    neighbors = GetNeighbors(row, col, x, y)
    FG = [[p,q] for p,q in neighbors if Im[p][q] == 0  ]

    return FG



# Check if image is valid
def CheckImage(Im) :

    """ This function asserts if the image is valid or not."""

    if type(Im) is not np.ndarray :
        if not Im :
            print("Error! NoneType object")
            sys.exit(1)

        print("Error! Input is not ndarray")
        sys.exit(1)

    shape = Im.shape
    if len(shape) <=1 :
        print("Error! Input is a 1D array, expected 2D or 3D np.ndarray")
        sys.exit(1)       

    elif len(shape) == 3 :
        if shape[0] == 0 :
            print("Error! Image width is zero")
            sys.exit(1)       

        if shape[1] == 0 :
            print("Error! Image height is zero")
            sys.exit(1)       

        gray = cv2.cvtColor(Im, cv2.COLOR_BGR2GRAY)
        # Convert Image to Binary
        (thresh, Im) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    elif len(shape) == 2 :

        if shape[0] == 0 :
            print("Error! Image width is zero")
            sys.exit(1)       

        if shape[1] == 0 :
            print("Error! Image height is zero")
            sys.exit(1)       

        # If image is not binary
        if len(np.unique(Im)) > 2 :
                # Convert Image to Binary
                (thresh, Im) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return Im



# Detect edges in binary images
def DetectLoopsEdges(Im) :

    """ This function detects loops, edges and outer boundary in binary image in order [loops, edges, outer_boundary]."""

    Im = CheckImage(Im)

    # Pad image with background pixels from all sides(top, bottom, left and right)
    Im = 1 - Im/255
    Im = np.pad(Im, ((1, 1), (1, 1)), 'constant')
    Im = 255 - Im*255

    Im = Im.astype(np.uint8)  # Convert image to uint8 type

    ## Im --> foreground 0 and background 255 ##

    Im1 = np.copy(Im)
    row, col = Im1.shape

    # Use floodfill to fill background
    Result = cv2.floodFill(Im1, None, (col-1, row-1) , 0)

    Im1 = Result[1] # Get Output Image
    Im1 = Im1.astype(np.uint8)

    # Fill all the Loops
    BG = np.where(Im1==255)
    X = np.asarray(BG[0])
    Y = np.asarray(BG[1])
    Loops = [[x,y] for x,y in zip(X,Y) ] # Store indices of Loops as [x, y]

    # Set everyting except loops indices to 255(background)
    Im2 = np.ones((row, col)) * 255
    for i in range(len(Loops)) :
        x, y = Loops[i]
        Im2[x][y] = 0

    # Elementwise multiply original image and loops, so that loops will get filled and outer boundary can be detected.
    LoopsFilled = np.multiply(Im, Im2)

    ###### Find Boundary ######

    kernel = np.ones((3,3))
    kernel[0][0] = 0
    kernel[0][2] = 0
    kernel[2][0] = 0
    kernel[2][2] = 0

    ImNew = Im/255
    FG = convolve(ImNew, kernel)    # Convolve original image with kernel to find edges
    FG[FG>0] = 255    # Set boundary points to 255 (similar to eroding)
    Edges = FG - Im    # Subtract eroded image from original image, to get only the edges
    Edges = 255 - Edges 

    # Find Boundary
    kernel = np.ones((3,3))
    kernel[0][0] = 0
    kernel[0][2] = 0
    kernel[2][0] = 0
    kernel[2][2] = 0

    ImNew = LoopsFilled/255
    FG = convolve(ImNew, kernel)    # Convolve Loops filled image with kernel to find outer boundary
    FG[FG>0] = 255
    OuterBoundary = FG - Im
    OuterBoundary = 255 - OuterBoundary

    # Remove padding that was added at the beginning
    Loops = Im2[1:row-1, 1:col-1]
    OuterBoundary = OuterBoundary[1:row-1, 1:col-1]

    Loops = Loops.astype(np.uint8)
    Edges = Edges.astype(np.uint8)

    return [Loops, Edges, OuterBoundary]