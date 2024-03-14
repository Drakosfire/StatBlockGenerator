# this imports the code from files and modules
import description_helper as dsh
import gradio as gr
import sd_generator as sd
import statblock_helper as sth
import utilities as u
import process_html
import os
import ctypes

print("Building app")
# This is a fix for the way that python doesn't release system memory back to the OS and it was leading to locking up the system
libc = ctypes.cdll.LoadLibrary("libc.so.6")
M_MMAP_THRESHOLD = -3

# Set malloc mmap threshold.
libc.mallopt(M_MMAP_THRESHOLD, 2**20)


# Build functions that will be called by Gradio UI


# Take input from gradio user and call the llm in description_helper
def gen_mon_desc(user_monster_type, user_monster_color,user_monster_size, user_monster_loc): 
    u.reclaim_mem()
    # Delete the list of images in sd
    sd.del_image_list
    dsh.del_sd_input
    
    # Prompt template with user inputs added to be printed to log and terminal
    prompt_template = f"You are an intelligent and very good writer of fantasy fiction that uses a diverse and wide ranging vocabulary. Write a very concise, visually descriptive, detailed and colorful paragraph description of a {user_monster_type}, include description of its body, face, and limbs, it is {user_monster_color} and size {user_monster_size} at {user_monster_loc}. The {user_monster_color} {user_monster_type} "
    print("Prompt Template : " + prompt_template)

    # setting sd_input as global to be called and moved between models, this could probably be done better as a variable called from description helper  
    
    response = dsh.generate_monster_desc(user_monster_type, user_monster_color, user_monster_size,user_monster_loc)
    print(response)

    # A list to hold user inputs and start user log, 
    # Build static folders, this too needs to go to utilities
    #Create user log path all this needs to be moved to utilities
    
    
    u.reclaim_mem()
    return response


# Pass sd_input and call function to generate image and save bu calling name making function in utilities 
def gen_mon_img():
    print(dsh.sd_input)
    print(type(dsh.sd_input))
    sd_input = dsh.sd_input[0]   
    generated_images = sd.generate_image(sd_input)    
    
    # return a list of image relative paths to pass to gallery
    return generated_images

# Take the selected image in gallery and assign to global variable


# Pass modified input to statblock generator
def gen_mon_statblock(challenge_rating,abilities):     
    input = dsh.sd_input[0] + f"it is very important it is built with a challenge rating {challenge_rating}, create and give it the abilities {abilities}"
    generated_statblock = sth.generate_statblock(input)    
    return generated_statblock

# Call the html process program and point to the file
def mon_html_process(user_text):
    input_dir = sth.file_name_list[0]                                                                    
    md_path = f"{input_dir}/my-brew.md"
    mon_file_name = sth.file_name_list[0]+'/' + sth.file_name_list[1] +'.html'
    sth.md_process(md_path, sth.file_name_list[1])
    print("Ouput path = " + mon_file_name)
    print(f"User Text : {user_text}")
    process_html.process_html(mon_file_name,user_text)
    
# Build the html and file path to pass to gradio to output html file in gr.html 
def gen_link():
    mon_file_path = sth.file_name_list[0]+'/' + sth.file_name_list[1] +'.html'
    if not os.path.exists(mon_file_path):
        print(f"{mon_file_path} not found")
    else: print(f"{mon_file_path} found")
    iframe = iframe = f"""<iframe src="file={mon_file_path}" width="100%" height="500px"></iframe>"""
    link = f'<a href="file={mon_file_path}" target="_blank">{sth.file_name_list[1] +".html"}</a>'
    return link, iframe
    
# Build gradio app   
demo = gr.Blocks()
with gr.Blocks() as demo:
    # Title, eventually turn this into an updated variable with Monster name
    gr.HTML(""" <div id="inner"> <header>
    <h1>Monster Statblock Generator</h1>
                </div>""")
    with gr.Tab("Generator"):
        with gr.Row():
        
            with gr.Column(scale = 1):
                # Does this need to be a column? Building interface to receive input           
                            
                mon_name = gr.Textbox(label = "Step 1 : The Monster's Name or type", lines = 1, placeholder=f"Ex : A friendly skeletal lich", elem_id= "Monster Name")
                mon_color = gr.Textbox(label = "Step 2 : Colors and description", lines = 3, placeholder="Ex: wearing a glimmering robe ", elem_id= "Monster Color")
                mon_size = gr.Dropdown(['Tiny','Small','Medium','Large','Huge','Gigantic','Titanic'], label = 'Step 3 : Size ', elem_id="Monster Size")
                mon_loc = gr.Textbox(label = "Step 4 Optional : Describe it's location", lines = 3, placeholder="in a dusty library", elem_id = "Monster Location" )
                desc_gen = gr.Button(value = "Step 5. Generate Description")
            with gr.Column(scale = 1):
                
                mon_desc = gr.Textbox(label = 'Monster Description', lines = 16, interactive=True)
                desc_gen.click(fn = gen_mon_desc, inputs = [mon_name, mon_color, mon_size,mon_loc], outputs= mon_desc)
            
              
        # Output object for image, and button to trigger  
        image_Gen = gr.Button(value = "Step 6 : Generate 4x Images about 1 minute" ) 
        output_gallery = gr.Gallery(label = "Generated Images",
                                    show_label = False,
                                    elem_id = "gallery",
                                    columns =[4], rows =[1],
                                    object_fit = "contain", height ="auto")
        
        image_Gen.click(gen_mon_img, outputs = output_gallery)
        output_gallery.select(fn = process_html.assign_img)

    # Create a tab to split off statblock generation
    with gr.Tab("Step 7 : Statblock"):

        # Block to take in  
        gr.Interface(
            fn=gen_mon_statblock,
            inputs = [gr.Textbox(label="Challenge Rating, 1-20", lines =1),
                      gr.Textbox(label="Names of Abilities seperated by commas", lines = 3)],
            outputs = gr.Textbox(label = "Statblock", lines = 20, interactive=True, elem_id= "User Input"),
            allow_flagging="never"
            )
        
        # Build buttons to modify to html and show html 
        gen_html = gr.Button(value = "Step 8 : Generate html, click once then go to Step 9")
        gen_html.click(mon_html_process,inputs =[mon_desc], outputs=[])
        markdown = gr.Markdown(label="Output Box")
        html = gr.HTML(label="HTML preview", show_label=True)
        new_link_btn = gr.Button("Step 9: Display HTML and Link")
        new_link_btn.click(fn = gen_link, inputs = [], outputs = [markdown, html])

def main() -> None:
  # run web server, expose port 8000, share to create web link, give app access folder path, gradio was updated for security and can no longer serve any directory not specified.
  if __name__ == '__main__':
    demo.launch(server_name = "0.0.0.0", server_port = 8000, share = False, allowed_paths = ["/home/user/app/output","/home/user/app/dependencies"])
  
main()










    