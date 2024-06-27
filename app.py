# this imports the code from files and modules
import description_helper as dsh
import gradio as gr
import sd_generator as sd
import utilities as u
import process_html
import process_text
import os
import ctypes
import tripo3d as tripo3d
import uuid
from weasyprint import HTML

# This is a fix for the way that python doesn't release system memory back to the OS and it was leading to locking up the system
libc = ctypes.cdll.LoadLibrary("libc.so.6")
M_MMAP_THRESHOLD = -3

# Set malloc mmap threshold.
libc.mallopt(M_MMAP_THRESHOLD, 2**20)

# Declare accessible directories
base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where the script is located
print(f"Base Directory :",base_dir)
list_of_static_dir = [os.path.join(base_dir, "output"), 
                    os.path.join(base_dir, "dependencies"),
                    os.path.join(base_dir, "galleries")] 
gr.set_static_paths(paths=list_of_static_dir)

style_css = custom_css = """
<link href='file=/media/drakosfire/Shared/Docker/StatblockGenerator/dependencies/all.css' rel='stylesheet' />
<link href='file=/media/drakosfire/Shared/Docker/StatblockGenerator/dependencies/css.css?family=Open+Sans:400,300,600,700' rel='stylesheet' type='text/css' />
<link href='file=/media/drakosfire/Shared/Docker/StatblockGenerator/dependencies/bundle.css' rel='stylesheet' />
<link href='file=/media/drakosfire/Shared/Docker/StatblockGenerator/dependencies/style.css' rel='stylesheet' />
<link href='file=/media/drakosfire/Shared/Docker/StatblockGenerator/dependencies/5ePHBstyle.css' rel='stylesheet' />
"""
    
# Build gradio app   

