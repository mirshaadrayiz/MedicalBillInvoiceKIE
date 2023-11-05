import re
import numpy as np
from collections import defaultdict
from base_functions import calculate_centroid


def identify_table(txts,boxes,ymax_header):

    table_boxes = []
    table_text = []

    index_table_bot = 0

    ymin_table = ymax_header
    pattern = r"\b(?i)Total\b"
    
    # Iterate through the list of words and search for the pattern
    ymax_table = 0
    
    for index,word in enumerate(txts):
        if re.search(pattern, word):
            if boxes[index][1][1] > ymax_table:
                ymax_table = boxes[index][1][1]

    for box,text in zip(boxes,txts):
        if box[1][1] > ymin_table - 10 and box[1][1] < ymax_table:
            
            table_boxes.append(box)
            table_text.append(text)
    
    return table_text, table_boxes, ymin_table


def find_description_items(table_text, table_boxes):
    
    description_text = []
    description_boxes = []
    to_remove_indices = []
 
    
    try:
        index = next((i for i, text in enumerate(table_text) if 'DESCRIPTION' in text.upper()), None)
        if index is not None:
            bounding_box_desc = table_boxes[index]
            description = table_text[index]
        else:
            print("'DESCRIPTION' not found in the list of texts.")
    except ValueError:
        print("'DESCRIPTION' not found in the list of texts.")

    xleft_description = bounding_box_desc[3][0]
    xright_description = bounding_box_desc[2][0]

    table_text.pop(index)
    table_boxes.pop(index)

    table_text_copy = table_text.copy()
    table_boxes_copy= table_boxes.copy()

    for index,box in enumerate(table_boxes):
        if box[3][0] > xleft_description-20 and box [3][0] < xright_description:
            description_text.append(table_text[index])
            description_boxes.append(box)
            to_remove_indices.append(index)

    # Remove the appended values from the original lists
    for j in reversed(to_remove_indices):
        del table_text_copy[j]
        del table_boxes_copy[j]
    
    return description, description_text, description_boxes, table_text, table_boxes, bounding_box_desc


def find_table_titles(bounding_box_desc,table_text,table_boxes):
    
    desc_centroid = calculate_centroid(bounding_box_desc)
    other_centroids = [calculate_centroid(box) for box in table_boxes]

    title_text = []
    title_boxes = []
    to_remove_indices = []

    for index, centroid in enumerate(other_centroids):
        ymin = abs(desc_centroid[1] - centroid[1])
        if ymin < 10:
            title_text.append(table_text[index])
            title_boxes.append(table_boxes[index])
            to_remove_indices.append(index)
            
    # Remove the appended values from the original lists
    for j in reversed(to_remove_indices):
        del table_text[j]
        del table_boxes[j]
        
    
    return title_text, title_boxes, table_text, table_boxes

def find_description_siblings(table_text, table_boxes, title_text, title_boxes, description_text, description_boxes, description):


    xleft = [] #Creating an empty list to store x-right coordinates of the titles except description
    xright = [] #Creating an empty list to store x-right coordinates of the titles except description

    #Function to iterate and find the x-left and x-right coordinates
    for column in range(len(title_text)):
        xleft.append(title_boxes[column][3][0])
        xright.append(title_boxes[column][2][0])

    #Calculating centroids for all description texts
    descript_centroids = [calculate_centroid(box) for box in description_boxes]
    #Calculating centroids for all other texts
    other_centroids = [calculate_centroid(box) for box in table_boxes]

    line_values_dict = defaultdict(list)
    line_values_dict[description] = description_text ## Adding title description to the description as a key

    ##Adding other titles to the dictionary as keys
    for i in range(1,len(title_text)+1):
        line_values_dict[title_text[i-1]] = []
        
    ##iterating through each description text attempting to find its siblings
    for index, desc_centroid in enumerate(descript_centroids):
        
        ##To keep track of the columns to which values were appended
        flags = np.zeros(len(title_text)) 
        
        for index1, centroid in enumerate(other_centroids):
            ymin = abs(desc_centroid[1] - centroid[1])
            if ymin < 8:

                #Iterating through the table columns
                for index2,title in enumerate(title_text): 

                    #Checking if the detected centroid falls within a column 
                    if centroid[0] > xleft[index2] and centroid[0] < xright[index2]: 
                        
                        #If yes, add it to that column
                        line_values_dict[title].append(table_text[index1]) 
                        flags[index2] = 1

        #Find columns that did not get a centroid for this line and add "Not Found"
        for i, flag in enumerate(flags):     
            if flag == 0:
                line_values_dict[title_text[i]].append("Not Found")
   


    return line_values_dict

def find_line_items(txts, boxes, ymax_header):

    table_text, table_boxes, ymin_table = identify_table(txts,boxes,ymax_header) #Identify the table segment of the image

    #Identify and extract description column coordinates and related items
    description, description_text, description_boxes, table_text, table_boxes, bounding_box_desc = find_description_items(table_text, table_boxes)

    #Identify and extract other table coumns
    title_text, title_boxes, table_text, table_boxes = find_table_titles(bounding_box_desc,table_text,table_boxes)

    #Obtain a dictionaru with keys as titles with lists of values for each key
    line_values = find_description_siblings(table_text, table_boxes,title_text, title_boxes, description_text, description_boxes, description)

    return line_values