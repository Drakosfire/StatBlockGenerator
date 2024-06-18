
#Function to process text from Key Value pairs into User Friendly text

def format_mon_qualities(qualities):
    formatted_text = ""
    for key, value in qualities.items():
        formatted_text += f" {key} : {value}, "
    formatted_text = formatted_text.rstrip(", ")
    return formatted_text

def format_actions_for_editing(actions):
    formatted_text = ""
    for action in actions:
        formatted_text += f"Action Name: {action['name']}; Description: {action['desc']} \n\n"
    formatted_text = formatted_text.rstrip(", ")
    return formatted_text

def format_abilities_for_editing(abilities):
    formatted_text = ""
    key_list = list(abilities)
    for key in key_list:        
        formatted_text += f"{key} : {abilities[key]}\n"
    return formatted_text

def format_spells_for_editing(spells):
    print(f"Spells in format_spells function : {spells}")
    formatted_cantrips = ""
    formatted_spells = ""
    formatted_spell_slots = ""
    if spells['cantrips'] and len(spells['cantrips']) >= 1: 
        print(f"Cantrips : {spells['cantrips']}")
        formatted_cantrips += "Cantrips \n\n"
        for cantrip in spells['cantrips']:
            formatted_cantrips += f"{cantrip['name']}; Description: {cantrip['desc']}, \n\n"
    if spells['known_spells'] and len(spells['known_spells']) >= 1:
        formatted_spells += "Known Spells \n\n"
        for spell in spells['known_spells']:
            formatted_spells += f"{spell['name']}; Level: {spell['level']}, Description: {spell['desc']}, \n\n"
    if spells['spell_slots'] and len(spells['spell_slots']) >= 1:
        print (f"Spell Slots : {spells['spell_slots']}")
        formatted_spell_slots += "Spell Slots \n\n"
        for key, value in spells['spell_slots'].items():
            if value != 0:
                formatted_spell_slots += f"{key.replace('_',' ')}: {value}, \n\n"
    formatted_cantrips = formatted_cantrips.rstrip(", ")
    formatted_spells = formatted_spells.rstrip(", ")
    formatted_spell_slots = formatted_spell_slots.rstrip(", ")
    return formatted_cantrips, formatted_spells, formatted_spell_slots

def format_legendaries_for_editing(legendary_actions):
    formatted_text = ""
    if legendary_actions['actions'] and len(legendary_actions['actions']) >= 1:
        formatted_text += "Legendary Actions \n\n"
        formatted_text += f"{legendary_actions['actions']} \n\n"
    if legendary_actions['options']:
        for option in legendary_actions['options']:
          formatted_text += f"{option['name']} : {option['desc']}, \n\n"
    formatted_text = formatted_text.rstrip(", \n\n")
    return formatted_text

