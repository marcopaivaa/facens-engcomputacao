import cv2
import numpy as np

IMG_SIZE = 10
SHAPE_SIZE = 3
FRAME_SIZE = 300


def main():
    img = np.ones((IMG_SIZE, IMG_SIZE), np.uint8)
    shape = cv2.getStructuringElement(cv2.MORPH_RECT, (SHAPE_SIZE, SHAPE_SIZE))
    print("\nOriginal:")
    print(img)
    output = cv2.erode(img, shape, borderValue=0)
    checkSquareArea(output)
    print("\nEroded:")
    print(output)
    showImg("Original", img)
    showImg("Eroded", output)
    cv2.waitKey()


def checkSquareArea(matrix):
    for i in range(1, IMG_SIZE - 1):
        for j in range(1, IMG_SIZE - 1):
            hasOne = False
            i_begin = i - int((SHAPE_SIZE/2))
            i_end = i + int((SHAPE_SIZE/2) + 1)
            j_begin = j - int((SHAPE_SIZE/2))
            j_end = j + int((SHAPE_SIZE/2) + 1)

            sub_m = matrix[i_begin:i_end, j_begin:j_end]
            for i_s in range(0, len(sub_m)):
                for j_s in range(0, len(sub_m[i_s])):
                    if(sub_m[i_s][j_s] == 1):
                        if(not hasOne):
                            hasOne = True
                        else:
                            sub_m[i_s][j_s] = 0


def showImg(name, matrix):
    img = np.ones((IMG_SIZE, IMG_SIZE, 3), np.uint8)
    matrix = matrix * 255
    for i in range(0, IMG_SIZE):
        for j in range(0, IMG_SIZE):
            img[i, j] = img[i, j] * matrix[i][j]

    img = cv2.resize(img, (FRAME_SIZE, FRAME_SIZE),
                     interpolation=cv2.INTER_NEAREST)
    img = cv2.bitwise_not(img)
    cv2.imshow(name, img)


if __name__ == "__main__":
    main()
