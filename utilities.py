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

list_of_monster = ["Kitsune", "Wendigo", "Chupacabra", "Kappa", "Jersey Devil", "Banshee", "Manticore", "Thunderbird", "Skinwalker","Bunyip", "Nuckelavee","Hodag", "Nymph", "Harpy", "Chimaera", "Krampus", "Tengu", "Jiangshi", "Cockatrice", "Naga", "Minotaur", "Hippogriff", "Centaur", "Chimera","Gorgon", "Siren", "Lamia", "Yuki-onna", "Jorogumo", "Peryton", "Manananggal", "Aswang", "Ifrit", "Ghouleh", "Tikbalang", "Impundulu", "Taniwha", "Lou Carcolh", "Baku", "Umibōzu", "Ahuizotl", "Grootslang", "Rusalka", "Cuca", "Loveland Frog", "Boggart", "Kishi", "Aqrabuamelu", "El Cuco", "Yara-ma-yha-who", "Kapre", "Camahueto", "Rokurokubi", "Aigamuxa", "Abada", "Catoblepas", "Wampus Cat", "Teju Jagua", "Peluda", "Leshy", "Tsukumogami", "Nuppeppo", "Akhlut", "Myling"]
list_of_vivid_words = ["Arcane", "Eldritch", "Luminous", "Shadowy", "Ethereal", "Enchanted", "Verdant", "Serpentine", "Ominous", "Crystalline", "Whispering", "Cacophonous", "Nebulous","Radiant", "Phantasmal", "Bioluminescent", "Gossamer", "Tempestuous", "Cavernous", "Glistening", "Iridescent", "Resplendent", "Ephemeral", "Polychromatic", "Volcanic", "Mysterious", "Subterranean", "Tremulous", "Spectral", "Eerie", "Prismatic", "Venerable", "Decrepit","Resonant", "Astral", "Quicksilver", "Mellifluous", "Arcadian", "Penumbral", "Sibilant", "Astronomical", "Empyreal", "Ineffable", "Nocturnal", "Verdigris", "Pluvial", "Sylphlike", "Labyrinthine", "Unfathomable", "Zephyrous", "Ethereal", "Opaque", "Abyssal", "Tranquil",  "Visceral", "Esoteric", "Euphoric", "Eldritch""", "Incantatory", "Surreal", "Nebulous", "Mythical", "Liminal", "Enigmatic", "Euphoric", "Mesmerizing", "Hypnotic","Enigmatic", "Quixotic", "Elysian", "Aberrant", "Enigmatical", "Tempestuous", "Astral", "Vibrant", "Nebulous","Prismatic", "Volatile", "Echolalic", "Mirthful", "Capricious", "Transcendent", "Unearthly", "Tempestuous", "Visceral", "Elemental", "Mesmeric", "Celestial", "Otherworldly"]
list_of_color_words = ["Crimson", "Azure", "Obsidian", "Amethyst", "Viridian", "Vermilion", "Cerulean", "Onyx", "Topaz", "Sable", "Ruby", "Jade", "Sapphire", "Ebony", "Indigo", "Garnet", "Turquoise", "Cobalt", "Citrine", "Opal", "Emerald", "Peridot","Scarlet", "Mauve", "Goldleaf", "Roseate", "Cobalt", "Ivory", "Ashen", "Tawny", "Umbral", "Alabaster", "Cerise", "Malachite", "Cyan", "Amber", "Scarlet", "Ochre", "Magenta", "Lavender", "Ebony", "Silvered", "Argent", "Tyrian","Platinum", "Fuchsia", "Marigold", "Aquamarine", "Olivine", "Garnet", "Cobalt", "Burnished", "Opulent", "Pearly", "Gilded", "Ebon", "Verdant", "Amaranthine", "Lavender", "Onyx", "Turquoise", "Ruby", "Citrine", "Iridescent", "Violet","Mauve", "Crimson", "Viridescent", "Cobalt", "Carmine", "Heliotrope"]
list_of_style = ["illustration", "painting", "CGI artwork", "Photograph"]




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
    folder_path = f"/media/drakosfire/Shared/Docker/StatblockGenerator/output/{foldertimestr}"
    if not os.path.exists("/media/drakosfire/Shared/Docker/StatblockGenerator/output"):
        os.mkdir("/media/drakosfire/Shared/Docker/StatblockGenerator/output")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return foldertimestr  

def make_image_name(name):
    del image_name_list[:]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    image_name = f"/media/drakosfire/Shared/Docker/StatblockGenerator/output/{make_folder()}/{name}{timestr}.png"
    image_name = image_name.replace(' ', '_')
    image_name_list.append(image_name)
    print("Image name is : " + image_name_list[-1])
    return image_name

def make_user_log() :
    del user_log[:]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    folder_path = f"/media/drakosfire/Shared/Docker/StatblockGenerator/output/{make_folder()}"
    user_log_file = open(f"{folder_path}/userlog-{timestr}.txt","w")
    user_log.append(dsh.prompt_list[0])
    user_log.append(f"Output from LLM: {dsh.sd_input[0]}")
    user_log.append(sth.output_list[0])    
    user_log.append(sth.output_list[1]) 

    date_time = generate_datetime()       
    print(date_time, file = user_log_file)    
    print(user_log, file= user_log_file)
    user_log_file.close()
    
# Create a unique time stamped file name
def gen_file_name(mon_name):
  del file_name_list[:]
  timestr = time.strftime("%H%M%S") 
  input_dir = f"/media/drakosfire/Shared/Docker/StatblockGenerator/output/{make_folder()}" 

  mon_file_name = mon_name
  file_name = mon_file_name + "_" + timestr 
  file_name_list.append(input_dir)
  file_name_list.append(file_name)
  file_name_list.append(mon_file_name)

def make_folder():
    foldertimestr = time.strftime("%Y%m%d_%H")
    folder_path = f"/media/drakosfire/Shared/Docker/StatblockGenerator/output/{foldertimestr}"
    if not os.path.exists("/media/drakosfire/Shared/Docker/StatblockGenerator/output"):
        os.mkdir("/media/drakosfire/Shared/Docker/StatblockGenerator/output")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return foldertimestr 

# Create a list of a directory if directory exists
def directory_contents(directory_path):
    if os.path.isdir(directory_path) :
          contents = os.listdir(directory_path)
          return contents
    else : pass


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
