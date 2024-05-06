import streamlit as st
import requests
from PIL import Image
import io

st.title('EcoTrack Recycling Assistant')
st.write("Welcome to EcoTrack, your smart AI-powered recycling assistant!")

# City selection dropdown
city = st.selectbox('Select your city:', ['Seattle'])

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Prepare the image to send to Flask
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)  # Important: move back to the beginning of the buffer
    image_bytes = buffer.getvalue()

    # Send the image to Flask, ensuring the name matches and including the MIME type
    try:
        response = requests.post(
            'http://127.0.0.1:5000/predict',
            files={"file": ("filename.jpg", image_bytes, "image/jpeg")}
        )

        if response.status_code == 200:
            result = response.json()
            st.write(f"Item classification: {result['class_name']}")
            st.write("Recycling Instructions:", result['recycling_instructions'])
##            st.write()
            
            if city == 'Seattle':
                st.markdown("For more information on recycling in Seattle, visit [Seattle Public Utilities](https://www.seattle.gov/utilities/your-services/collection-and-disposal/recycling).")
        else:
            st.error(f"Failed to get prediction from the server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the server: {str(e)}")
else:
    st.write("Please upload an image to proceed.")
