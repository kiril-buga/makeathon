import streamlit as st

import cv2
import numpy as np

# if complains about cv2/libgl1 then run the following command
# sudo apt-get install libgl1-mesa-glx
def preprocess(img):
    bytes_data = np.asarray(bytearray(img.read()), dtype=np.uint8)
    img = cv2.imdecode(bytes_data, cv2.IMREAD_COLOR)
    return img

def invert(img):
    img = preprocess(img)
    inv = cv2.bitwise_not(img)
    return inv

def sketch(img):
    img = preprocess(img)
    _, sketch_img = cv2.pencilSketch(
        img, sigma_s=60, sigma_r=0.07, shade_factor=0.1
    )
    return sketch_img

def gray(img):
    img = preprocess(img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
    return gray_img

def none(img):
    img = preprocess(img)
    return img

picture = st.camera_input("First, take a picture...")

filters_to_funcs = {
    "No filter": none,
    "Grayscale": gray,
    "Invert": invert,
    "Sketch": sketch,
}
filters = st.selectbox("...and now, apply a filter!", filters_to_funcs.keys())

if picture:
    st.image(filters_to_funcs[filters](picture), channels="BGR")