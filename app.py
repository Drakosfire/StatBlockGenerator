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

# This is a fix for the way that python doesn't release system memory back to the OS and it was leading to locking up the system
libc = ctypes.cdll.LoadLibrary("libc.so.6")
M_MMAP_THRESHOLD = -3

# Set malloc mmap threshold.
libc.mallopt(M_MMAP_THRESHOLD, 2**20)

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
    
    gr.HTML(""" <div id="inner"> <header>
            <h1>Monster Statblock Generator</h1>
            <p>
            With this AI driven tool you will build a collectible style card of a fantasy flavored item with details.
            </p>
            </div>""")
    
    markdown_instructions = """## How It Works
This tool is a fun way to quickly generate Dungeons and Dragons monster manual style statblocks with art and a token for a Virtual Table Top.
1. Your intitial text along with the prompt is sent to Llama 3 70b to generate all the values for a Dungeons and Dragons creature.
    a. Include as much or as little information as you'd like.
    b. Just a name : The Flavor Lich
    c. A bit of detail : A friendly skeletal lich who is a master of flavor, called The Flavor Lich
    d. Lots of detail : A friendly skeletal lich who is a master of flavor, called The Flavor Lich, the Lich is Challenge Rating 8 and is a 4th level spell caster whose spells are all about food.
2. The results will populate below in editable fields that are saved on edit. 
3. Review the results, make any changes you'd like.
## The first image generation take about 2 minutes for model to 'cold boot' after that it's ~10s per image.
**Image and Text Generation**: Now you can generate 4 images for the statblock page without text and pick your favorite.
4. Click 'Generate Statblock Art' and wait for the images to generate, then select the one you'd like to use.
5. Click 'Generate HTML' to generate a webpage that can be saved or printed as PDF.
6. Last, you can generate a Virtual Tabletop token or figure of your creature.
 """

    gr.Markdown(markdown_instructions)
    with gr.Tab("Generator"):
                    
        with gr.Row():
            with gr.Column():
                user_mon_description = gr.Textbox(label = "Step 1 : Write a description and give a name or type to your creation!",
                                                lines = 1, placeholder=f"Ex : A friendly skeletal lich who is a master of flavor, called The Flavor Lich",
                                                
                                                elem_id= "custom-textbox")
            with gr.Column():
                spells_checkbox = gr.Checkbox(label= "Spellcaster?")
                legendary_action_checkbox = gr.Checkbox(label= "Legendary Actions?")
            
        desc_gen = gr.Button(value = "Step 2 : Generate Description")

        mon_description_output = gr.Textbox(label = 'Description', lines = 2, interactive=True)
        

        with gr.Row():
            with gr.Column(scale = 1):            
                mon_name_output = gr.Textbox(label = 'Name', lines = 1, interactive=True)   
                mon_size_output =  gr.Textbox(label = 'Size', lines = 1, interactive=True)               
                mon_alignment_output = gr.Textbox(label = 'Alignment', lines = 1, interactive=True)
                mon_armor_class_output = gr.Textbox(label = 'Armor Class', lines = 1, interactive=True)
                mon_hit_dice_output = gr.Textbox(label = 'Hit Dice', lines = 1, interactive=True)
                mon_senses_output = gr.Textbox(label = 'Senses', lines = 1, interactive=True)
                mon_actions_output = gr.Textbox(label = 'Actions', lines = 16, interactive=True)
                
            with gr.Column(scale = 1):
                mon_type_output = gr.Textbox(label = 'Type', lines = 1, interactive=True)
                mon_speed_output = gr.Textbox(label = 'Speed', lines = 1, interactive=True)
                mon_abilities_output = gr.Textbox(label ='Ability Scores', lines = 5, interactive=True)
                mon_damage_resistance_output = gr.Textbox(label = 'Damage Resistance', lines = 1, interactive=True)
                mon_challenge_rating_output = gr.Textbox(label = 'Challenge Rating', lines = 1, interactive=True)
                mon_cantrips_output = gr.Textbox(label = 'Cantrips', lines = 16, interactive=True)
                mon_spells_output = gr.Textbox(label = 'Spells', lines = 16, interactive=True)
                mon_spell_slot_output = gr.Textbox(label = 'Spell Slots', lines = 8, interactive=True)

            with gr.Column(scale = 1):
                mon_subtype_output = gr.Textbox(label = 'Subtype', lines = 1, interactive=True)                
                mon_saving_throws_output = gr.Textbox(label = 'Saving Throws', lines = 1, interactive=True)
                mon_skills_output = gr.Textbox(label = 'Skills', lines = 1, interactive=True)
                mon_hp_output = gr.Textbox(label = 'Health Points', lines = 1, interactive=True)
                mon_languages_output = gr.Textbox(label = 'Languages', lines = 1, interactive=True)
                mon_xp_output = gr.Textbox(label = 'XP', lines = 1, interactive=True)
                mon_legendary_actions_output = gr.Textbox(label = 'Legendary Actions', lines = 16, interactive=True) 

        mon_sd_prompt_output = gr.Textbox(label = 'Image Generation Prompt', lines = 1, interactive=True)

        with gr.Row():
            with gr.Column():
                image_gen = gr.Button(value = "Generate Art for the statblock" ) 
                mon_image_gallery = gr.Gallery(label = "Generated Images",
                                        show_label = True,
                                        elem_id = "gallery",
                                        columns =[4], rows =[1],
                                        object_fit = "contain", height ="auto")
              
            with gr.Column(): 
                token_gen = gr.Button(value = "Generate Token Image" ) 
                mon_token_gallery = gr.Gallery(label = "Generated Tokens",
                                        show_label = True,
                                        elem_id = "token_gallery",
                                        columns =[4], rows =[1],
                                        object_fit = "contain", height ="auto")
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
    gen_html = gr.Button(value = "Step 8 : Generate html, click once then go to Step 9")
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
    
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where the script is located
    print(f"Base Directory :",base_dir)
    list_of_static_dir = [os.path.join(base_dir, "output"), 
                        os.path.join(base_dir, "dependencies")] 
    gr.set_static_paths(paths=list_of_static_dir)
    
    
    if __name__ == "__main__":
        demo.launch(allowed_paths=list_of_static_dir)      
        
        
        












    