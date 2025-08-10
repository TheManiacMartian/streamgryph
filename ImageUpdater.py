import requests
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image
import re
import os


ValMap = "https://valorant-api.com/v1/maps"
ValChar = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"

OWMap = "https://overfast-api.tekrop.fr/maps"
OWChar = "https://overfast-api.tekrop.fr/heroes"

MrMap = "https://marvelsapi.com/api/maps"
MrChar = "https://marvelsapi.com/api/heroes"

API_URL = "blank"
Image_Title = "blank"

ValRoles = ["duelist", "initiator", "sentinel", "controller"]
OWRoles = ["tank", "damage", "support"]
MRRoles = ["vanguard","duelist","strategist"]

char_to_role = []
canvas_size = (1368, 1368)

def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def process_image(url, output_filename, top, left):
    response = requests.get(url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    
    # Scale down the image to make it appear more zoomed out
    scale_factor = 0.8  # Make image 70% of original size (adjust as needed)
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))  # Transparent background
    img_width, img_height = img.size
    x = ((canvas_size[0] - img_width) // 2) + left  # Center horizontally
    y = 0 + top  # Top of canvas
    canvas.paste(img, (x, y), img.convert("RGBA"))
    canvas.save(output_filename)

def main():
    global API_URL, Image_Title, char_to_role

    while True:
        print("""what would you like the update? (1 - 8):
            1: Valorant Maps
            2: Valorant Agents
            3: Overwatch Maps
            4: Overwatch Heroes
            5: Marvel Rivals Maps
            6: Marvel Rivals Heroes
            7: League Champs
            8: Exit\n""")
        
        choice = int(input("Enter your choice: "))

        # Pramaeters for each game
        match(choice):
            case 1: 
                API_URL = ValMap
                Image_Title = "listViewIconTall"
                top = 0
                left = 0
            case 2:
                API_URL = ValChar
                Image_Title = "fullPortrait"
                top = 50
                left = 100
            case 3:
                API_URL = OWMap
                Image_Title = "Screenshot"
                top = 150
                left = 0
            case 4:
                API_URL = OWChar
                Image_Title = "portrait"
                top = 150
                left = 0
            case 5:
                API_URL = MrMap
                Image_Title = "images"
                top = 150
                left = -200
            case 6:
                API_URL = MrChar
                top = 150
                left = 50
            case 7:
                API_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
                versions = fetch_data()
                API_URL = f"https://ddragon.leagueoflegends.com/cdn/{versions[0]}/data/en_US/champion.json"
                left = 50
                top = 200
            case _:
                return

        # Create folder if it doesn't exist
        os.makedirs("Images", exist_ok=True)
        
        data = fetch_data()

        if choice == 7:
            call = data.get("data", {}).values()
        else:
            call = data if isinstance(data, list) else data.get("data", [])

        if not call:
            print("No Images found in API response.")
            return
        
        # Normal Calls
        print("[")
        if choice > 0 and choice < 6:
            for i, info in enumerate(call, start=1):

                if choice == 1 or choice == 2:
                    name = info.get("displayName", f"image_{i}")
                else:
                    name = info.get("name", f"image_{i}")
                name = name.replace("/","-")

                if choice == 2:
                    char_to_role.append(ValRoles.index(info.get("role",{}).get("displayName", "").lower()))
                if choice == 4:
                    char_to_role.append(OWRoles.index(info.get("role","").lower()))

                thumbnail_url = info.get(Image_Title)
                if not thumbnail_url:
                    print(f"No thumbnail URL for {name}, skipping...")
                    continue
                
                # Handle case where thumbnail_url is a list of URLs - take only the first one
                if isinstance(thumbnail_url, list):
                    if not thumbnail_url:  # Empty list
                        print(f"Empty thumbnail URL list for {name}, skipping...")
                        continue
                    thumbnail_url = thumbnail_url[0]  # Take only the first URL
                    # print(f"Found multiple images for '{name}', using first one")
                
                # print(f"Downloading thumbnail...")
                output_filename = os.path.join("Images", f"{name}.png")
                output_filename = output_filename.replace(":", "")
                try:
                    process_image(thumbnail_url, output_filename, top, left)
                    print(f'"{name}",')
                except Exception as e:
                    print(f"Error processing {name}: {e}")

        # Marvel Rivals Characters
        elif (choice == 6):
            for i, info in enumerate(call, start=1):
                name = info.get("name", f"image_{i}")

                api_name = name.replace(" ","-")
                api_name = api_name.replace("&-","")
                API_URL = f"https://marvelsapi.com/api/heroes/information/{api_name}".lower()
                
                character = fetch_data()
                thumbnail_url = character.get("image")

                char_to_role.append(MRRoles.index(character.get("role","").lower()))

                if not thumbnail_url:
                    print(f"No thumbnail URL for {name}, skipping...")
                    continue
                
                # Handle case where thumbnail_url is a list of URLs - take only the first one
                if isinstance(thumbnail_url, list):
                    if not thumbnail_url:  # Empty list
                        print(f"Empty thumbnail URL list for {name}, skipping...")
                        continue
                    thumbnail_url = thumbnail_url[0]  # Take only the first URL
                    # print(f"Found multiple images for '{name}', using first one")
                
                output_filename = os.path.join("Images", f"{name}.png")
                output_filename = output_filename.replace(":", "")
                try:
                    process_image(thumbnail_url, output_filename, top, left)
                    print(f'"{name}",')
                except Exception as e:
                    print(f"Error processing {name}: {e}")
        
        # League Characters
        elif (choice == 7):
            for i, info in enumerate(call, start=1):
                name = info.get("name", f"image_{i}")
                idName = info.get("id", f"image_{i}")
                thumbnail_url = f"http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{idName}_0.jpg"

                if not thumbnail_url:
                    print(f"No thumbnail URL for {name}, skipping...")
                    continue
                
                # Handle case where thumbnail_url is a list of URLs - take only the first one
                if isinstance(thumbnail_url, list):
                    if not thumbnail_url:  # Empty list
                        print(f"Empty thumbnail URL list for {name}, skipping...")
                        continue
                    thumbnail_url = thumbnail_url[0]  # Take only the first URL
                    # print(f"Found multiple images for '{name}', using first one")
                
                # print(f"Downloading thumbnail...")
                output_filename = os.path.join("Images", f"{name}.png")
                output_filename = output_filename.replace(":", "")
                try:
                    process_image(thumbnail_url, output_filename, top, left)
                    # print(f"Saved: {output_filename}")
                    print(f'"{name}",')
                except Exception as e:
                    print(f"Error processing {name}: {e}")

        print("]")        
        if choice == 2 or choice == 4 or choice == 6:
            print(f"{char_to_role}")
        char_to_role = []
        print("\n-------------------------------------------------\n")

if __name__ == "__main__":
    main()