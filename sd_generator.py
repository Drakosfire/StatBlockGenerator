import time
import fal_client  # Import the FLUX client
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

start_time = time.time()
temp_image_path = "./image_temp/"

def preview_and_generate_image(character_name, sd_prompt, token):
    try:
        logger.info(f"Generating image for character: {character_name} with prompt: {sd_prompt}")
        
        request_handle = fal_client.submit(
            "fal-ai/flux/dev",
            arguments={
                "num_inference_steps": 35,
                "prompt": sd_prompt,
                "num_images": 4,
                "strength": 0.85,
                "width": 1024,
                "height": 1024
            }
        )
        
        result = request_handle.get()
        logger.info(f"API result: {result}")
        
        image_urls = [img['url'] for img in result.get('images', [])]

        if not image_urls:
            logger.warning("No images were generated.")
            return []
        
        logger.info(f"Generated image URLs: {image_urls}")
        return image_urls

    except Exception as e:
        logger.error(f"Error during API call or processing: {str(e)}")
        logger.exception("Full traceback:")
        return []

   
        


