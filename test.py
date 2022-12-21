import re

para_text="""

First create a 7 paragraph article outline:

Paragraph 1: Introduction

Paragraph 2: Types of Coolers
-Passive Coolers
-Thermoelectric Coolers
-Absorption Coolers
-Compressor Coolers

Paragraph 3: How to Choose a Cooler
-Size and Capacity
-Features
-Type of cooler

Paragraph 4: Passive Coolers 
-Evaporative coolers 
-Peltier coolers 
-Phase change coolers 
Paragraph 5: Thermoelectric Coolers  
- advantages and disadvantages  
Paragraph 6: Absorption Coolers  

 -advantages and disadvantages
"""
# python 3
text="""
Introduction

There are different types of coolers on the market and each one has its own advantages and disadvantages. In this article, we will take a look at the four main types of coolers: passive, thermoelectric, absorption, and compressor coolers.

How to Choose a Cooler

Coolers come in all shapes and sizes and it can be hard to decide which one is right for you. When choosing a cooler, you need to consider the following factors: size and capacity, features, and type of cooler.

Passive Coolers

The first type of cooler is the passive cooler. Passive coolers do not use any electricity and rely on natural methods to cool down the contents of the cooler. There are three types of passive coolers: evaporative, peltier, and phase change coolers.

Evaporative Coolers
Evaporative coolers use water to cool down the contents of the cooler. The water evaporates into the air and takes the heat with it, cooling down the contents of the cooler. Evaporative coolers are best for cooling down small spaces or personal items. They are not very effective at cooling down large spaces or objects.

Peltier Coolers
Peltier coolers work by transferring heat from one side of the device to the other. This allows them to create a cold side and a hot side. Peltier coolers are not very efficient and can only produce a small amount of cold air. They are best used for cooling down small spaces or personal items.

Phase Change Coolers
Phase change coolers use a material that changes from a liquid to a solid in order to cool the contents of the cooler. This type of cooler is very effective at cooling down large spaces or objects. However, it is expensive and requires a lot of maintenance.

Thermoelectric Coolers

The second type of cooler is the thermoelectric cooler. Thermoelectric coolers use electricity to create a cold side and a hot side. This allows them to cool down the contents of the cooler. Thermoelectric coolers are more efficient than peltier coolers and can produce a greater amount of cold air. They are best used for cooling down large spaces or objects.

Absorption Coolers

The third type of cooler is the absorption cooler. Absorption coolers use a material that absorbs heat in order to create a cold side and a hot side. Absorption coolers are not as efficient as compressor coolers, but they are cheaper and do not require any electricity. They are best used for cooling down large spaces or objects.
"""
titles = re.findall(r'Paragraph \d+: (.*)', para_text)


def split_title_paragraph(text, titles):
    # split the text into lines
    lines = text.split("\n")
    # Go through each line      
    index = list()
    titles_ind_iter = 0
    for title_it, line in enumerate(lines):
        title = titles[titles_ind_iter]
        # Match the index
        if title in line:
            index.append(title_it)
            try:
                title = titles[titles_ind_iter+1]
            except StopIteration as e:
                print("End")
        else:

            # Check if any other title after this titles_ind_iter is present
            titles_to_check = titles[titles_ind_iter+1:]
            print("titles")
            print(titles_to_check)
            for i, tit in enumerate(titles_to_check):
                if tit in line:
                    title_gap = True
                    index.append(title_it)
                    titles_ind_iter = titles_ind_iter+1+i
                    break


    # Check the length of index
    if len(index) < len(titles):
        all_title_present = False
        print("NOT ALL TITLES ARE PRESENT. Partially Built or the format has changed.")
    else:
        all_title_present = True
    title_paragraph = dict()
    print(index)
    # Loop through the indexes that match and get value between index[i] and index[i+1]
    for i in range(len(index)):
        index_val = index[i]
        if i+1 == len(index):
            title_paragraph[lines[index_val]] = lines[index_val+1:]
        else:
            title_paragraph[lines[index_val]] = lines[index_val+1:index[i+1]]
    return title_paragraph, all_title_present, title_gap
titles = [title.strip() for title in titles]
print(titles)
title_para, all_til, tg = split_title_paragraph(text, titles)
import json

with open(f'sometopic.json', 'w') as f:
    json.dump(title_para, f)
