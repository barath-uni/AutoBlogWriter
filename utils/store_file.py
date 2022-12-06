import json
from gptgenerator.datasummarizer import DataSummarizer
from pipeline.review.ImageStripper import download_image
from pathlib import Path
from pipeline.imagegen.stableDiffusionImageGenerator import create_hero_image
POST_WRITE_PATH=Path("/home/barath/codespace/coolerssstack/_posts")
LOCAL_IMAGE_PATH = Path("/home/barath/codespace/coolerssstack/public")
RELATIVE_IMAGE_PATH = Path("assets/images/posts")
def write_links_to_file(list_of_links, file_name):
    f = open("{}/{}.html".format(POST_WRITE_PATH, file_name), "w")
    # fileheader = "<html><head></head><body>\n"
    # fileclosing = "</body></html>\n"
    fileheader =    "--- \n"\
                   f"title: {file_name} \n"\
                    "description: basic \n"\
                    "category: FILL \n"\
                    "modified_date: September 6, 2022 2:33 PM \n"\
                    "date: September 6, 2022 2:33 PM \n"\
                    f"image: {create_hero_image(hero_image_prompt_builder())} \n"\
                    "---\n"
    fileheader += "<div>"
    fileclosing = "</div>"
    for dicti in list_of_links:
        dictionary = clean_dictionary(dicti)
        

        name = dictionary['title']
        name = name.replace(" ","_")
        img_local_path = Path(RELATIVE_IMAGE_PATH, name)
        print(img_local_path)
        
        fileheader += "<h3>"+dictionary['title']+"</h3>\n"
        if dictionary.get('question'):
            val = dictionary['question']
            fileheader += "<p>"+val.get('question')+"</p>"
            fileheader += "<p>"+val.get('answer')+"</p>"
        fileheader += f"\n <table>{dictionary['table']}</table>\n"
        try:
            exte = download_image(dictionary['img_link'], Path(LOCAL_IMAGE_PATH, RELATIVE_IMAGE_PATH, name))
            # Neccessarily add a download and extract section here
            fileheader += "<section class='text-gray-600 body-font overflow-hidden'>"\
  "<div class='container px-5 py-24 mx-auto'>"\
    "<div class='mx-auto flex flex-wrap border-a-8' id='ig8o'>"\
      f"<img alt='ecommerce' src='/{img_local_path}{exte}' alt='product image' rel='nofollow noopener sponsored' class='lg:w-1/2 w-full p-4 lg:h-auto h-64 object-cover object-center rounded'/>"\
      "<div class='lg:w-1/2 lg:pl-10 lg:py-6 mt-6 lg:mt-0'>"\
        f"<h4 class='text-gray-900 text-xl p-2 title-font font-medium mb-1'>{dictionary['title']}"\
        "</h4>"\
        "<form method='get' id='ixww' class='p-2'>"\
          f"<span class='title-font font-medium text-l p-2 text-gray-900'>₹ {dictionary['price']}</span>"\
          "<div class='flex'>"\
            f"<button type='submit' class='flex ml-auto text-white bg-indigo-500 border-0 p-2 focus:outline-none hover:bg-indigo-600 rounded'><a style='color:white' href=\"{dictionary['link']}\"> Amazon</a></button>"\
          "</div>"\
        "</form>"\
      "</div>"\
    "</div>"\
  "</div>"\
"</section>"
        except:
            print("Exception during downloading the image")
        try:
            description = DataSummarizer(str(dictionary['description'].encode('ascii', 'ignore')))
        except Exception as e:
            description = dictionary['description']
        fileheader += f"<p>{description}</p>\n"

        try:
            output = DataSummarizer(str(dictionary["reviews"].encode('ascii', 'ignore')))
        except Exception as e:
            print(e)
            output = str(dictionary["reviews"].encode('ascii', 'ignore'))
        fileheader += "<p>"+output+"</p>\n"

    fileheader += fileclosing

    f.write(fileheader)

def clean_dictionary(dicti):
    title = dicti['title']
    # clean title for easier reading
    clean_title = title[:20]
    dicti['title'] = clean_title
    # Heuristics to weed out unwanted products :TODO
    return dicti


def hero_image_prompt_builder(keyword=""):
  #  high detail render, Emulating Reality ,f/ 4.2 , 250 mm lens,becoming the subject extreme wide shot, accurate features, high detailed light refraction, Emulating reality, high level texture render, low focus point
  return f"{keyword}, Neat Home, with Sofa, air cooler, mat on the floor, photo realistic,4K HD, High Detail, accurate features, "

def write_gpt_content_to_file(keyword:str, json_file:Path):
  """
  This function is responsible for writing a GPT content to a file. 
  Just convert dict to an HTML file and write to OUT
  Future changes, this should not be a separate flow, combine both the dictionaries into one file.
  In each dictionary
  1. Title
  2. Content (h3, p) -> Has its own pipeline, Could be review content+gpt content+comparison Phrases+Pre-determined phrases etc
  3. Hero image
  4. Content images - Ideally a table comparison image, etc
  5. Dall-e Images to plug in-between content 
  """
  with open(json_file, 'r') as f:
    dictionary_val = json.load(f)
  for dict_key in dictionary_val.keys():
    file_name = f"gpt_content_{dict_key[:10].replace(' ', '_')}"
    f = open("output/{}.html".format(file_name), "w")
      # fileheader = "<html><head></head><body>\n"
      # fileclosing = "</body></html>\n"
    fileheader =    "--- \n"\
                    "title: TITLE \n"\
                    "description: basic \n"\
                    "category: FILL \n"\
                    "modified_date: September 6, 2022 2:33 PM \n"\
                    "date: September 6, 2022 2:33 PM \n"\
                    f"image: {create_hero_image(hero_image_prompt_builder())} \n"\
                    "---\n"
    fileheader += "<div>"
    fileheader += f"\n<h1>{dict_key}</h1>"
    fileclosing = "</div>"
    for section in dictionary_val[dict_key]:
      fileheader += f"<h3>{section}</h3>"
      fileheader += f"<p>{dictionary_val[dict_key][section]}</p>"
    fileheader += fileclosing
    f.write(fileheader)
