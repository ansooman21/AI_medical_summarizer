import pdfplumber
import logging
import os
from typing import Optional
from PIL import Image
import pytesseract

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as string, or None if extraction failed
    """
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            logger.warning(f"No text extracted from {pdf_path}")
            return None
            
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        return None

def extract_text_from_image(image_path: str) -> Optional[str]:
    """
    Extract text from an image file using OCR.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text as string, or None if extraction failed
    """
    try:
        # Open image
        image = Image.open(image_path)
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        
        if not text.strip():
            logger.warning(f"No text extracted from image {image_path}")
            return None
            
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from image {image_path}: {str(e)}")
        return None

def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extract text from a file based on its extension.
    Supports PDF and common image formats (PNG, JPG, JPEG, TIFF, BMP).
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text as string, or None if extraction failed
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
        
    # Get file extension in lowercase
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp']:
        return extract_text_from_image(file_path)
    else:
        logger.error(f"Unsupported file type: {ext}")
        return None

if __name__ == "__main__":
    # For testing
    import sys
    if len(sys.argv) > 1:
        text = extract_text_from_file(sys.argv[1])
        if text:
            print(text[:500])  # Print first 500 chars
        else:
            print("Failed to extract text")
    else:
        print("Usage: python pdf_extractor.py <file_path>")
