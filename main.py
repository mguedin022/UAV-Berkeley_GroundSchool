import cv2
image = cv2.imread('hendrix.jpg')


if image is None:
    print("Couldn't find the image — check the file name and that it's in the same folder.")
else:
    cv2.namedWindow('My Image', cv2.WINDOW_NORMAL)  # makes it resizable
    cv2.resizeWindow('My Image', 800, 600)  # width, height in pixels
    cv2.imshow('My Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
