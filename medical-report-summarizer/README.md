# Medical Report Summarifier

An AI-powered tool to summarize medical PDF reports and images and identify actionable items and deficiencies, with a FastAPI backend and Streamlit frontend.

## Features

- Extract text from medical PDF reports and images (using OCR for images)
- Generate concise summaries using AI (Google's Gemini)
- Identify actionable items (what needs to be done)
- Detect deficiencies or missing elements in the report
- RESTful API backend for integration
- User-friendly Streamlit frontend

## Project Structure

```
medical-report-summarizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── pdf_extractor.py # PDF and image text extraction
│   │   └── summarizer.py    # AI summarization with Gemini
│   ├── requirements.txt     # Backend dependencies
│   └── .env.example         # Environment variable template
├── frontend/
│   ├── streamlit_app.py     # Streamlit frontend
│   └── requirements.txt     # Frontend dependencies
├── data/                    # Sample data directory
│   └── .gitkeep
├── .gitignore               # Git ignore rules
├── .env.example             # Root environment template (unused)
├── LICENSE                  # MIT license
└── README.md                # This file
```

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env to add your Gemini API key:
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

   **Note for image processing:** The OCR functionality requires Tesseract OCR to be installed on your system.
   - **Windows:** Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - **macOS:** `brew install tesseract`
   - **Linux:** `sudo apt-get install tesseract-ocr` or equivalent

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the Backend API

From the `backend` directory:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 2. Start the Frontend

From the `frontend` directory:
```bash
streamlit run streamlit_app.py
```

The Streamlit interface will open in your default web browser (typically at `http://localhost:8501`).

### 3. Using the Application

1. In the Streamlit interface, click "Choose a PDF or image file" and select a medical PDF report or image (PNG, JPG, JPEG, TIFF, BMP)
2. Click the "Analyze Report" button
3. Wait for the processing to complete
4. View the summary, action items, and deficiencies

## API Endpoints

### POST `/upload`
Upload a medical PDF or image file for summarization.

**Parameters:**
- `file`: The file to process (multipart/form-data)

**Response:**
```json
{
  "summary": "Concise summary of key findings",
  "action_items": ["Action item 1", "Action item 2"],
  "deficiencies": ["Deficiency 1", "Deficiency 2"]
}
```

### GET `/health`
Health check endpoint to verify the API is running.

## Example Output

```
Summary:
The patient is a 55-year-old male with hypertension and type 2 diabetes. Current medications include metformin and lisinopril. Recent labs show elevated HbA1c at 8.5% and LDL cholesterol at 130 mg/dL.

Action Items:
- Schedule follow-up appointment in 3 months
- Refer to nutritionist for diabetes management
- Consider statin therapy for cholesterol management
- Monitor blood pressure weekly at home

Deficiencies:
- No recent eye examination documented
- Missing foot examination for diabetes complications
- No documentation of physical activity levels
- No recent lipid panel (last one was 6 months ago)
```

## How It Works

1. **Frontend (Streamlit)**: User uploads a PDF or image file through the web interface
2. **Backend (FastAPI)**: 
   - Receives the uploaded file
   - For PDFs: Extracts text using pdfplumber
   - For Images: Extracts text using OCR (pytesseract + Tesseract)
   - Sends the extracted text to Google's Gemini API for analysis
   - Returns structured JSON with summary, action items, and deficiencies
3. **Frontend**: Displays the results in an easy-to-read format

## Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

You can obtain a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Dependencies

### Backend
- pdfplumber: PDF text extraction
- google-generativeai: Gemini API client
- python-dotenv: Environment variable management
- fastapi: Web framework for building APIs
- uvicorn: ASGI server for running the FastAPI app
- pytesseract: Python wrapper for Tesseract OCR
- Pillow: Python Imaging Library for image processing

### Frontend
- streamlit: Web application framework
- requests: HTTP client for communicating with the backend

## Customizing the AI Prompt

You can modify the prompt in `backend/app/summarizer.py` to change what the AI focuses on or the output format.

## License

MIT License - see the LICENSE file for details

## Disclaimer

This tool is for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.

**OCR Disclaimer:** The accuracy of text extraction from images depends on image quality, text clarity, and the OCR engine. For medical documents, please verify critical information manually.
