import streamlit as st

st.title('EcoTrack Recycling Assistant')

st.write("Welcome to EcoTrack, your smart AI-powered recycling assistant!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
if uploaded_file is not None:
    # Assuming the image is in PIL format
    from PIL import Image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("Image is uploaded. Processing will be here...")

    
