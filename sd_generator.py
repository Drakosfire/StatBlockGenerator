import time
import utilities as u
from PIL import Image
import replicate
from pathlib import Path


start_time = time.time()
temp_image_path = "./image_temp/"

def preview_and_generate_image(character_name,sd_prompt, token):    
    img_start = time.time()   
    output=replicate.run(
            "drakosfire/dnd_monster_generator:80c9d4247c1e1bd92084af24fa61e88b6a809a42585e343af9722d90337c9ada",
            input={
            "character_name":character_name,
            "sd_prompt":sd_prompt,
           "token":token

        }
    )
    
    
    img_time = time.time() - img_start
    img_its = 35/img_time
    print(f"image gen time = {img_time} and {img_its} it/s")
    
    total_time = time.time() - start_time
    print(total_time)

    return output

