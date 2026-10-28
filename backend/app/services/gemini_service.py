# app/services/gemini_service.py
import os
import logging
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()
logger = logging.getLogger(__name__)

# Initialize the new Google GenAI client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY is not set in the environment.")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_image_caption(file_path: str) -> str:
    try:
        img = Image.open(file_path)
        prompt = (
            "Describe this image in detail. Focus on the main subjects, "
            "actions, colors, and context. This description will be used "
            "for a semantic search engine, so use descriptive keywords."
        )
        logger.info(f"Sending image {file_path} to Gemini for captioning...")

        # FIX: Swapped to the active 2.5 flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[img, prompt]
        )

        caption = response.text.strip()
        logger.info("Successfully generated image caption.")
        return caption

    except Exception as e:
        logger.error(f"Error generating caption with Gemini: {str(e)}")
        return "Image description unavailable."
