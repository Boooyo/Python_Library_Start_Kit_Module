from config.settings import INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH
from utils.image_utils import read_image, save_image
from operations.filters import apply_gaussian_blur
from operations.transformations import resize_image, rotate_image

def main():
    # 이미지 읽기
    image = read_image(INPUT_IMAGE_PATH)
    
    # 이미지 처리
    image = apply_gaussian_blur(image, kernel_size=(7, 7))
    image = resize_image(image, width=800, height=600)
    image = rotate_image(image, angle=45)
    
    # 결과 저장
    save_image(image, OUTPUT_IMAGE_PATH)

if __name__ == "__main__":
    main()
