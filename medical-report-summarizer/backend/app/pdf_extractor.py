import pdfplumber
import logging
from typing import Optional

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

if __name__ == "__main__":
    # For testing
    import sys
    if len(sys.argv) > 1:
        text = extract_text_from_pdf(sys.argv[1])
        if text:
            print(text[:500])  # Print first 500 chars
        else:
            print("Failed to extract text")
    else:
        print("Usage: python pdf_extractor.py <pdf_path>")
