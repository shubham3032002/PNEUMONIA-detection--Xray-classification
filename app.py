import streamlit as st
import os
import torch
from torchvision.transforms import transforms
from PIL import Image
from pathlib import Path

# Prediction Function
def predict(uploaded_file):
    try:
        # Save the uploaded image temporarily
        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, "uploaded_image.jpg")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Load the model
        model_path = Path("model/model.pt")
        if not model_path.exists():
            st.error("⚠️ Model file not found. Please ensure 'model/model.pt' exists.")
            return

        model = torch.load(model_path)
        model.eval()

        # Define image transformation
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

        # Load and preprocess the image
        image = Image.open(file_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)

        # Predict
        with torch.no_grad():
            output = model(input_tensor)
            prediction = torch.argmax(output, dim=1).item()

        # Display results
        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Uploaded X-ray", use_container_width=True)  # Updated here

        with col2:
            st.markdown("### Prediction Result:")
            if prediction == 0:
                st.success("🟢 **Normal**: The X-ray appears healthy.")
            elif prediction == 1:
                st.error("🔴 **Pneumonia**: Pneumonia detected in the X-ray.")
            else:
                st.warning("⚠️ Unexpected prediction result.")

    except Exception as e:
        st.error(f"Error during prediction: {e}")

# Main Streamlit App
def main():
    st.set_page_config(
        page_title="X-ray Lung Classifier",
        page_icon="🩻",
        layout="wide",
    )

    # Header Section
    st.title("🩻 X-ray Lung Classifier")
    st.markdown("""
    This application uses a deep learning model to classify X-ray images into two categories:
    - 🟢 **Normal**
    - 🔴 **Pneumonia**

    Upload an X-ray image to get started.
    """)

    # Upload Section
    st.markdown("### Upload Your X-ray Image Below:")
    uploaded_file = st.file_uploader(
        "Choose an X-ray image (JPEG/PNG):",
        type=["jpg", "jpeg", "png"],
    )

    # Sidebar Info
    with st.sidebar:
        st.header("How it works:")
        st.markdown("""
        - Upload an X-ray image of the chest.
        - The model will analyze the image.
        - You'll get a prediction result of either:
          - 🟢 **Normal**
          - 🔴 **Pneumonia**
        """)
        st.markdown("---")
      
    # Analyze Button
    if st.button("Analyze X-ray"):
        if uploaded_file is not None:
            predict(uploaded_file)
        else:
            st.warning("⚠️ Please upload an image before clicking 'Analyze X-ray'.")

    # Footer
    st.markdown("---")
    

if __name__ == "__main__":
    main()
