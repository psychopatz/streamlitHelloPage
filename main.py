import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import os

st.set_page_config(layout="wide", page_title="Patrick Oliver Bustamante",page_icon="🥴")


st.markdown("""
<style>
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
</style>
""", unsafe_allow_html=True)

# Function to create wavy text with larger font
def create_wavy_text(text, width, height):
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    font_size = 36
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default().font_variant(size=font_size)

    lines = text.split('\n')
    total_height = len(lines) * (font_size + 10)

    start_y = (height - total_height) // 2

    for i, line in enumerate(lines):
        line_width = draw.textlength(line, font=font)
        
        for j, char in enumerate(line):
            x = (width - line_width) // 2 + draw.textlength(line[:j], font=font)
            y = start_y + i * (font_size + 10) + int(np.sin((time.time() * 5 + j) / 2) * 5)
            draw.text((x, y), char, font=font, fill=(255, 255, 255, 255))

    return image

# Function to load images
def load_images(folder_path):
    images = []
    for filename in ['img1.jpg', 'img2.jpg']:  
        img_path = os.path.join(folder_path, filename)
        if os.path.exists(img_path):
            img = Image.open(img_path)
            images.append(img)
        else:
            st.error(f"Image not found: {img_path}")
    return images

# Function to create combined image with animation and text
def create_combined_image(anim_img, text_img):
    combined = Image.new('RGBA', (text_img.width, text_img.height + anim_img.height))
    combined.paste(anim_img, (0, 0))
    combined.paste(text_img, (0, anim_img.height), mask=text_img)
    return combined

def play_music():
    audio_file = open("sfx.mp3", "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/ogg",loop=True, autoplay=True)

# Main app
def main():
    # Load images
    img_folder = 'img'  
    images = load_images(img_folder)
    
    if not images:
        st.error("No images found. Please check the 'img' folder.")
        return

    # Create placeholders
    combined_placeholder = st.empty()

    width, height = 900, 500
    text_height = 300 
    text = """Hello! My name is Patrick Oliver Bustamante
I like Peanuts and Youtube
Nice to Meet You!!!
"""

    frame = 0
    play_music()
    while True:
        # Create wavy text
        text_image = create_wavy_text(text, width, text_height)
        
        # Select current animation frame
        anim_image = images[frame % len(images)]
        anim_image = anim_image.resize((width, height - text_height))
        
        # Combine animation and text
        combined_image = create_combined_image(anim_image, text_image)
        
        # Display combined image
        combined_placeholder.image(combined_image, use_column_width=True)
       
        # Wait a short time before updating
        time.sleep(0.4)  # Adjust this value to change animation speed
        
        frame += 1

if __name__ == "__main__":
    main()