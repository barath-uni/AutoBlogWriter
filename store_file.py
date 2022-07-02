def write_links_to_file(list_of_links, file_name):
    f = open("output/{}.html".format(file_name), "w")
    fileheader = "<html><head></head><body>"
    fileclosing = "</body></html>"
    for dictionary in list_of_links:
        print("DICTIONATRY")
        print(dictionary)
        # Read the link, title and reviews and write to a file
        # str(dictionary["aff_link"].encode('ascii', 'ignore')
        fileheader += "<h3>"+dictionary['title']+"</h3>"
        fileheader += "<h4>"+dictionary["link"]+"</h4>"
        fileheader += "<div>"+str(dictionary["reviews"].encode('ascii', 'ignore'))+"</div>"

    fileheader += fileclosing

    f.write(fileheader)
