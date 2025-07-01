import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.title("AI Image Generator App (By Hemanta Ghosh)")

st.write("Enter a prompt and click 'Generate' to create an image")

prompt = st.text_input("Enter your image prompt: ")

API_KEY = "AIzaSyDd3JZ68VJsbjGtR7Ri9azoIbK4szySwcQ"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent"

if st.button("Generate"):
    if prompt:
        try:
            headers = {
                "x-goog-api-key": API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "contents": [{
                    "parts": [
                        {"text": prompt}
                    ]
                }],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
            }
            response = requests.post(ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            # Find the image part in the response
            image_data = None
            for part in result["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    image_data = part["inlineData"]["data"]
                    break
            if image_data:
                img_bytes = base64.b64decode(image_data)
                img = Image.open(BytesIO(img_bytes))
                st.image(img, caption="Your image", use_column_width=True)
            else:
                st.error("No image was generated. Try a different prompt.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a prompt to generate an image.")
         





        
        