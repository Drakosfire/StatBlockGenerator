import time
from datetime import datetime
import os
import gc
import torch
import description_helper as dsh

# Utility scripts for all modules

# List for file locations to point at
file_name_list = []
image_name_list = []
link_list =['something','Link to monster statblock once generated']
random_prompt_list = []
user_log = []

def clear_cache():
    command = "sync; echo 3 > /proc/sys/vm/drop_caches"
    os.system(command)
    print(os.system("free"))
    
def reclaim_mem():
    allocated_memory = torch.cuda.memory_allocated()
    cached_memory = torch.cuda.memory_reserved()
    mem_alloc = f"Memory Allocated: {allocated_memory / 1024**2:.2f} MB"
    mem_cache = f"Memory Cached: {cached_memory / 1024**2:.2f} MB"
    print(mem_alloc)
    print(mem_cache)
    torch.cuda.ipc_collect()
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    time.sleep(0.01)
    allocated_memory = torch.cuda.memory_allocated()
    cached_memory = torch.cuda.memory_reserved()
    print(f"Memory Allocated after del {mem_alloc}")
    print(f"Memory Cached after del {mem_cache}")


def generate_datetime():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

def make_folder():
    foldertimestr = time.strftime("%Y%m%d_%H")
    folder_path = f"./output/{foldertimestr}"
    if not os.path.exists("./output"):
        os.mkdir("./output")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return foldertimestr  

def make_image_name(name):
    del image_name_list[:]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    image_name = f"./output/{make_folder()}/{name}{timestr}.png"
    image_name = image_name.replace(' ', '_')
    image_name_list.append(image_name)
    print("Image name is : " + image_name_list[-1])
    return image_name

    
# Create a unique time stamped file name
def gen_file_name(mon_name):
  del file_name_list[:]
  timestr = time.strftime("%H%M%S") 
  input_dir = f"./output/{make_folder()}" 

  mon_file_name = mon_name
  file_name = mon_file_name + "_" + timestr 
  file_name_list.append(input_dir)
  file_name_list.append(file_name)
  file_name_list.append(mon_file_name)

def make_folder():
    foldertimestr = time.strftime("%Y%m%d_%H")
    folder_path = f"./output/{foldertimestr}"
    if not os.path.exists("./output"):
        os.mkdir("./output")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return foldertimestr 

# Create a list of a directory if directory exists
def directory_contents(directory_path):
    if os.path.isdir(directory_path) :
          contents = os.listdir(directory_path)
          return contents
    else : pass

def absolute_path(directory_path):
    path_list = []
    if os.path.isdir(directory_path):
        contents = os.listdir(directory_path)
        for item in contents:
            item_path = os.path.join(directory_path,item)
            abs_path = os.path.abspath(item_path)
            path_list.append(abs_path)
    return path_list
            
            

# Delete a list of file 
def delete_files(file_paths):
    if file_paths:
     
        for file_path in file_paths:
            try:
                os.remove(f"./image_temp/{file_path}")
                print(f"Remove : ./image_temp/{file_path}")
            except OSError as e:
                print(f"Error: {file_path} : {e.strerror}")
        file_paths.clear()                                                                                                                                                   
