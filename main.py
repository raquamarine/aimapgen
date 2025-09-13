from google import genai
from google.genai import types
import os
apikey = input("Insert your Gemini API key: ")
client = genai.Client(api_key=apikey)

modelnum = int(input("Select AI model: 1 - gemini-2.5-pro, 2 - gemini-2.5-flash, 3 - gemini-2.0-flash \n"))
if modelnum == 1:
    modelselected = "gemini-2.5-pro"
elif modelnum == 2:
    modelselected = "gemini-2.5-flash"
elif modelnum == 3:
    modelselected = "gemini-2.0-flash"
else:
    print("Wrong number")
    exit()

#open the example file
example_vmf_path = "AImapExample.vmf"
with open(example_vmf_path, "r", encoding="utf-8") as f:
    vmf_contents = f.read()

gameselected = "Team Fortress 2" #fallback if no game is selected
gameselectedask = int(input("Select Game: 1 - TF2. 2 - HL2. 3 - Portal 1. 4 - Portal 2 \n"))
if gameselectedask == 1:
    gameselected = "Team Fortress 2"
elif gameselectedask == 2:
    gameselected = "Half life 2"
elif gameselectedask == 3:
    gameselected = "Portal 1"
elif gameselectedask == 4:
    gameselected = "Portal 2"
else:
    print("Wrong Number")
    exit()


maptopic = input("Insert map topic (leave blank for none): \n")

aitemperature = int(input("Insert the temperature for the AI prompt (must be a number between 0 and 2): \n"))

mustincludeask = input("Insert something the AI must include (leave blank for none): \n")
if mustincludeask == "":
    mustinclude = ""
else:
    mustinclude = "and You MUST include a " + mustincludeask + ""

print("Generating map (may take a while)...")

prompt = (
                    f"You are now a VMF map generator for {gameselected}. "
                    "Your task is to create a new VMF map that is playable \n"
                    f"The theme of the map is: {maptopic}. "
                    "Keep the layout large and varied. "
                    "Do not keep it minimal—make the map feel expansive rather than small\n"
                    "Technical requirements:\n"
                    "- All VMF brushes must be valid.\n"
                    "- No unused or placeholder visgroups.\n"
                    "- If you include a gametext, make it ALL CAPS and make the text laconic and concise.\n"
                    "- Use:\n"
                    "  - editorversion 400\n"
                    "  - editorbuild 3325\n"
                    "  - mapversion 0\n"
                    "  - formatversion 100\n"
                    "- Ensure all solids are valid.\n\n"
                    "Follow this guideline for structure:\n"
                    "- A VMF file begins with 'versioninfo', 'visgroups', 'viewsettings', and 'world'.\n"
                    "- 'world' contains brushes defined as 'solid' blocks with valid planes, sides, and texture assignments.\n"
                    "- Entities follow the structure:\n"
                    "  entity\n"
                    "  {\n"
                    "    \"id\" \"X\"\n"
                    "    \"classname\" \"classname_here\"\n"
                    "    \"origin\" \"X Y Z\"\n"
                    "  }\n"
                    "- Displacements are defined inside 'side' blocks with 'dispinfo'.\n"
                    "- Each solid must close correctly with braces and contain only valid sides.\n\n"
                    "Output only the VMF code. No commentary, no backticks, no explanations."
                )

content_chat = [
    types.Part(text=vmf_contents),
    types.Part(text=prompt)
]
response = client.models.generate_content(model=modelselected,
                                          contents=content_chat,
                                          config=types.GenerateContentConfig(
                                            temperature=aitemperature
                                          ))


def get_next_map_filename(directory="maps", prefix="map", extension=".vmf"):
    # makes sure directory exists
    os.makedirs(directory, exist_ok=True)

    i = 1
    while True:
        filename = f"{prefix}{i}{extension}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1


wfilename = get_next_map_filename()

cleaned_text = response.text.replace("`", "")  # remove all backticks

print("Done!, Map saved as " + wfilename)
with open(wfilename, "w", encoding="utf-8") as file:
    file.write(cleaned_text)
    exit()

