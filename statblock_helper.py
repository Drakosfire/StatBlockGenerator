import description_helper as dsh
import time
import os
import subprocess
import utilities as u 
from python_on_whales import docker 

from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer,
    ExLlamaV2Lora,
)

from exllamav2.generator import (
    ExLlamaV2BaseGenerator,
    ExLlamaV2StreamingGenerator,
    ExLlamaV2Sampler
)

file_name_list = []
output_list = []

# This needs to be moved to utilities

def gen_file_name():
  del file_name_list[:]
  timestr = time.strftime("%H%M%S") 
  input_dir = f"/home/user/app/output/{u.make_folder()}" 

  mon_file_name = dsh.generate_monster_desc.monster_type.replace(' ', '') 
  file_name = mon_file_name + "_" + timestr 
  file_name_list.append(input_dir)
  file_name_list.append(file_name)
  file_name_list.append(mon_file_name)

# Function to find the beginning of the output markdown and remove the prompt before it

def rembeforestart(text):
  where_start = text.find('{{')
  if where_start == -1:    
    return text  
  return text[where_start:] 

# Function to remove any extra after the end of the Markdown

def remafterend(text):
  where_end = text.find('}}')
  if where_end == -1:
    return text
  return text[:where_end + 2]

def generate_statblock(input):
    gen_file_name()     
    run_time = time.time()
    generate_statblock.input = input
  
    # Initialize model and cache

    model_directory = "/home/user/app/models/Speechless-Llama2-Hermes-Orca-Platypus-WizardLM-13B-GPTQ"
    config = ExLlamaV2Config()
    config.model_dir = model_directory
    config.prepare()

    model = ExLlamaV2(config)
    print("Loading model: " + model_directory)
    model.load()

    tokenizer = ExLlamaV2Tokenizer(config)

    cache = ExLlamaV2Cache(model)

    # Load LoRA

    lora_directory = "/home/user/app/models/statblock-alpha"
    lora = ExLlamaV2Lora.from_directory(model, lora_directory)

    # Initialize generators

    
    simple_generator = ExLlamaV2BaseGenerator(model, cache, tokenizer)

    # Sampling settings

    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 0.85
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.1

    max_new_tokens = 1100

    # Build prompt

    monster_frame_wide ="""{{monster,frame,wide"""
    statblock_start = f"""{monster_frame_wide} \n## {dsh.generate_monster_desc.monster_type} """
    input_context = f"Write a .brewery formatted dungeons and dragons statblock of {generate_statblock.input} any abilities that reference actions need to have those actions defined \n" + statblock_start
    print(input_context)
    prompt = input_context
    

    generate_time = time.time()    
    output_text = simple_generator.generate_simple(prompt, settings, max_new_tokens, loras = lora)
    output_text = rembeforestart(output_text)

    generate_statblock.output_text = remafterend(output_text)
    print(generate_statblock.output_text)
    print("statblock generation time : " + str(time.time() - generate_time))
    
    input_dir = file_name_list[0]                                                                    
    input_md = open(f"{input_dir}/my-brew.md", 'w') 
    print(generate_statblock.output_text, file = input_md)
    
    #md_process(md_path, file_name_list[1])
 
   
    del model
    del tokenizer
    del output_text
    del simple_generator
    del cache
    del lora
    u.reclaim_mem()
    print("total statblock generation time  : " + str(time.time() - run_time))
    output_list.append(input_context)
    output_list.append(generate_statblock.output_text)
    u.make_user_log()
    return generate_statblock.output_text

# Function to process the my-brew.md file into a named html inside docker using process.js
def md_process(input_md,output_name):
  
  file_name = output_name
  # Passing in file name to derive absolute directory, and the desired output name
  abs_path = os.path.abspath(input_md)
  input_dir = os.path.dirname(abs_path)
  
  print(abs_path)
  print(input_dir)  
  # Subprocess to pass the docker command to the command line 
  # Docker compused from this https://github.com/G-Ambatte/.brewery/tree/experimentalCommandLineBrewProcess
  process_call = f"node /home/user/app/homebrewery/cli/process.js --input {abs_path} --output {input_dir}/{file_name}.html --renderer v3 --overwrite"
  print(process_call) 
  subprocess.run(process_call, shell=True)
  
# beginning of code to run html process and display in one shot
  #while True:
    #if os.path.isfile(file_name_list[0]+'/' + file_name_list[1] +'.html'):
        #gen_html()
        #break
    #else:
        #print("File not found, waiting.")
        #time.sleep(1)  # wait for 1 second before checking again











