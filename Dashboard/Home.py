import streamlit as st
from PIL import Image, ImageDraw, ImageFont





st.set_page_config(
    page_title="Home",
    layout="wide",   # <- this makes it full-width
    initial_sidebar_state="collapsed"  # optional
)



st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem;  /* keep this if you have a fixed footer */
    }

    header { 
        visibility: collapsed; 
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.title(" 🤺 Head-to-Head Fencing Analytics for Philippine Fencing Association Senior Rankings")

# ---------- Footer ----------


from utils import render_footer
render_footer()






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
text = "Photo by UAAP Season 87 Media Team"
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
text = "Photo by Brandon Deichmann"
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
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 90)
except:
    font = ImageFont.load_default()

# Text and position
text = "Photo by Brandon Deichmann"
width, height = img_we.size
x = 40  # pixels from left
y = height - 1370  # pixels from bottom

# Draw text
draw.text((x, y), text, font=font, fill=(255, 255, 255)) 


#WF
# Load the image
img_wf = Image.open("pages/images/womens_foil.png")
# Create a drawing context
draw = ImageDraw.Draw(img_wf)

# Choose font (you may need to install a TTF font)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 33)
except:
    font = ImageFont.load_default()

# Text and position
text = "Photo by @jannallysh on Instagram"
width, height = img_we.size
x = 10  # pixels from left
y = height - 1360  # pixels from bottom

# Draw text
draw.text((x, y), text, font=font, fill=(255, 255, 255)) 

#WS
# Load the image
img_ws = Image.open("pages/images/womens_saber.jpg")
# Create a drawing context
draw = ImageDraw.Draw(img_ws)

# Choose font (you may need to install a TTF font)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 100)
except:
    font = ImageFont.load_default()

# Text and position
text = "Photo by Brandon Deichmann"
width, height = img_we.size
x = 10  # pixels from left
y = height - 1350  # pixels from bottom

# Draw text
draw.text((x, y), text, font=font, fill=(255, 255, 255)) 

#MS
# Load the image
img_ms = Image.open("pages/images/mens_saber.jpg")
# Create a drawing context
draw = ImageDraw.Draw(img_ms)

# Choose font (you may need to install a TTF font)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 100)
except:
    font = ImageFont.load_default()

# Text and position
text = "Photo by Brandon Deichmann"
width, height = img_we.size
x = 10  # pixels from left
y = height - 1350  # pixels from bottom

# Draw text
draw.text((x, y), text, font=font, fill=(255, 255, 255)) 


# To make sure all images are same dimensions

def resize_image(img, size=(800, 500)):
    return img.resize(size, Image.LANCZOS)
TARGET_SIZE = (800, 500)

img_we = resize_image(img_we, TARGET_SIZE)
img_me = resize_image(img_me, TARGET_SIZE)
img_mf = resize_image(img_mf, TARGET_SIZE)
img_wf = resize_image(img_wf, TARGET_SIZE)
img_ws = resize_image(img_ws, TARGET_SIZE)
img_ms = resize_image(img_ms, TARGET_SIZE)

col1, col2, col3 = st.columns(3)

# ---------- Column 1: Women's Epee ----------
with col1:
    st.image(img_we, use_container_width=True)
    if st.button("Women's Epee", use_container_width=True):
        st.switch_page("pages/01_Women's_Epee.py")

# ---------- Column 2: Men's Epee ----------
with col2:
    st.image(img_wf, use_container_width=True)
    if st.button("Women's Foil", use_container_width=True):
        st.switch_page("pages/02_Women's_Foil.py")

# ---------- Column 3: Women's Saber ----------
with col3:
    st.image(img_ws, use_container_width=True)
    if st.button("Women's Saber", use_container_width=True):
        st.switch_page("pages/03_Women's_Saber.py")
        


col4, col5, col6 = st.columns(3)

# ---------- Column 4: Men's Epee ----------
with col4:
    st.image(img_me, use_container_width=True)
    if st.button("Men's Epee", use_container_width=True):
        st.switch_page("pages/04_Men's_Epee.py")
        
# ---------- Column 5: Men's Foil ----------
with col5:
    st.image(img_mf, use_container_width=True)
    if st.button("Men's Foil", use_container_width=True):
        st.switch_page("pages/05_Men's_Foil.py")
        
# ---------- Column 6: Men's Saber ----------
with col6:
    st.image(img_ms, use_container_width=True)
    if st.button("Men's Saber", use_container_width=True):
        st.switch_page("pages/06_Men's_Saber.py")







