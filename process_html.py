import re, fileinput, sys
import utilities as u
import description_helper as dsh

import gradio as gr

# HTML section headers
actions_header = """<h4 id="actions">Actions</h4>		
				"""
cantrips_header = """<h4 id="cantrips">Cantrips</h4>		
            """
spells_header = """<h4 id="known spells">Known Spells</h4>		
            """
spell_slot_header = """<h4 id="spell slots">Spell Slots</h4>		
            """
legendary_actions_header = """<h4 id="legendary actions">Legendary Actions</h4>		
            """

# Assigning strings to variables for replacing location of dependencies for the webpage to local static folders
# Path is ../../ for the html files location in output/dated_folder/
break_tag = "<br>"
def build_html_base(
                mon_name,
                mon_size,
                mon_type,
                mon_subtype,
                mon_alignment,
                mon_armor_class,
                mon_hp,
                mon_hit_dice,
                mon_speed,
                mon_abilities,
                mon_saving_throws,
                mon_skills,
                mon_damage_resistance,
                mon_senses,
                mon_languages,
                mon_challenge_rating,
                mon_xp,
                mon_actions,
                mon_description,
                mon_image_path,                
                mon_cantrips = False,
                mon_spells = False,
                mon_spell_slots = False,
                mon_legendary_actions = False               
                
                ) :
    
    

    # Combine the properties that will go on a single line
    if mon_subtype != "" :
        mon_properties = f"{mon_size}, {mon_type}, {mon_subtype}, {mon_alignment}"
    else: mon_properties = f"{mon_size}, {mon_type}, {mon_alignment}"
    mon_abilities = parse_abilities_from_text(mon_abilities)

    # Template for the page
    html_base = f"""<!DOCTYPE html>
<html>
<head>

<link href="../../dependencies/all.css" rel="stylesheet" />
<link href="../../dependencies/css.css?family=Open+Sans:400,300,600,700" rel="stylesheet" type="text/css" />
<link href='../../dependencies/bundle.css' rel='stylesheet' />
<link rel="icon" href="../../dependencies/favicon.ico" type="image/x-icon" />
<title>{mon_name}</title>
</head>
<body>
<link href='../../dependencies/style.css' rel='stylesheet' />
<link href='../../dependencies/5ePHBstyle.css' rel='stylesheet' />

<div class='brewRenderer'>
<style>undefined</style>
<div class='pages'>
	<div class='page phb' id='p1' key='0' >
		<div className='columnWrapper'>
			<div class="block monster frame wide"  >
				<h4 id="user-monster-name">{mon_name}</h4>
				<p><em>{mon_properties}</em> 
				<p><img class=" " style="width:330px; mix-blend-mode:multiply; border:3px solid black;" src={mon_image_path} alt="image"></p>
				<div class="block descriptive">
					<h5 id="user-monster-description">{mon_description}</h5>
					
				</div>
				<hr>
				<dl>
					<strong>Armor Class</strong> : {mon_armor_class}
					<strong>Hit Points</strong>: {mon_hp} Hit Dice : {mon_hit_dice}
					<strong>Speed</strong>: {mon_speed}
				</dl>
				<hr>
				<table>
					<thead>
						<tr>
							<th align=center>STR</th>
							<th align=center>DEX</th>
							<th align=center>CON</th>
							<th align=center>INT</th>
							<th align=center>WIS</th>
							<th align=center>CHA</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td align=center>{mon_abilities[0]}</td>
							<td align=center>{mon_abilities[1]}</td>
							<td align=center>{mon_abilities[2]}</td>
							<td align=center>{mon_abilities[3]}</td>
							<td align=center>{mon_abilities[4]}</td>
							<td align=center>{mon_abilities[5]}</td>
						</tr>
					</tbody>
				</table>
				<hr>
				<strong>Saving Throws</strong> : {mon_saving_throws}
				<br><strong>Skills</strong> : {mon_skills}
                <br><strong>Resistances</strong> : {mon_damage_resistance}
				<br><strong>Senses</strong> : {mon_senses}
				<br><strong>Languages</strong>  : {mon_languages}
				<br><strong>Challenge Rating</strong> : {mon_challenge_rating} ({mon_xp})"""
   
    
    if mon_actions :
        print("Actions : True")
        parsed_actions = parse_actions_from_text(mon_actions)
        
        html_file_as_text = f"""{html_base} <hr> {actions_header}
{''.join(parsed_actions)}"""
    else:
        print("Actions : False")
        html_file_as_text = html_base
    
    
    if mon_cantrips:
        print(mon_cantrips)
        mon_cantrips = mon_cantrips.replace("Cantrips", '')
        mon_cantrips = parse_cantrips_from_text(mon_cantrips)
        html_file_as_text = html_file_as_text + cantrips_header + mon_cantrips
    
    if mon_spells :
        print(mon_spells)
        mon_spells = mon_spells.replace("Known Spells",'')
        mon_spells = parse_spells_from_text(mon_spells)
        html_file_as_text = html_file_as_text + spells_header + mon_spells

    if mon_spell_slots:
        print(mon_spell_slots)
        mon_spell_slots = mon_spell_slots.replace("Spell Slots", '')
        mon_spell_slots = parse_spell_slots_from_text(mon_spell_slots)        
        html_file_as_text = html_file_as_text + spell_slot_header + mon_spell_slots
        

    else:        
        print("Spells : False")
    
    if mon_legendary_actions:        
        print("Legendary Actions : True")
        mon_legendary_actions = mon_legendary_actions.replace("Legendary Actions \n\n", '')
        mon_legendary_actions = parse_legendary_action_from_text(mon_legendary_actions)
        html_file_as_text = html_file_as_text +legendary_actions_header + mon_legendary_actions
    else: 
        print("Legendary Actions : False")

    # Open a file path that will receive the processed text 
    u.gen_file_name(mon_name)
    mon_file_path = f"{u.file_name_list[0]}/{u.file_name_list[1]}.html"
    with open(mon_file_path, 'w') as clean_html:
        clean_html.write(html_file_as_text)
    clean_html.close()
     
    #Passing back a file path that Gradio can access and is local
    return mon_file_path