with gr.Blocks(css = "style.css") as demo:
    # Functions and State Variables
    mon_name = gr.State()
    mon_size = gr.State()
    mon_type = gr.State()
    mon_subtype = gr.State()
    mon_alignment = gr.State()
    mon_armor_class = gr.State()
    mon_hp = gr.State()
    mon_hit_dice = gr.State()
    mon_speed = gr.State()
    mon_abilities = gr.State()
    mon_saving_throws = gr.State()
    mon_skills = gr.State()
    mon_damage_resistance = gr.State()
    mon_senses = gr.State()
    mon_languages = gr.State()
    mon_challenge_rating = gr.State()
    mon_xp = gr.State()
    mon_actions = gr.State()
    mon_cantrips = gr.State()
    mon_spells = gr.State() 
    mon_spell_slots = gr.State()   
    mon_legendary_actions = gr.State()    
    mon_description = gr.State()
    mon_sd_prompt = gr.State()
    # Image Variables
    generated_image_list = gr.State([])
    selected_generated_image = gr.State()
    selected_seed_image = gr.State()
    selected_token_image = gr.State()
    


    # Take input from gradio user and call the llm in description_helper
    def gen_mon_desc(user_monster_text, spellcaster, legendary_actions): 
                
        # declare cantrips, spells, and spell slots as empty string unless the variable is changed.
        mon_cantrips = ""
        mon_spells = "" 
        mon_spell_slots = ""
        mon_legendary_actions = ""

        llm_output = dsh.call_llm_and_cleanup(user_monster_text, spellcaster, legendary_actions)
        user_monster = dsh.convert_to_dict(llm_output)
        user_monster = llm_output
        keys_list = list(user_monster)
        mon_name = user_monster['name']
        mon_size = user_monster['size']
        mon_type = user_monster['type']
        mon_subtype = user_monster['subtype']
        mon_alignment = user_monster['alignment']
        mon_armor_class = user_monster['armor_class']
        mon_hp = user_monster['hit_points']
        mon_hit_dice = user_monster['hit_dice']
        mon_speed = user_monster['speed']
        if type(mon_speed) == dict:
            mon_speed = process_text.format_mon_qualities(mon_speed)
        
        mon_abilities = process_text.format_abilities_for_editing(user_monster['abilities'])        
        mon_saving_throws = user_monster['saving_throws']
        if type(mon_saving_throws) == dict:
            mon_saving_throws = process_text.format_mon_qualities(mon_saving_throws)

        mon_skills = user_monster['skills']        
        if type(mon_skills) == dict:
            mon_skills = process_text.format_mon_qualities(mon_skills)
        mon_damage_resistance = user_monster['damage_resistance']
        if type(mon_damage_resistance) == dict:
            mon_damage_resistance = process_text.format_mon_qualities(mon_damage_resistance)
        mon_senses = user_monster['senses']
        if type(mon_senses) == dict:
            mon_senses = process_text.format_mon_qualities(mon_senses)
        mon_languages = user_monster['languages']
        mon_challenge_rating = user_monster['challenge_rating']
        mon_xp = user_monster['xp']
        if 'actions' in keys_list:
            mon_actions = process_text.format_actions_for_editing(user_monster['actions'])
        

        if "spells" in keys_list : 
            print(user_monster['spells'])
            print(f"Length of spells : {len(user_monster['spells'])}")
            if len(user_monster['spells']) >= 1 and user_monster['spells'] != "{}": 
                mon_spells = user_monster['spells'] 
                mon_cantrips,mon_spells,mon_spell_slots = process_text.format_spells_for_editing(mon_spells)   
                print(mon_cantrips,mon_spells, mon_spell_slots)      
        
        if 'legendary_actions' in keys_list and len(user_monster['legendary_actions']) >= 1 and user_monster['legendary_actions'] != "{}":
            mon_legendary_actions = user_monster['legendary_actions']    
        if type(mon_legendary_actions) == dict:
            mon_legendary_actions = process_text.format_legendaries_for_editing(mon_legendary_actions)
                    
        mon_description = user_monster['description']
        mon_sd_prompt = user_monster['sd_prompt']      
        
        #Return each State variable twice, once to the variable and once to the textbox
        return [mon_name,mon_name,
                mon_size,mon_size,
                mon_type,mon_type,
                mon_subtype,mon_subtype,
                mon_alignment, mon_alignment,
                mon_armor_class, mon_armor_class,
                mon_hp, mon_hp,
                mon_hit_dice, mon_hit_dice,
                mon_speed, mon_speed,
                mon_abilities,mon_abilities,
                mon_saving_throws, mon_saving_throws,
                mon_skills, mon_skills,
                mon_damage_resistance, mon_damage_resistance,
                mon_senses, mon_senses,
                mon_languages, mon_languages,
                mon_challenge_rating, mon_challenge_rating,
                mon_xp, mon_xp,
                mon_actions, mon_actions,
                mon_cantrips, mon_cantrips, mon_spells, mon_spells,mon_spell_slots,mon_spell_slots,
                mon_legendary_actions, mon_legendary_actions,
                mon_description, mon_description,
                mon_sd_prompt,mon_sd_prompt 
                ]
    #Function to dynamically render textbox if it has text.                
    def update_visibility(textbox):        
        if not textbox:
            return gr.update(visible=False)
        return gr.update(visible=True)
    
    
    # Called on user selecting an image from the gallery, outputs the path of the image
    def assign_img_path(evt: gr.SelectData):          
        img_dict = evt.value
        print(img_dict)
        selected_image_path = img_dict['image']['url']
        print(selected_image_path)
        return selected_image_path  
    
     # Make a list of files in image_temp and delete them
    def delete_temp_images():
        image_list = u.directory_contents('./image_temp')
        u.delete_files(image_list)
        #img2img.image_list.clear()
    
    # Called when pressing button to generate image, updates gallery by returning the list of image URLs
    def generate_image_update_gallery(image_prompt,image_name, token = False):        
        delete_temp_images()
        print(f"sd_prompt is a {type(image_prompt)}")
        image_list = []
        
        num_img = 4
        for x in range(num_img):
            preview = sd.preview_and_generate_image(image_name, image_prompt,token)
            image_list.append(preview)
            yield image_list
        del preview
        
        return image_list
    
    def generate_token_update_gallery(image_prompt,image_name,token = True):
        delete_temp_images()
        print(f"sd_prompt is a {type(image_prompt)}")
        image_list = []
        
        num_img = 4
        for x in range(num_img):
            preview = sd.preview_and_generate_image(image_name, image_prompt,token)
            image_list.append(preview)
            yield image_list
        del preview
        
        return image_list
       
        
     # Generate a 3D model by passing the chosen token image to Tripo3D.ai API
    def generate_model_update_gallery(image):
        generated_model = tripo3d.generate_model(image)
        return generated_model
  
    # Build html text by processing the generated dictionaries.
    def build_html_file(mon_name_output, 
                    mon_size_output,
                    mon_type_output,
                    mon_subtype_output,
                    mon_alignment_output,
                    mon_armor_class_output,
                    mon_hp_output,
                    mon_hit_dice_output,
                    mon_speed_output,
                    mon_abilities,
                    mon_saving_throws_output,
                    mon_skills_output,
                    mon_damage_resistance_output,
                    mon_senses_output,
                    mon_languages_output,
                    mon_challenge_rating_output,
                    mon_xp_output,
                    mon_actions_output,
                    selected_generated_image,
                    mon_description_output,
                    mon_cantrips_output,
                    mon_spells_output,
                    mon_spell_slot_output,
                    mon_legendary_actions_output
                    ):
        mon_file_path = process_html.build_html_base(
                        mon_name_output, 
                        mon_size_output,
                        mon_type_output,
                        mon_subtype_output,
                        mon_alignment_output,
                        mon_armor_class_output,
                        mon_hp_output,
                        mon_hit_dice_output,
                        mon_speed_output,
                        mon_abilities,
                        mon_saving_throws_output,
                        mon_skills_output,
                        mon_damage_resistance_output,
                        mon_senses_output,
                        mon_languages_output,
                        mon_challenge_rating_output,
                        mon_xp_output,
                        mon_actions_output,
                        selected_generated_image,
                        mon_description_output,   
                        mon_cantrips_output,                     
                        mon_spells_output,
                        mon_spell_slot_output,
                        mon_legendary_actions_output,
                                              
                        
                        )
        mon_file_path = u.file_name_list[0]+'/' + u.file_name_list[1] +'.html'
        if not os.path.exists(mon_file_path):
            print(f"{mon_file_path} not found")
        else: print(f"{mon_file_path} found")
        iframe = iframe = f"""<iframe src="file={mon_file_path}" width="100%" height="500px"></iframe>"""
        
        return iframe
    
        # Build the html and file path to pass to gradio to output html file in gr.html 
    def gen_link():
        mon_file_path = u.file_name_list[0]+'/' + u.file_name_list[1] +'.html'
        if not os.path.exists(mon_file_path):
            print(f"{mon_file_path} not found")
        else: print(f"{mon_file_path} found")
        iframe = iframe = f"""<iframe src="file={mon_file_path}" width="100%" height="500px"></iframe>"""
        link = f'<a href="file={mon_file_path}" target="_blank">{u.file_name_list[1] +".html"}</a>'
        return iframe
  
    with gr.Tab("Instructions"):
        image_path_list= u.absolute_path("./galleries/instructions")
        try:
            md_img_0 = f"""/file={image_path_list[0]} """
            md_img_1 =f"""/file={image_path_list[1]} """
            md_img_2 =f"""/file={image_path_list[2]} """
        except IndexError:
            # Handle the case where the list is empty
            md_img_0 = "No images found."
            md_img_1 = "No images found."
            md_img_2 = "No images found."
        
        gr.HTML(""" <div id="inner"> <header>
                <h1>Monster Statblock Generator</h1>
               
                </div>""")
        
        md_instructions_header = """## How It Works:"""       
        gr.Markdown(md_instructions_header)
        
        md_instructions_1=""" **Include as much or as little information as you'd like.** """
        gr.Markdown(md_instructions_1)
        gr.Image(value=md_img_0, show_label=False)
        
        gr.Image(value=md_img_1, show_label=False)
        
        md_instructions_2="""## Image Generation: 
        ** The first image generation take about 2 minutes to 'warm up' after that it's ~10s per image. ** \n
                
        1. Click 'Generate Statblock Art' and wait for the images to generate, then select the one you'd like to use. \n
        2. Click 'Generate HTML' to generate a webpage that can be saved or printed as PDF. \n
        3. Last, you can generate a token or figure of your creature or a 3d model to download. \n """

        gr.Markdown(md_instructions_2)
        
        gr.Image(value=md_img_2, show_label=False)
        
    with gr.Tab("Generator"):
                    
        with gr.Row():
            with gr.Column():
                user_mon_description = gr.Textbox(label = "Write a description and give a name or type to your creation!",
                                                lines = 1, placeholder=f"Ex : A friendly skeletal lich who is a master of flavor, called The Flavor Lich",
                                                
                                                elem_id= "custom-textbox")
            with gr.Column():
                spells_checkbox = gr.Checkbox(label= "Spellcaster?")
                legendary_action_checkbox = gr.Checkbox(label= "Legendary Actions?")
            
        desc_gen = gr.Button(value = "Click to Generate Description")

        mon_description_output = gr.Textbox(label = 'Description', lines = 2, interactive=True, visible=False)
        mon_description_output.change(fn=update_visibility,
                                                    inputs=[mon_description_output],
                                                    outputs=[mon_description_output])
        

        with gr.Row():
            with gr.Column(scale = 1):            
                mon_name_output = gr.Textbox(label = 'Name', lines = 1, interactive=True, visible=False) 
                mon_name_output.change(fn=update_visibility,
                                                    inputs=[mon_name_output],
                                                    outputs=[mon_name_output])  
                mon_size_output =  gr.Textbox(label = 'Size', lines = 1, interactive=True, visible=False)
                mon_size_output.change(fn=update_visibility,
                                                    inputs=[mon_size_output],
                                                    outputs=[mon_size_output])                 
                mon_alignment_output = gr.Textbox(label = 'Alignment', lines = 1, interactive=True, visible=False)
                mon_alignment_output.change(fn=update_visibility,
                                                    inputs=[mon_alignment_output],
                                                    outputs=[mon_alignment_output])
                mon_armor_class_output = gr.Textbox(label = 'Armor Class', lines = 1, interactive=True, visible=False)
                mon_armor_class_output.change(fn=update_visibility,
                                                    inputs=[mon_armor_class_output],
                                                    outputs=[mon_armor_class_output])
                mon_hit_dice_output = gr.Textbox(label = 'Hit Dice', lines = 1, interactive=True, visible=False)
                mon_hit_dice_output.change(fn=update_visibility,
                                                    inputs=[mon_hit_dice_output],
                                                    outputs=[mon_hit_dice_output])
                mon_senses_output = gr.Textbox(label = 'Senses', lines = 1, interactive=True, visible =False)
                mon_senses_output.change(fn=update_visibility,
                                                    inputs=[mon_senses_output],
                                                    outputs=[mon_senses_output])
                mon_actions_output = gr.Textbox(label = 'Actions', lines = 16, interactive=True, visible = False)
                mon_actions_output.change(fn=update_visibility,
                                                    inputs=[mon_actions_output],
                                                    outputs=[mon_actions_output])
                
            with gr.Column(scale = 1):
                mon_type_output = gr.Textbox(label = 'Type', lines = 1, interactive=True, visible=False)
                mon_actions_output.change(fn=update_visibility,
                                                    inputs=[mon_actions_output],
                                                    outputs=[mon_actions_output])
                mon_speed_output = gr.Textbox(label = 'Speed', lines = 1, interactive=True, visible=False)
                mon_speed_output.change(fn=update_visibility,
                                                    inputs=[mon_speed_output],
                                                    outputs=[mon_speed_output])
                mon_abilities_output = gr.Textbox(label ='Ability Scores', lines = 5, interactive=True, visible=False)
                mon_abilities_output.change(fn=update_visibility,
                                                    inputs=[mon_abilities_output],
                                                    outputs=[mon_abilities_output])
                mon_damage_resistance_output = gr.Textbox(label = 'Damage Resistance', lines = 1, interactive=True, visible=False)
                mon_damage_resistance_output.change(fn=update_visibility,
                                                    inputs=[mon_damage_resistance_output],
                                                    outputs=[mon_damage_resistance_output])
                mon_challenge_rating_output = gr.Textbox(label = 'Challenge Rating', lines = 1, interactive=True, visible=False)
                mon_cantrips_output = gr.Textbox(label = 'Cantrips', lines = 16, interactive=True, visible=False)
                mon_cantrips_output.change(fn=update_visibility,
                                           inputs=[mon_cantrips_output],
                                           outputs=[mon_cantrips_output])
                mon_spells_output = gr.Textbox(label = 'Spells', lines = 16, interactive=True, visible=False)
                mon_spells_output.change(fn=update_visibility,
                                         inputs=[mon_spells_output],
                                         outputs=[mon_spells_output])
                mon_spell_slot_output = gr.Textbox(label = 'Spell Slots', lines = 8, interactive=True, visible=False)
                mon_spell_slot_output.change(fn=update_visibility,
                                             inputs=[mon_spell_slot_output],
                                             outputs=[mon_spell_slot_output])

            with gr.Column(scale = 1):
                mon_subtype_output = gr.Textbox(label = 'Subtype', lines = 1, interactive=True, visible = False)
                mon_subtype_output.change(fn=update_visibility,
                                          inputs=[mon_subtype_output],
                                          outputs=[mon_subtype_output])                
                mon_saving_throws_output = gr.Textbox(label = 'Saving Throws', lines = 1, interactive=True, visible=False)
                mon_saving_throws_output.change(fn=update_visibility,
                                                    inputs=[mon_saving_throws_output],
                                                    outputs=[mon_saving_throws_output])
                mon_skills_output = gr.Textbox(label = 'Skills', lines = 1, interactive=True, visible=False)
                mon_skills_output.change(fn=update_visibility,
                                                    inputs=[mon_skills_output],
                                                    outputs=[mon_skills_output])
                mon_hp_output = gr.Textbox(label = 'Health Points', lines = 1, interactive=True, visible=False)
                mon_hp_output.change(fn=update_visibility,
                                                    inputs=[mon_hp_output],
                                                    outputs=[mon_hp_output])
                mon_languages_output = gr.Textbox(label = 'Languages', lines = 1, interactive=True, visible=False)
                mon_languages_output.change(fn=update_visibility,
                                                    inputs=[mon_languages_output],
                                                    outputs=[mon_languages_output])
                mon_xp_output = gr.Textbox(label = 'XP', lines = 1, interactive=True, visible=False)
                mon_xp_output.change(fn=update_visibility,
                                                    inputs=[mon_xp_output],
                                                    outputs=[mon_xp_output])
                mon_legendary_actions_output = gr.Textbox(label = 'Legendary Actions', lines = 16, interactive=True, visible = False) 
                mon_legendary_actions_output.change(fn = update_visibility,
                   inputs =[mon_legendary_actions_output],
                   outputs=[mon_legendary_actions_output])

        mon_sd_prompt_output = gr.Textbox(label = 'Image Generation Prompt', lines = 1, interactive=True, visible=True)
        mon_sd_prompt_output.change(fn=update_visibility,
                                                    inputs=[mon_sd_prompt_output],
                                                    outputs=[mon_sd_prompt_output])
        image_gen_instructions =  """ ## Image Generation  \n
    1. Review the text in the 'Image Generation Prompt' Textbox\n
    2. Click 'Generate Statblock Art' \n
    3. This will take 2 minutes for the first image, then about 10 seconds each. \n
        ** *Additional generation will take about 10 seconds each, until the server goes to sleep ~3 minutes inactivity. \n
    4. Click your favorite of the four images, this loads it for the page builder and 3d model generator.
    """

        gr.Markdown(image_gen_instructions)

        with gr.Row():
            with gr.Column():
                image_gen = gr.Button(value = "Generate Statblock Art" ) 
                mon_image_gallery = gr.Gallery(label = "Generated Images",
                                        show_label = True,
                                        elem_id = "gallery",
                                        columns =[4], rows =[1],
                                        object_fit = "cover",
                                        height ="auto")
              
            with gr.Column(): 
                token_gen = gr.Button(value = "Generate Token Image" ) 
                mon_token_gallery = gr.Gallery(label = "Generated Tokens",
                                        show_label = True,
                                        elem_id = "token_gallery",
                                        columns =[4], rows =[1],
                                        object_fit = "cover",
                                        height ="auto")
        model_gen_instructions = """## Generate a 3d model 

1. Make sure an image was clicked in the "Generated Images" gallery. 
*Works best with images without thin qualities, like antenna \n
2. Click Generate a 3d model button. 
3. Wait about 30 seconds, then review and download as an .glb file.
 """

        gr.Markdown(model_gen_instructions)
        model_gen = gr.Button(value= "Generate a 3D model")
        mon_model_gallery = gr.Model3D(label = "3D Model Display",
                                        elem_id = "model_gallery",
                                              )
        
        image_gen.click(generate_image_update_gallery, inputs = [mon_sd_prompt_output,mon_name], outputs = mon_image_gallery)
        token_gen.click(generate_token_update_gallery, inputs = [mon_sd_prompt_output,mon_name], outputs = mon_token_gallery)
        model_gen.click(generate_model_update_gallery, inputs = selected_generated_image, outputs = mon_model_gallery)
        
        mon_image_gallery.select(fn = assign_img_path, outputs=selected_generated_image)
        mon_token_gallery.select(fn = assign_img_path, outputs=selected_token_image)

        desc_gen.click(fn = gen_mon_desc, inputs = [user_mon_description,spells_checkbox, legendary_action_checkbox],
                        outputs= [mon_name, mon_name_output,
                                    mon_size,mon_size_output,
                                    mon_type,mon_type_output,
                                    mon_subtype,mon_subtype_output,
                                    mon_alignment, mon_alignment_output,
                                    mon_armor_class, mon_armor_class_output,
                                    mon_hp, mon_hp_output,
                                    mon_hit_dice, mon_hit_dice_output,
                                    mon_speed, mon_speed_output,
                                    mon_abilities, mon_abilities_output,
                                    mon_saving_throws, mon_saving_throws_output,
                                    mon_skills, mon_skills_output,
                                    mon_damage_resistance, mon_damage_resistance_output,
                                    mon_senses, mon_senses_output,
                                    mon_languages, mon_languages_output,
                                    mon_challenge_rating, mon_challenge_rating_output,
                                    mon_xp, mon_xp_output,
                                    mon_actions, mon_actions_output,
                                    mon_cantrips,mon_cantrips_output,
                                    mon_spells, mon_spells_output,
                                    mon_spell_slots, mon_spell_slot_output,
                                    mon_legendary_actions, mon_legendary_actions_output,
                                    mon_description, mon_description_output,
                                    mon_sd_prompt,mon_sd_prompt_output 
                                    
                                    ])
        
    
            
        # Build buttons to modify to html and show html 
        
        
        with gr.Row():
            with gr.Column():
                gen_html = gr.Button(value = "Step 3 : Generate html")
                html = gr.HTML(label="HTML preview", show_label=True)
            gen_html.click(build_html_file,inputs =[
                        mon_name_output, 
                        mon_size_output,
                        mon_type_output,
                        mon_subtype_output,
                        mon_alignment_output,
                        mon_armor_class_output,
                        mon_hp_output,
                        mon_hit_dice_output,
                        mon_speed_output,
                        mon_abilities_output,
                        mon_saving_throws_output,
                        mon_skills_output,
                        mon_damage_resistance_output,
                        mon_senses_output,
                        mon_languages_output,
                        mon_challenge_rating_output,
                        mon_xp_output,
                        mon_actions_output,
                        mon_description_output,
                        selected_generated_image,
                        mon_cantrips_output,
                        mon_spells_output,
                        mon_spell_slot_output,
                        mon_legendary_actions_output,

                        ], 
                        outputs= html
                        )
           
    example_headers = ['## Statblock Examples',
                           '## Token Examples',
                           '## 3D Model Examples']   
    with gr.Tab("Statblock Examples"):
        
        gr.Markdown(example_headers[0])
    
        examples = u.absolute_path("./galleries/examples/statblocks")
       
        example_gallery = gr.Gallery(label = "Statblock Examples",
                                    show_label = True,
                                    elem_id = "gallery",
                                    columns =[4], rows =[1],
                                    object_fit = "fill",
                                    height = 768,                                       
                                    value = examples)
    with gr.Tab("Token Examples"):
        example_headers = ['## Statblock Examples',
                           '## Token Examples',
                           '## 3D Model Examples']
        gr.Markdown(example_headers[1])
    
        examples = u.absolute_path("./galleries/examples/tokens")
        
        example_gallery = gr.Gallery(label = "Token Examples",
                                    show_label = True,
                                    elem_id = "gallery",
                                    columns =[4], rows =[1],
                                    object_fit = "fill",
                                    height = 768,                                       
                                    value = examples)
    with gr.Tab("3d Model Examples"):
        example_headers = ['## Statblock Examples',
                           '## Token Examples',
                           '## 3D Model Examples']
        gr.Markdown(example_headers[2])
    
        examples = u.absolute_path("./galleries/examples/models")
        with gr.Row():
            example_gallery = gr.Model3D(label = "3d Model Examples",
                                        show_label = True,
                                        value = examples[0])
            example_gallery = gr.Model3D(label = "3d Model Examples",
                                    show_label = True,
                                                                        
                                    value = examples[1])
    
    
    if __name__ == "__main__":
        demo.launch(allowed_paths=list_of_static_dir)      
        
        
        












    