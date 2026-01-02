import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64




st.set_page_config(
    page_title="Home",
    layout="wide",   # <- this makes it full-width
    initial_sidebar_state="expanded"  # optional
)

st.title(" 🤺 Head2Head PFA Rankings Dashboard")




#WE
# Load the image
img_we = Image.open("pages/images/womens_epee.jpg")
# Create a drawing context
draw = ImageDraw.Draw(img_we)

# Choose font (you may need to install a TTF font)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
except:
    font = ImageFont.load_default()

# Text and position
text = "© UAAP Season 87 Media Team"
width, height = img_we.size
x = 10  # pixels from left
y = height - 1350  # pixels from bottom

# Draw text
draw.text((x, y), text, font=font, fill=(255, 255, 255)) 

#ME
# Load the image
img_me = Image.open("pages/images/mens_epee.jpg")
# Create a drawing context
draw = ImageDraw.Draw(img_me)

# Choose font (you may need to install a TTF font)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 92)
except:
    font = ImageFont.load_default()

# Text and position
text = "© Brandon Deichmann"
width, height = img_we.size
x = 40  # pixels from left
y = height - 1350  # pixels from bottom

# Draw text
draw.text((x, y), text, font=font, fill=(255, 255, 255)) 

#MF
# Load the image
img_mf = Image.open("pages/images/mens_foil.jpg")
# Create a drawing context
draw = ImageDraw.Draw(img_mf)

# Choose font (you may need to install a TTF font)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 72)
except:
    font = ImageFont.load_default()

# Text and position
text = "© Brandon Deichmann"
width, height = img_we.size
x = 40  # pixels from left
y = height - 1370  # pixels from bottom

# Draw text
draw.text((x, y), text, font=font, fill=(255, 255, 255)) 



col1, col2, col3 = st.columns(3)

# ---------- Column 1: Women's Epee ----------
with col1:
    st.image(img_we, use_container_width=True)
    if st.button("Women's Epee", use_container_width=True):
        st.switch_page("pages/01_Women's_Epee.py")

# ---------- Column 2: Men's Epee ----------
with col2:
    st.image(img_me, use_container_width=True)
    if st.button("Men's Epee", use_container_width=True):
        st.switch_page("pages/02_Men's_Epee.py")

# ---------- Column 3: Men's Foil ----------
with col3:
    st.image(img_mf, use_container_width=True)
    if st.button("Men's Foil", use_container_width=True):
        st.switch_page("pages/03_Men's_Foil.py")
        




# ---------- Footer ----------


def get_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
github_base64 = get_base64_image("pages/images/GitHub_Lockup_Light.png")


st.markdown(
    "<div style='text-align: center; margin-top:20px;'>"
    "<small style='color: white; font-size:16px;'>Made by Daniel Canlas | BS Statistics, University of the Philippines Diliman</small><br>"
    "<a href='https://www.linkedin.com/in/danielkarlocanlas' target='_blank'>"
    "<img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='28' style='margin:8px;'></a>"
    f"<a href='https://github.com/dafencer' target='_blank'>"
    f"<img src='data:image/png;base64,{github_base64}' width='70' style='margin:5px;'></a>"
    "</div>",
    unsafe_allow_html=True
)







