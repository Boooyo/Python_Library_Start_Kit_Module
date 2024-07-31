import cv2

def read_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f'이미지를 찾을 수 없습니다: {image_path}')
    return image

def save_image(image, output_path):
    cv2.imwrite(output_path, image)