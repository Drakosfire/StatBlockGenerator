
#import sys, os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import torch
import random
from random import randint
import gc
import os
import utilities as u
import time
from exllamav2 import(
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer,
)

from exllamav2.generator import (
    ExLlamaV2BaseGenerator,
    ExLlamaV2Sampler
)

# Creating userlog again? This needs to be merged and rebuilt in utilities


# Declare globals
device = "cuda:0"
model_directory =  "/home/user/app/models/Speechless-Llama2-Hermes-Orca-Platypus-WizardLM-13B-GPTQ"
prompt_list = []
sd_input = []

def del_sd_input() :
    del sd_input[:]
    print(sd_input)

# Initialize model and cache

   

# Function to load the llm, pass user input into a prompt, pass that prompt to llm and log memory and time then cleanup
def generate_monster_desc(monster_type, monster_color,monster_size,monster_loc):
    u.reclaim_mem()
    del_sd_input()
    print(sd_input)
    prompt_template = f"You are an intelligent, accomplished, expert writer of fantasy fiction that uses diverse and wide ranging vocabulary with a particular knack for painting mental images. Do not write instructions or tips, only write a concise, visually descriptive, detailed and colorful three to 5 sentences about the appearance of the {monster_type}, include description of its body and all of it's parts. This is a wholly orginial and unique creation {monster_color} is size {monster_size} and can be found {monster_loc}. The focus should be on describing it's appearance and it's very important it is FIVE sentences! Always start with the creatures name/type : {monster_type}"
    prompt_list.append(prompt_template)
    
    start_time = time.time()
    generate_monster_desc.monster_type = monster_type      
    generate_monster_desc.monster_color = monster_color    
    generate_monster_desc.monster_size = monster_size
    generate_monster_desc.monster_loc = monster_loc
    
    config = ExLlamaV2Config()
    config.model_dir = model_directory
    config.prepare()

    model = ExLlamaV2(config)
    print("Loading model: " + model_directory)
    print(f"Model load took {time.time() - start_time}")
    print(f"Memory allocated : {torch.cuda.memory_allocated()}")

    cache = ExLlamaV2Cache(model, lazy = True)
    model.load_autosplit(cache)

    tokenizer = ExLlamaV2Tokenizer(config)   
    # Initialize generator

    generator = ExLlamaV2BaseGenerator(model, cache, tokenizer)
    #generator.set_stop_conditions([tokenizer.eos_token_id])

    # Define settings

    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 1.10
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.15
      

    max_new_tokens = 512
    start_time = time.time()
    generator.warmup()
    

    generate_monster_desc.response = generator.generate_simple(prompt_template, settings, max_new_tokens, seed = random.randint(0,10**20))
    
    # Check if LLM output prompt as part of output, and remove.
    if prompt_template in generate_monster_desc.response:
        generate_monster_desc.response = generate_monster_desc.response.replace(prompt_template, '').replace('<s>','' ).replace('</s>', '')

    print(time.time() - start_time)
    print(f"Text generation took {time.time() - start_time}")
    print(f"Memory allocated : {torch.cuda.memory_allocated()}")

    # Clean up memory
    del model
    del tokenizer
    del generator
    del cache
    del config
    gc.collect()
    sd_input.append(generate_monster_desc.response)
    print(sd_input)
    return generate_monster_desc.response    
