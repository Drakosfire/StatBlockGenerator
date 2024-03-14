import os
import re, fileinput, sys
import statblock_helper as sth
import utilities as u
import description_helper as dsh

import gradio as gr



# Assigning strings to variables for replacing location of dependencies for the webpage to local static folders
# Path is ../../ for the html files location in output/dated_folder/
break_tag = "<br>"
old_all_css = """<link href="https://use.fontawesome.com/releases/v5.15.1/css/all.css" rel="stylesheet" />"""
new_all_css = """<link href="../../dependencies/all.css" rel="stylesheet" />"""
old_fonts = """<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700" rel="stylesheet" type="text/css" />""" 
new_fonts = """<link href="../../dependencies/css.css?family=Open+Sans:400,300,600,700" rel="stylesheet" type="text/css" />"""
old_bundle = """<link href='/bundle.css' rel='stylesheet' />"""
new_bundle = """<link href='../../dependencies/bundle.css' rel='stylesheet' />"""
old_icon = """<link rel="icon" href="/assets/favicon.ico" type="image/x-icon" />"""
new_icon = """<link rel="icon" href="../../dependencies/favicon.ico" type="image/x-icon" />"""
old_style = """<link href='../build/themes/V3/Blank/style.css' rel='stylesheet' />"""
new_style = """<link href='../../dependencies/style.css' rel='stylesheet' />"""
old_5estyle = """<link href='../build/themes/V3/5ePHB/style.css' rel='stylesheet' />"""
new_5estyle = """<link href='../../dependencies/5ePHBstyle.css' rel='stylesheet' />"""


# creating global variable to pass user image selection to html file as variable usr_img
def assign_img(evt: gr.SelectData):   
    global usr_img  
    img_dict = evt.value
    usr_img = img_dict['image']['url']
    print(usr_img)

# function to collect the data in the description box if a user edits it.

    
# Functions to insert input strings before and after to modify html file 
def find_all_insert_before(html_file, pattern, new_tag):
    file = fileinput.input(html_file, inplace=True)
    for line in file:
        replacement = new_tag + line
        line = re.sub(pattern,replacement,line)
        sys.stdout.write(line)
    file.close()
   
def  insert_tag_before(html_file, pattern, new_tag):
    index = html_file.find(pattern)
    if index != -1:
        output = html_file[:index] + new_tag + html_file[index:]
        return output
         
def  insert_tag_after(html_file, pattern, new_tag):
    len_new_tag = len(new_tag)
    print(len_new_tag)
    index = html_file.find(pattern)
    output = html_file[:index + len(pattern)] + new_tag + html_file[ index + len(pattern):]
    return output

# Modify the output from the home/userbrewery process.js 
def process_html(self, user_text):
    
    # There is an encoding issue with the left and right quotation marks in the html files, they need to be replaced with single quotes
    html_path = self
    statblock_html = open(html_path, 'r')
    html_as_string = statblock_html.read()
    html_as_string = html_as_string.replace("â€™", "'").replace("â€˜", "'")  
    html_as_string = html_as_string.replace(old_all_css, new_all_css)
    html_as_string = html_as_string.replace(old_fonts, new_fonts)
    html_as_string = html_as_string.replace(old_bundle, new_bundle)
    html_as_string = html_as_string.replace(old_icon, new_icon)
    html_as_string = html_as_string.replace(old_style, new_style)
    html_as_string = html_as_string.replace(old_5estyle, new_5estyle)

    # Strip out <br> so that it can be readded after strong  marker to be bold, then remove it from Armor and Speed for reasons of formatting
    html_as_string = html_as_string.replace("<br><strong>","<strong>")
    html_as_string = html_as_string.replace("<strong>","<br><strong>")
    html_as_string = html_as_string.replace("<br><strong>Armor","<strong>Armor" )
    html_as_string = html_as_string.replace("<br><strong>Speed","<strong>Speed" )
    html_as_string = html_as_string.replace("</p>","" )
    html_as_string = html_as_string.replace("<p><br>","" )
    html_as_string = insert_tag_before(html_as_string,"<hr>", "</dl>" )
    html_as_string = insert_tag_before(html_as_string,"<strong>Armor Class</strong>", '<hr><dl>' )
    
    # Call global usr_img and assign a local variable
    input_img = usr_img
    print(usr_img)

    # Store image location string as variable to make it accesisble for locating and formatting
    
    img_location = f"""{input_img}" alt="{dsh.generate_monster_desc.monster_type}"""

    # Insert image before <hr> 
    html_as_string = insert_tag_before(html_as_string,"<hr><dl>", f'<p><img class=" " style="width:330px; mix-blend-mode:multiply;" src="{img_location}"></p>'  )

    # Use image to target where to insert description box
    user_desc = f""" <div class="block descriptive"><p>{user_text}</div></p> """
    html_as_string = insert_tag_before(html_as_string,"<hr><dl>", user_desc )

    # Re write and close html file
    with open(sth.file_name_list[0]+'/' + os.path.basename(html_path) , 'w') as clean_html:
        clean_html.write(html_as_string)
    clean_html.close()
    #clear link list and append with new entries
    del u.link_list[:]
    u.link_list.append(sth.file_name_list[0]+'/' + sth.file_name_list[1] +'.html')
    u.link_list.append(dsh.generate_monster_desc.monster_type)
 