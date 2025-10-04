import cv2
import numpy as np
import os

def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Unable to read image: {path}")
    print(f" Loaded image: {path}")
    return img

def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def denoise(img):
    return cv2.fastNlMeansDenoising(img, h=20)

def enhance_contrast(img):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    return clahe.apply(img)

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    if len(coords) == 0:
        return image
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def adaptive_binarize(img):
    return cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 35, 15
    )

def remove_shadows(img):
    dilated_img = cv2.dilate(img, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(img, bg_img)
    norm_img = cv2.normalize(diff_img, None, 0, 255, cv2.NORM_MINMAX)
    return norm_img

def preprocess_image(path):
    img = load_image(path)
    gray = to_gray(img)
    no_shadow = remove_shadows(gray)
    denoised = denoise(no_shadow)
    enhanced = enhance_contrast(denoised)
    deskewed = deskew(enhanced)
    binary = adaptive_binarize(deskewed)
    output_path = os.path.join(os.path.dirname(path), "preprocessed_clean.png")
    cv2.imwrite(output_path, binary)
    print(f" Saved preprocessed image at: {output_path}")
    return output_path