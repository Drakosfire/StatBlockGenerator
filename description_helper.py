import replicate
import ast
import gc
import os
from openai import OpenAI

api_key = os.getenv('REPLICATE_API_TOKEN')
client = OpenAI()

def load_llm(user_input, spellcaster, legendary_actions ):
    prompt = f"the subject is {user_input}, Spellcaster : {spellcaster}, Legendary Actions : {legendary_actions}"
    print(prompt)
    response = client.chat.completions.create(            
                    model="gpt-4o",
                    messages=[
                        {
                        "role": "user",
                        "content": f"{prompt_instructions} {prompt}"
                        }
                    ],
                    temperature=1,
                    max_tokens=2000,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
    
    return response.choices[0].message.content

model_path = "meta/meta-llama-3-70b-instruct"
#def load_llm(user_input, spellcaster, legendary_actions):
 # prompt = f"the subject is {user_input}, Spellcaster : {spellcaster}, Legendary Actions : {legendary_actions}"
  #input = {"prompt" : f" {prompt_instructions} {prompt}","max_tokens":2000}
  #print(f"Generation Started, \n Prompt = {prompt}")
  #output = replicate.run(model_path,
  #input=input
  
   # )
  #return output
  

def call_llm_and_cleanup(user_input,spellcaster, legendary_actions):
    # Call the LLM and store its output
    llm_output = load_llm(user_input, spellcaster, legendary_actions)
    llm_output = "".join(llm_output)
    print(llm_output)
    llm_output = ast.literal_eval(llm_output)
    

    gc.collect()
  
    # llm_output is still available for use here
    
    return llm_output

  
def convert_to_dict(string):
    # Check if the input is already a dictionary
    if isinstance(string, dict):
        print("Input is already a dictionary.")
        return string

    # Function to try parsing the string to a dictionary
    def try_parse(s):
        try:
            result = ast.literal_eval(s)
            if isinstance(result, dict):
                print("Item dictionary is valid")
                return result
        except SyntaxError as e:
          error_message = str(e)
          print("Syntax Error:", error_message)
          # Check if the error message indicates an unclosed '{'
          if "'{' was never closed" in error_message:
              return try_parse(s + '}')  # Attempt to fix by adding a closing '}'
        except ValueError as e:
            print("Value Error:", e)
        return None 

    # First, try parsing the original string
    result = try_parse(string)
    if result is not None:
        return result

    # Check if braces are missing
    if not string.startswith('{'):
        string = '{' + string
    if not string.endswith('}'):
        string = string + '}'

    # Try parsing again with added braces
    return try_parse(string) or "Dictionary not valid"
        
  

# Instructions past 4 are not time tested and may need to be removed.
### Meta prompted : 
prompt_instructions = """ **Purpose**: ONLY Generate a structured json following the provided format. The job is to generate a balance, creative, interesting monster statblock in the rule style of Dungeons and Dragons. You do not need to stick strictly to the abilities and spells of the game, if it fits the style and flavor of the user input, get weird, scary, or silly with the details. You will also be writing a paragraph of interesting flavor text and description, and a brief one sentence image generation prompt.Include the type and subtype in the image prompt.

Image Generation Prompt Examples :
"A hooded stout dwarf necromancer, in black robes, emanating evil magic "
"A black and tan battle dog with spike collar, hackles up and ready to strike"
"a tanned human barbarian with bleeding red axes"
"a magical zombie tiger, colorful and decaying"

1. Only output file structure starting with { and ending with } it is CRITICAL to end with a }, DO NOT say anything, don't add ''' or json"
2. You tend to build over powered monsters, tend towards average to a bit underpowered. Damage Resistance can be left blank.
3. All Actions should have explicit instructions on how to use and what dice and effects they have
4. DO NOT type other_sense_type, other_skill_type or any other label or item.
5. DO NOT use null, use "".
5. If Spellcaster : False then Spells should not be printed. If Spellcaster 
6. If Legendary Actions : False then legendary_action should not be printed
7. Review and stick closely to this table.

Monster Statistics by Challenge Rating
Fractions MUST be surrounded by double quotes ""
| CR | XP | Prof. Bonus | Armor Class | Hit Points | Attack Bonus | Damage/Round | Save DC | Prob. of Spell | Num. of Spells | Level of Spells | Prob. of Legendary Actions | Num. of Legendary Actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 10 | 2 | 10-13 | 1-3 | 3 | 0-1 | 13 | 0% | 0 | - | 0% | 0 |
| "1/8" | 25 | 2 | 10-13 | 2-7 | 3 | 2-3 | 13 | 05% | 1 | 1st | 0% | 0 |
| "1/4" | 50 | 2 | 10-13 | 4-8 | 3 | 4-5 | 13 | 10% | 2 | 1st | 0% | 0 |
| "1/2" | 100 | 2 | 10-13 | 5-11 | 3 | 6-8 | 13 | 15% | 3 | 1st | 0% | 0 |
| 1 | 200 | 2 | 10-13 | 8-20 | 3 | 9-14 | 13 | 15% | 4 | 1st | 0% | 0 |
| 2 | 450 | 2 | 11-13 | 15-30 | 3 | 15-20 | 13 | 20% | 5 | 2nd | 0% | 0 |
| 3 | 700 | 2 | 11-13 | 25-50 | 4 | 21-26 | 13 | 25% | 6 | 2nd |05% | 1 |
| 4 | 1100 | 2 | 11-14 | 35-75 | 5 | 27-32 | 14 | 30% | 7 | 2nd | 10% | 1 |
| 5 | 1800 | 3 | 12-15 | 45-95 | 6 | 33-38 | 15 | 50% | 8 | 3rd | 10% | 1 |
| 6 | 2300 | 3 | 12-15 | 60-110 | 6 | 39-44 | 15 | 60% | 9 | 3rd | 15% | 2 |
| 7 | 2900 | 3 | 12-15 | 70-140 | 6 | 45-50 | 15 | 75% | 10 | 3rd | 20% | 2 |
| 8 | 3900 | 3 | 13-16 | 80-160 | 7 | 51-56 | 16 | 90% | 11 | 4th | 20% | 3 |
| 9 | 5000 | 4 | 13-16 | 105-205 | 7 | 57-62 | 16 | 90% | 12 | 4th | 20% | 3 |
| 10 | 5900 | 4 | 14-17 | 206-220 | 7 | 63-68 | 16 | 100% | 13 | 4th | 30% | 3 |
| 11 | 7200 | 4 | 14-17 | 221-235 | 8 | 69-74 | 17 | 100% | 14 | 5th | 40% | 3 |
| 12 | 8400 | 4 | 14-17 | 236-250 | 8 | 75-80 | 18 | 100% | 15 | 6th | 60% | 4 |
| 13 | 10000 | 5 | 15-18 | 251-265 | 8 | 81-86 | 18 | 100% | 16 | 7th | 80% | 4 |
| 14 | 11500 | 5 | 15-18 | 266-280 | 8 | 87-92 | 18 | 100% | 17 | 7th | 100% | 4 |
| 15 | 13000 | 5 | 15-18 | 281-295 | 8 | 93-98 | 18 | 100% | 18 | 8th | 100% | 5 |
| 16 | 15000 | 5 | 15-18 | 296-310 | 9 | 99-104 | 18 | 100% | 19 | 8th | 100% | 5 |
| 17 | 18000 | 6 | 16-19 | 311-325 | 10 | 105-110 | 19 | 100% | 20 | 8th | 100% | 5 |
| 18 | 20000 | 6 | 16-19 | 326-340 | 10 | 111-116 | 19 | 100% | 21 | 9th | 100% | 5 |
| 19 | 22000 | 6 | 16-19 | 341-355 | 10 | 117-122 | 19 | 100% | 22 | 9th | 100% | 5 |
| 20 | 25000 | 6 | 16-19 | 356-400 | 10 | 123-140 | 19 | 100% | 23 | 9th | 100% | 5 |
| 21 | 33000 | 7 | 16-19 | 401-445 | 11 | 141-158 | 20 | 100% | 24 | 9th | 100% | 5 |
| 22 | 41000 | 7 | 16-19 | 446-490 | 11 | 159-176 | 20 | 100% | 25 | 9th | 100% | 5 |
| 23 | 50000 | 7 | 16-19 | 491-535 | 11 | 177-194 | 20 | 100% | 26 | 9th | 100% | 5 |
| 24 | 62000 | 7 | 16-19 | 536-580 | 11 | 195-212 | 21 | 100% | 27 | 9th | 100% | 5 |
| 25 | 75000 | 8 | 16-19 | 581-625 | 12 | 213-230 | 21 | 100% | 28 | 9th | 100% | 5 |
| 26 | 90000 | 8 | 16-19 | 626-670 | 12 | 231-248 | 21 | 100% | 29 | 9th | 100% | 5 |
| 27 | 105000 | 8 | 16-19 | 671-715 | 13 | 249-266 | 22 | 100% | 30 | 9th | 100% | 5 |
| 28 | 120000 | 8 | 16-19 | 716-760 | 13 | 267-284 | 22 | 100% | 31 | 9th | 100% | 5 |
| 29 | 135000 | 9 | 16-19 | 760-805 | 13 | 285-302 | 22 | 100% | 32 | 9th | 100% | 5 |
| 30 | 155000 | 9 | 16-19 | 805-850 | 14 | 303-320 | 23 | 100% | 33 | 9th | 100% | 5 |

8. If a creature has Legendary Actions they need to be fully described. 
Example : "legendary_actions": {
    "actions": "Hermione the Grumpy can take 3 legendary actions, choosing from the options below. Only one legendary action can be used at a time and only at the end of another creature's turn. Hermione regains spent legendary actions at the start of her turn.",
    "options": [
      {
        "name": "Imperial Claw Strike",
        "desc": "With a swift motion that belies her regal composure, Hermione unsheathes her gleaming claws, striking with the precision of a seasoned sovereign. She makes one attack with her claws that deal an extra 2d6 slashing damage. If the attack hits a creature, that creature also suffers a -2 penalty to AC until the start of Hermione's next turn, as her claws leave rending tears in their armor or flesh, symbolizing her disdain for any challenge to her rule."
      },
      {
        "name": "Royal Command",
        "desc": "Hermione gazes across the battlefield, her eyes glowing with an ethereal light. She issues a commanding meow that resonates with arcane power. All creatures within 60 feet that can hear her must succeed on a DC 20 Wisdom saving throw or become charmed by Hermione for 1 minute. A charmed creature regards Hermione as its beloved monarch and will protect her as if it were guarding its own life. This charm effect ends if the charmed creature suffers any harm or if Hermione dismisses it as unworthy with a wave of her paw."
      },
      {
        "name": "Divine Whisker Quiver",
        "desc": "Hermione channels the cosmic power of her royal lineage through her whiskers, which quiver with the energy of the universe itself. She chooses up to three creatures she can see within 100 feet of her. Each target must succeed on a DC 18 Constitution saving throw or be stunned by the overwhelming presence of the Empress until the end of their next turn. Creatures that fail their saving throw by 5 or more are also teleported up to 30 feet in any direction Hermione chooses, as she rearranges the battlefield to her liking with but a thought."
      }
    ] 


Output format : 
{
  "name": "",
  "size": "",
  "type": "",
  "subtype": "",
  "alignment": "",
  "armor_class": ,
  "hit_points": ,
  "hit_dice": "",
  "speed": {
    "walk": 
    
  },
  "abilities": {
    "str": ,
    "dex": ,
    "con": ,
    "int": ,
    "wis": ,
    "cha":
  },
  "saving_throws": {
    "str": ,
    "dex": ,
    "wis":
  },
  "skills": {
    "perception": 
  },
  "damage_resistance": 
  "senses": {
    "darkvision": 
  },
  "languages": "",
  "challenge_rating": ,
  "xp": ,
  "actions": [
    {
      "name": "",
      "desc": ""
    }
  ],
  "spells": {
    "cantrips": [
      {
        "name": "",
        "desc": ""
      }
    ],
    "known_spells": [
      {
        "name": "",
        "level":"",
        "desc": ""
      }
    ],
    "spell_slots": {
      "1st_level": ,
      "2nd_level": ,
      "3rd_level": ,
      "4th_level": ,
      "5th_level": ,
      "6th_level": ,
      "7th_level": ,
      "8th_level": ,
      "9th_level":
    }
  },
  "legendary_actions": {
    "actions": ,
    "options": [
      {
        "name": "",
        "desc": ""
      }
    ]
  },
  "description":"",
  "sd_prompt":""
}
"""
