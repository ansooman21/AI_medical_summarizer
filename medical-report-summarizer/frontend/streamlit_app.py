import streamlit as st
import requests
import json
import os

# Configure the page
st.set_page_config(
    page_title="Medical Report Summarizer",
    page_icon="🏥",
    layout="centered"
)

# Title and description
st.title("🏥 Medical Report Summarizer")
st.markdown("""
Upload a medical PDF report or image to get a concise summary, actionable items, and identified deficiencies.
Powered by Google's Gemini AI.
""")

# File uploader - accept both PDF and image files
uploaded_file = st.file_uploader("Choose a PDF or image file", type=["pdf", "png", "jpg", "jpeg", "tiff", "tif", "bmp"])

if uploaded_file is not None:
    # Display file details
    st.write(f"**Filename:** {uploaded_file.name}")
    st.write(f"**File size:** {uploaded_file.size / 1024:.2f} KB")
    
    # Button to process
    if st.button("Analyze Report"):
        # Show a spinner while processing
        with st.spinner("Processing your medical report..."):
            try:
                # Prepare the file for upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # Send request to the backend API
                # Assuming the backend is running on localhost:8000
                response = requests.post("http://localhost:8000/upload", files=files)
                
                # Check if the request was successful
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display the results
                    st.success("Analysis complete!")
                    
                    # Summary
                    st.subheader("Summary")
                    st.write(result.get("summary", "No summary available"))
                    
                    # Action Items
                    st.subheader("Action Items (What needs to be done)")
                    action_items = result.get("action_items", [])
                    if action_items:
                        for item in action_items:
                            st.write(f"- {item}")
                    else:
                        st.write("- No specific action items identified")
                    
                    # Deficiencies
                    st.subheader("Deficiencies (What the body lacks)")
                    deficiencies = result.get("deficiencies", [])
                    if deficiencies:
                        for item in deficiencies:
                            st.write(f"- {item}")
                    else:
                        st.write("- No deficiencies identified")
                    
                else:
                    # Handle API errors
                    try:
                        error_detail = response.json().get("detail", "Unknown error")
                    except:
                        error_detail = response.text
                    st.error(f"API Error: {response.status_code} - {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend API. Please make sure the FastAPI server is running on localhost:8000.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
**Note:** This tool is for informational purposes only and should not be used as a substitute for professional medical advice.
Always consult with qualified healthcare providers for medical decisions.

**For image files:** The tool uses OCR (Optical Character Recognition) to extract text. For best results, use clear, high-resolution images of text.
""")
