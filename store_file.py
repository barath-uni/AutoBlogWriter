from datasummarizer import DataSummarizer

def write_links_to_file(list_of_links, file_name):
    print("INTERESTING")
    f = open("output/{}.html".format(file_name), "w")
    fileheader = "<html><head></head><body>\n"
    fileclosing = "</body></html>\n"
    for dicti in list_of_links:
        print(dicti)
        dictionary = clean_dictionary(dicti)
        # Read the link, title and reviews and write to a file
        # str(dictionary["aff_link"].encode('ascii', 'ignore')
        fileheader += "<h3>"+dictionary['title']+"</h3>\n"
        fileheader += f"<p>Check out the product <a href=\"{dictionary['link']}\"> here</a></p>\n"
        fileheader += f"<p>Price {dictionary['price']} here</p>\n"
        fileheader += f"TABLE \n <table>{dictionary['table']}</table>\n"
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
        fileheader += "<div>"+output+"</div>\n"

    fileheader += fileclosing

    f.write(fileheader)

def clean_dictionary(dicti):
    title = dicti['title']
    # clean title for easier reading
    clean_title = title[:20]
    dicti['title'] = clean_title
    # Heuristics to weed out unwanted products :TODO
    return dicti
