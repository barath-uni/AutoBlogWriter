from datasummarizer import DataSummarizer
from ImageStripper import download_image
from pathlib import Path
LOCAL_IMAGE_PATH = Path("output/images")
RELATIVE_IMAGE_PATH = Path("assets/images/posts")
def write_links_to_file(list_of_links, file_name):
    f = open("output/{}.html".format(file_name), "w")
    # fileheader = "<html><head></head><body>\n"
    # fileclosing = "</body></html>\n"
    fileheader =    " --- \n"\
                    "title: TITLE \n"\
                    "description: basic \n"\
                    "category: FILL \n"\
                    "modified_date: TITLE \n"\
                    "date: TITLE \n"\
                    "image: https://dummyimage.com/1048x600 \n"\
                    "---\n"
    fileheader += "<div>"
    fileclosing = "</div>"
    for dicti in list_of_links:
        dictionary = clean_dictionary(dicti)
        

        name = dictionary['title']
        name = name.replace(" ","_")
        img_local_path = Path(RELATIVE_IMAGE_PATH, name)
        print(img_local_path)
        # Read the link, title and reviews and write to a file
        # str(dictionary["aff_link"].encode('ascii', 'ignore')
        fileheader += "<h3>"+dictionary['title']+"</h3>\n"
        if dictionary.get('questions'):
            fileheader += "<p>"+dictionary['questions']+"</p>"
        fileheader += f"<p>Check out the product <a href=\"{dictionary['link']}\"> here</a></p>\n"
        fileheader += f"<p>Price {dictionary['price']} here</p>\n"
        fileheader += f"TABLE \n <table>{dictionary['table']}</table>\n"
        try:
            exte = download_image(dictionary['img_link'], Path(LOCAL_IMAGE_PATH, name))
            # Neccessarily add a download and extract section here
            fileheader += "<section class='text-gray-600 body-font overflow-hidden'>"\
  "<div class='container px-5 py-24 mx-auto'>"\
    "<div class='mx-auto flex flex-wrap' id='ig8o'>"\
      f"<img alt='ecommerce' src='/{img_local_path}{exte}' alt='product image' class='lg:w-1/2 w-full lg:h-auto h-64 object-cover object-center rounded'/>"\
      "<div class='lg:w-1/2 lg:pl-10 lg:py-6 mt-6 lg:mt-0'>"\
        f"<h1 class='text-gray-900 text-3xl title-font font-medium mb-1'>{dictionary['title']}"\
        "</h1>"\
        "<form method='get' id='ixww'>"\
          "<span class='title-font font-medium text-2xl text-gray-900'>Check price</span>"\
          "<div class='flex'>"\
            "<button type='submit' class='flex ml-auto text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded'>Amazon</button>"\
          "</div>"\
        "</form>"\
      "</div>"\
    "</div>"\
  "</div>"\
"</section>"
            fileheader += f"<img class='object-cover object-center rounded' src='/{img_local_path}{exte}' alt='product image'> \n"
        except:
            print("Exception during downloading the image")
        try:
            description = DataSummarizer(str(dictionary['description'].encode('ascii', 'ignore')))
        except Exception as e:
            description = dictionary['description']
        fileheader += f"<p>Description = {description}</p>\n"

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
