from diffusers import StableDiffusionXLPipeline
import torch
from compel import Compel, ReturnedEmbeddingsType
import utilities as u
import time


image_list = []
def del_image_list() :
    del image_list 

# batch size  
num_img = 4
# Assign path to model to be used and tell torch to be ready for 32 bit
torch.backends.cuda.matmul.allow_tf32 = True
model_path = ("/home/user/app/models/stable-diffusion/SDXLFaetastic_v24.safetensors")

def generate_image(sd_input) :
    u.reclaim_mem()
 
    start_time = time.time()
      
    
    # create variable that calls SD model and work in float 16
    # from_single_file is critical for loading a local file
    pipeline = StableDiffusionXLPipeline.from_single_file(model_path, custom_pipeline="lpw_stable_diffusion", torch_dtype=torch.float16, variant="fp16" ).to("cuda")
   
    # enable vae slicing ton prevent Out Of Memory Error when generating batches
    # pipeline.enable_vae_slicing()
    
    # Compel is a module that could allow longer than 77 token prompts AND adding weights to specific tokens
    compel = Compel(tokenizer=[pipeline.tokenizer, pipeline.tokenizer_2] , 
                text_encoder=[pipeline.text_encoder, pipeline.text_encoder_2], 
                returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED, 
                requires_pooled=[False, True],
               truncate_long_prompts=False)

        
    # assign prompt as global sd_input
    prompt = sd_input
    

    # Not sure what conditioning or pooled means, but it's in the demo code from here https://github.com/damian0815/compel/blob/main/compel-demo-sdxl.ipynb
    negative_prompt = "sex, lingerie, midriff, watermark, text, fastnegative2, blurry, ugly, low quality, worst quality, 3d"
    conditioning, pooled = compel([prompt, negative_prompt])
    print(conditioning.shape, pooled.shape)
    
    # generate image
    # image = pipe(prompt=prompt,num_inference_steps=50).images[0]
    for x in range(num_img):
        image = pipeline(prompt_embeds=conditioning[0:1], pooled_prompt_embeds=pooled[0:1], 
                    negative_prompt_embeds=conditioning[1:2], negative_pooled_prompt_embeds=pooled[1:2],
                    num_inference_steps=30, width=1024, height=1024).images[0]
        image_name = u.make_image_name()
        image.save(image_name)
        image_list.append(image_name)
        del image        


    del pipeline
    del compel
    
    del image_name
    del prompt

    u.reclaim_mem()
    print(image_list)
    stop_time = time.time()
    run_time = stop_time - start_time
    print(f"Time to generate : {run_time}")

    return image_list 

