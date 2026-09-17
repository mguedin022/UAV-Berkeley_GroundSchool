import cv2
import numpy as np

image_path = 'hendrix.jpg'
image = cv2.imread(image_path)

if image is None:
    print("Couldn't find the image — check the file name and that it's in the same folder.")
    input("Press Enter to close...")
    exit()

try:
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)

    K = 4
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    labels = labels.flatten()

    h, w = image.shape[:2]

    for i in range(K):
        single_color_img = np.zeros_like(pixels)
        single_color_img[labels == i] = centers[i]
        single_color_img = single_color_img.reshape((h, w, 3)).astype(np.uint8)

        window_name = f'Color Group {i}'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 500, 500)
        cv2.imshow(window_name, single_color_img)

        mask = np.zeros((h * w), dtype=np.uint8)
        mask[labels == i] = 255
        mask = mask.reshape((h, w))

        M = cv2.moments(mask)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"Color Group {i}: center at x={cx}, y={cy}")
        else:
            print(f"Color Group {i}: no pixels found")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except Exception as e:
    print("An error occurred:", e)
    input("Press Enter to close...")