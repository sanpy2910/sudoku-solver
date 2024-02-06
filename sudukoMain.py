import os
import cv2
import numpy as np
from tkinter import Tk, filedialog
from utlis import *
import sudukoSolver

def upload_image():
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    path_image = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    return path_image

print('Setting UP')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
model = intializePredectionModel()  # LOAD THE CNN MODEL

# Replace the fixed path with the uploaded image path
path_image = upload_image()
if path_image:
    height_img = 450
    width_img = 450

    #### 1. PREPARE THE IMAGE
    img = cv2.imread(path_image)
    img = cv2.resize(img, (width_img, height_img))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    img_blank = np.zeros((height_img, width_img, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    img_threshold = preProcess(img)

    # #### 2. FIND ALL CONTOURS
    img_contours = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    img_big_contour = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)  # DRAW ALL DETECTED CONTOURS

    #### 3. FIND THE BIGGEST CONTOUR AND USE IT AS SUDOKU
    biggest, max_area = biggestContour(contours)  # FIND THE BIGGEST CONTOUR
    print(biggest)
    if biggest.size != 0:
        biggest = reorder(biggest)
        print(biggest)
        cv2.drawContours(img_big_contour, biggest, -1, (0, 0, 255), 25)  # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]])  # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GET
        img_warp_colored = cv2.warpPerspective(img, matrix, (width_img, height_img))
        img_detected_digits = img_blank.copy()
        img_warp_colored = cv2.cvtColor(img_warp_colored, cv2.COLOR_BGR2GRAY)

        #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
        img_solved_digits = img_blank.copy()
        boxes = splitBoxes(img_warp_colored)
        print(len(boxes))
        # cv2.imshow("Sample", boxes[65])
        numbers = getPredection(boxes, model)
        print(numbers)
        img_detected_digits = displayNumbers(img_detected_digits, numbers, color=(0,0,0))
        numbers = np.asarray(numbers)
        pos_array = np.where(numbers > 0, 0, 1)
        print(pos_array)

        #### 5. FIND SOLUTION OF THE BOARD
        board = np.array_split(numbers, 9)
        print(board)
        sudukoSolver.solve(board)
        print("Solved Board")
        try:
            sudukoSolver.solve(board)
        except:
            pass
        print(board)
        flat_list = []
        for sublist in board:
            for item in sublist:
                flat_list.append(item)
        solved_numbers = flat_list * pos_array
        img_solved_digits = displayNumbers(img_detected_digits, solved_numbers)

        # #### 6. OVERLAY SOLUTION
        pts2 = np.float32(biggest)  # PREPARE POINTS FOR WARP
        pts1 = np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]])  # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GET
        img_inv_warp_colored = img.copy()
        img_inv_warp_colored = cv2.warpPerspective(img_solved_digits, matrix, (width_img, height_img))
        inv_perspective = cv2.addWeighted(img_inv_warp_colored, 1, img, 0.5, 1)
        img_detected_digits = drawGrid(img_detected_digits)
        img_solved_digits = drawGrid(img_solved_digits)

        image_array = ([img,img_threshold, img_contours],
                       [img_big_contour, img_detected_digits, img_solved_digits, inv_perspective])
        #stacked_image = stackImages(image_array, 1)

        cv2.imshow('img',img)
        cv2.imshow('img_threshold',img_threshold)
        cv2.imshow('img_contours',img_contours)
        cv2.imshow('img_big_contour',img_big_contour)
        cv2.imshow('img_detected_digits',img_detected_digits)
        cv2.imshow('img_solved_digits',img_solved_digits)
        cv2.imshow('inv_perspective',inv_perspective)

    else:
        print("No Sudoku Found")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
