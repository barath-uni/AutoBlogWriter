def write_links_to_file(list_of_links, file_name):
    f = open("output/{}.html".format(file_name), "w")
    fileheader = "<html><head></head><body>\n"
    fileclosing = "</body></html>\n"
    for dictionary in list_of_links:
        # Read the link, title and reviews and write to a file
        # str(dictionary["aff_link"].encode('ascii', 'ignore')
        fileheader += "<h3>"+dictionary['title']+"</h3>\n"
        fileheader += "<h4>"+dictionary["link"]+"</h4>\n"
        fileheader += "<div>"+str(dictionary["reviews"].encode('ascii', 'ignore'))+"</div>\n"

    fileheader += fileclosing

    f.write(fileheader)
