import cv2

def DecodeQR(img_path):
    img = cv2.imread(img_path)
    detect = cv2.QRCodeDetector()
    value, *i = detect.detectAndDecode(img)
    print('-------', value)
    return value