def parse_actions_from_text(edited_text):
    html_content = '<dl>'
    actions = []
    action_entries = edited_text.strip().split('\n\n')
    print(action_entries)
    for entry in action_entries:
        parts = entry.split(';')
        action_dict = {
            "name": parts[0].split(": ")[1].strip(),
            "desc": parts[1].split("Description: ")[1].strip()
        }
        actions.append(action_dict)

    for action in actions:
        html_content += f"<dt><em><strong>{action['name']}</strong></em> :</dt><dd>‘{action['desc']}</dd>"
        html_content += "<br>"
    html_content=html_content.rstrip('br')
   
    html_content += '</dl>'
    return html_content

def parse_abilities_from_text(abilities):
    abilities_list = []
    ability_entries = abilities.strip().split('\n')
    for entry in ability_entries:
        parts = entry.split(':')
        ability_value = parts[1]
        abilities_list.append(ability_value)
    return abilities_list

def parse_cantrips_from_text(cantrips):
    html_content = '<dl>'
    cantrips_list = []
    cantrip_entries = cantrips.strip().split('\n\n')
    for entry in cantrip_entries:
        parts = entry.split(';')
        cantrip_dict = {
            "name": parts[0],
            "desc": parts[1].split("Description: ")[1].strip()
        }
        cantrips_list.append(cantrip_dict)
    for cantrip in cantrips_list:
        html_content += f"<dt><em><strong>{cantrip['name']}</strong></em> :</dt> <dd> ‘{cantrip['desc']}’</dd>"
        html_content += "<br>"
    html_content=html_content.rstrip('br')
    html_content += '</dl>'
    return html_content

def parse_spells_from_text(spells):
    html_content = '<dl>'
    spells_list = []
    spell_entries = spells.strip().split('\n\n')
    for entry in spell_entries:
        print(f"Spell entry = {entry}")
        parts = entry.split(';')
        spell_name_part = parts[0]
        level_desc_part = parts[1]

        # Extract the spell's name (before 'level:')
        name = spell_name_part.strip()

        # Further split level and description
        level_part = level_desc_part.split(", Description:")[0].strip()
        description_part = level_desc_part.split(", Description:")[1].strip() if ", Description:" in level_desc_part else ""

        # Extract the level (assuming it follows 'Level: ' directly)
        level = level_part.replace("Level: ", "").strip()
        print(f"Level = {level}")


        # Assemble the dictionary for this spell
        spell_dict = {
            "name": name,
            "level": level,
            "desc": description_part
        }
        spells_list.append(spell_dict)
    for spell in spells_list:
        html_content += f"<dt><em><strong>{spell['name']}</strong></em> :</dt>  <dd> ‘Level : {spell['level']} {spell['desc']}’</dd>"
        html_content += " <br>"
    html_content=html_content.rstrip('br')
    html_content += '</dl>'
    return html_content

def parse_spell_slots_from_text(spell_slots):
    html_content = '<dl>'
    spell_slots_list = []
    spell_slot_entries = spell_slots.strip().split('\n\n')
    for entry in spell_slot_entries:
        
        if '0' not in entry:
            parts = entry.split(':')
            spell_slot_dict = {
                "level": parts[0],
                "number": parts[1]
        
        }
        
            spell_slots_list.append(spell_slot_dict)
    for spell_slot in spell_slots_list:
        html_content += f"<dt><em><strong>{spell_slot['level']}</strong></em>:</dt> <dd>‘{spell_slot['number']}’</dd>"
        html_content += " <br>"
    html_content=html_content.rstrip(' br')
    html_content += '</dl>'
    return html_content

def parse_legendary_action_from_text(legendary_actions):    
    html_content = '<dl>'
    parts = legendary_actions.split('\n\n')    
    description = parts[0].strip() 
    description = description + "<br>"
    print(f"Description : {description}")   
    actions_text = parts[1:]
    actions = ';'.join(actions_text)
    actions = actions.split(';')
    print(f"actions : {actions}")

    legendary_actions_dict = {
        "description": description,
        "actions":[]
    } 
    html_content += description
       # Process each action
    for action in actions:
        print(f"action to be parsed: {action}")
        action_split = action.split(':')
        print(f"Split Action : {action_split}")
        legendary_actions_dict['actions'].append({
            "name": action_split[0],
            "desc": action_split[1]
        })
    
    for action in legendary_actions_dict['actions']:
        print(action)
        html_content += f"<dt><em><strong>{action['name']}</strong></em>:</dt> <dd> ‘{action['desc']}’</dd>"
        html_content += " <br>"
    html_content=html_content.rstrip(' br')
    html_content += '</dl>'
    return html_content
   

