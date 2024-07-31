import cv2

def apply_gaussian_blur(image, kernel_size=(5, 5)):
    return cv2.GaussianBlur(image, kernel_size, 0)

def apply_median_blur(image, ksize=5):
    return cv2.medianBlur(image, ksize)