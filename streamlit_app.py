import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

colors_df = load_colors()

def get_color_name(R, G, B):
    minimum = float("inf")
    cname = None
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + abs(G - int(colors_df.loc[i, "G"])) + abs(B - int(colors_df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = colors_df.loc[i, "color_name"]
    return cname

st.set_page_config(page_title="Color Detection App", layout="wide")
st.title("🎨 Color Detection from Images")
st.write("Upload an image and click anywhere to detect the color.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img = np.array(image)

    coords = streamlit_image_coordinates(image, key="color_picker")

    if coords is not None:
        x, y = coords["x"], coords["y"]
        pixel = img[int(y), int(x)]
        R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])
        cname = get_color_name(R, G, B)

        st.success(f"**Detected Color:** {cname}")
        st.write(f"**RGB Values:** R={R}, G={G}, B={B}")

        st.markdown(
            f"<div style='width:150px;height:75px;background:rgb({R},{G},{B});border:2px solid black;'></div>",
            unsafe_allow_html=True
        )
