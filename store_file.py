from datasummarizer import DataSummarizer
from ImageStripper import download_image
from pathlib import Path
LOCAL_IMAGE_PATH = Path("output/images")
RELATIVE_IMAGE_PATH = Path("assets/images/posts")
def write_links_to_file(list_of_links, file_name):
    f = open("output/{}.html".format(file_name), "w")
    # fileheader = "<html><head></head><body>\n"
    # fileclosing = "</body></html>\n"
    fileheader = "<div>"
    fileclosing = "</div>"
    for dicti in list_of_links:
        dictionary = clean_dictionary(dicti)
        name = dictionary['title']
        name = name.replace(" ","%20")
        img_local_path = Path(RELATIVE_IMAGE_PATH, name)
        print(img_local_path)
        # Read the link, title and reviews and write to a file
        # str(dictionary["aff_link"].encode('ascii', 'ignore')
        fileheader += "<h3>"+dictionary['title']+"</h3>\n"
        fileheader += f"<p>Check out the product <a href=\"{dictionary['link']}\"> here</a></p>\n"
        fileheader += f"<p>Price {dictionary['price']} here</p>\n"
        fileheader += f"TABLE \n <table>{dictionary['table']}</table>\n"
        try:
            exte = download_image(dictionary['img_link'], Path(LOCAL_IMAGE_PATH, name))
            # Neccessarily add a download and extract section here
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
