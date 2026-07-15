import streamlit as st
import requests
import random
from urllib.parse import quote


# Page Configuration

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 AI Image Studio")



# Sidebar

st.sidebar.header("⚙️ Settings")

art_style = st.sidebar.selectbox(
    "🎭 Select Art Style",
    [
        "Photorealistic",
        "Anime",
        "Vintage Victorian",
        "Sketch",
        "3D Render",
        "Cyberpunk",
        "Fantasy",
        "Watercolor",
        "Oil Painting",
        "Pixar Style"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)


# Task 3 - Magic Enhance

magic_enhance = st.sidebar.checkbox(
    "✨ Enable Magic Enhance"
)

st.sidebar.markdown("---")



# Prompt Input

user_prompt = st.text_area(
    "Describe your image",
    placeholder="Example: A futuristic city at sunset"
)


# Task 4 - Surprise Prompts

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon drinking coffee in Paris",
    "A floating castle above the clouds",
    "A futuristic underwater city with glowing whales"
]

# Buttons

col1, col2 = st.columns(2)

with col1:
    generate = st.button("🚀 Generate Image")

with col2:
    surprise = st.button("🎲 Surprise Me!")

# If Surprise Me clicked
if surprise:
    user_prompt = random.choice(surprise_prompts)
    generate = True
    st.success(f"🎲 Surprise Prompt:\n\n{user_prompt}")


# Generate Image

if generate:

    if user_prompt.strip() == "":
        st.warning("Please enter a prompt.")
        st.stop()

    with st.spinner("Generating your masterpiece..."):

        # Base Prompt
        full_prompt = f"{user_prompt}, high quality, {art_style}"

        # Task 3
        if magic_enhance:
            full_prompt += (
                ", masterpiece,"
                " 8k resolution,"
                " highly detailed,"
                " trending on artstation,"
                " unreal engine 5 render"
            )

        encoded_prompt = quote(full_prompt)

        
        # Task 1
        # Width & Height Parameters
        
        url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width={width}&height={height}"
        )

        try:

            response = requests.get(url, timeout=90)

            if response.status_code == 200:

                st.success("✅ Image Generated Successfully!")

                st.image(
                    response.content,
                    caption=full_prompt,
                    use_container_width=True
                )

                st.markdown("### 📋 Generation Details")

                st.write(f"🎭 Art Style: {art_style}")
                st.write(f"📐 Size: {width} × {height}")

                if magic_enhance:
                    st.success("✨ Magic Enhance Enabled")
                else:
                    st.info("Magic Enhance Disabled")

                with st.expander("Prompt Used"):
                    st.code(full_prompt)

                
                # Task 2
                # Dynamic Download Name
                
                st.download_button(
                    label="⬇ Download Image",
                    data=response.content,
                    file_name=f"{art_style.lower().replace(' ','_')}_image.png",
                    mime="image/png"
                )

            else:
                st.error(f"API Error : {response.status_code}")
                st.text(response.text)

        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")

        except requests.exceptions.ConnectionError:
            st.error("🌐 Unable to connect to Pollinations AI.")

        except Exception as e:
            st.error(f"Error : {e}")