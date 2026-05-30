import os
import logging
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class MedicalReportSummarizer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            self.model = None
        else:
            genai.configure(api_key=self.api_key)

            self.model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )
    
    def summarize_report(self, text: str) -> Dict[str, List[str]]:
        """
        Analyze medical report text to generate summary, action items, and deficiencies.
        
        Args:
            text: Extracted text from medical PDF report
            
        Returns:
            Dictionary with keys: 'summary', 'action_items', 'deficiencies'
        """
        if not self.model:
            logger.error("Gemini model not initialized. Check API key.")
            return {
                "summary": "Error: Unable to initialize AI service. Please check API key.",
                "action_items": [],
                "deficiencies": []
            }
        
        # Truncate text if too long (Gemini has token limits)
        # We'll keep first 25000 characters as a safe estimate (Gemini Pro has higher limits)
        max_chars = 25000
        if len(text) > max_chars:
            logger.warning(f"Text truncated from {len(text)} to {max_chars} characters")
            text = text[:max_chars] + "... [text truncated]"
        
        prompt = f"""You are an AI medical assistant tasked with analyzing medical reports. 
Please analyze the following medical report text and provide:

1. A concise summary of the key findings
2. A list of actionable items (what needs to be done based on the report)
3. A list of deficiencies or missing elements (what the body lacks or what's incomplete in the report)

Please format your response as follows:
SUMMARY: [Your summary here]
ACTION_ITEMS: [Each action item on a new line starting with - ]
DEFICIENCIES: [Each deficiency on a new line starting with - ]

Medical Report Text:
{text}"""

        try:
            response = self.model.generate_content(prompt)
            
            # Parse the response
            content = response.text
            return self._parse_response(content)
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return {
                "summary": f"Error generating summary: {str(e)}",
                "action_items": [],
                "deficiencies": []
            }
    
    def _parse_response(self, response_text: str) -> Dict[str, List[str]]:
        """
        Parse the AI response into structured format.
        
        Args:
            response_text: Raw response from Gemini
            
        Returns:
            Dictionary with summary, action_items, deficiencies
        """
        result = {
            "summary": "",
            "action_items": [],
            "deficiencies": []
        }
        
        # Split by sections
        sections = response_text.split('\n')
        current_section = None
        
        for line in sections:
            line = line.strip()
            if line.startswith("SUMMARY:"):
                current_section = "summary"
                result["summary"] = line.replace("SUMMARY:", "").strip()
            elif line.startswith("ACTION_ITEMS:"):
                current_section = "action_items"
                # Handle case where items might be on same line
                items_text = line.replace("ACTION_ITEMS:", "").strip()
                if items_text:
                    # If it starts with - or we need to split
                    if items_text.startswith("-"):
                        result["action_items"].append(items_text[1:].strip())
                    else:
                        result["action_items"].append(items_text)
            elif line.startswith("DEFICIENCIES:"):
                current_section = "deficiencies"
                items_text = line.replace("DEFICIENCIES:", "").strip()
                if items_text:
                    if items_text.startswith("-"):
                        result["deficiencies"].append(items_text[1:].strip())
                    else:
                        result["deficiencies"].append(items_text)
            elif current_section == "action_items" and line.startswith("-"):
                result["action_items"].append(line[1:].strip())
            elif current_section == "deficiencies" and line.startswith("-"):
                result["deficiencies"].append(line[1:].strip())
            elif current_section == "summary" and line and not line.startswith(("ACTION_ITEMS:", "DEFICIENCIES:")):
                # Append to summary if it's a continuation line
                if result["summary"]:
                    result["summary"] += " " + line
                else:
                    result["summary"] = line
        
        # Clean up empty items
        result["action_items"] = [item for item in result["action_items"] if item]
        result["deficiencies"] = [item for item in result["deficiencies"] if item]
        
        # If we didn't find proper sections, fall back to simple parsing
        if not result["summary"] and not result["action_items"] and not result["deficiencies"]:
            logger.warning("Could not parse structured response, using fallback")
            result["summary"] = response_text[:500] + "..." if len(response_text) > 500 else response_text
            
        return result

def summarize_medical_report(text: str) -> Dict[str, List[str]]:
    """
    Convenience function to summarize medical report.
    
    Args:
        text: Extracted text from medical PDF report
        
    Returns:
        Dictionary with summary, action_items, deficiencies
    """
    summarizer = MedicalReportSummarizer()
    return summarizer.summarize_report(text)

if __name__ == "__main__":
    # For testing
    import sys
    if len(sys.argv) > 1:
        # In real usage, we'd extract text first
        # For now, just echo the input
        print("This is the summarizer module. Use main.py for full functionality.")
    else:
        print("Usage: python summarizer.py <text_file>")
