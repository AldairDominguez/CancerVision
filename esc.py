import cv2
import os
import numpy as np
import tensorflow as tf
from keras._tf_keras.keras.applications.vgg16 import VGG16, preprocess_input
from keras._tf_keras.keras.preprocessing.image import img_to_array
from keras._tf_keras.keras.models import load_model
from datetime import datetime
from threading import Thread

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
spot_detection_model = VGG16(weights='imagenet', include_top=True)

camara_dir = './img/Camara'
if not os.path.exists(camara_dir):
    os.makedirs(camara_dir)

def detect_human_and_spot(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    humans, _ = hog.detectMultiScale(gray, winStride=(8, 8), padding=(32, 32), scale=1.05)

    input_image = cv2.resize(image, (224, 224))
    input_image = img_to_array(input_image)
    input_image = np.expand_dims(input_image, axis=0)
    input_image = preprocess_input(input_image)

    preds = spot_detection_model.predict(input_image)
    spot_detected = np.argmax(preds[0])

    return humans, spot_detected

def draw_keypoints(image):
    orb = cv2.ORB_create()
    keypoints = orb.detect(image, None)
    if keypoints:
        image_with_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=0)
    else:
        image_with_keypoints = image
    return image_with_keypoints

def capture_and_save_image(frame):
    humans, spot_detected = detect_human_and_spot(frame)
    if len(humans) > 0:
        print("Humano detectado.")
    if spot_detected:
        print("Mancha detectada.")
    for (x, y, w, h) in humans:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    frame_with_keypoints = draw_keypoints(frame)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(camara_dir, f"capture_{timestamp}.jpg")
    cv2.imwrite(image_path, frame_with_keypoints)

    print(f"Imagen guardada en {image_path}")

def adjust_camera_settings(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 150)
    cap.set(cv2.CAP_PROP_CONTRAST, 50)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    adjust_camera_settings(cap)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el cuadro.")
            break

        frame = cv2.resize(frame, (640, 480))

        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=50)

        frame_with_keypoints = draw_keypoints(frame)
        cv2.imshow('Camara', frame_with_keypoints)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            thread = Thread(target=capture_and_save_image, args=(frame,))
            thread.start()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
