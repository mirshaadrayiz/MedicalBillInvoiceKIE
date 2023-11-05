import re
import numpy as np
from collections import defaultdict
from base_functions import calculate_centroid, euclidean_distance
import parameters

##Function to identify the header segment of the invoice

def identify_header(txts,boxes):

    header_text = []
    header_boxes = []
    ymin_header = 0
    index_table = 0
    
    pattern = r"\b(Description|Amount|DESCRIPTION|AMOUNT)\b"
    
    # Iterate through the list of words and search for the pattern
    for word in txts:
        match = re.search(pattern, word)
        if match:
            index_header_bot = txts.index(word)
            break

    ymax_header = boxes[index_header_bot][1][1]

    for box,text in zip(boxes,txts):

        if box[1][1] > ymin_header and box[1][1] < ymax_header:
            header_boxes.append(box)
            header_text.append(text)
                
    return header_text, header_boxes, ymax_header

def find_key_vals_regex(txts, header_text, header_boxes):

    # Define the regex patterns for the items you want to search for
    patterns = [
        r"(?i)patient\s*name",
        r"(?i)patient\s*(national\s*ID|ID)",
        r"(?i)hospital",
        r"(?i)gst\s*(reg\s*No|No)",
        r"(?i)visit\s*date",
        "(?i)tax\s*invoice\s*date|invoice\s*date",
        r"(?i)(bill/|receipt\s*|bill\s*|receipt\s*date|bill\s*reference\s*number|bill\s*ref\s*(number|no)|bill\s*no|bill\s*number)",
        r"(?i)admission\s*date",
        r"(?i)discharge\s*date",
        r"(?i)(tax\s*invoice\s*number|invoice\s*no)",
        r"(?i)total\s*amount\s*payable",
        r"(?i)doctor\s*name",
        r"(?i)location",
        r"(?i)bill\s*type",
        r"(?i)(payment\s*class|class\s*of\s*payment)",
        r"(?i)(type\s*of\s*supply|supply\s*type)",
        r"(?i)patient\s*(nric/|nric\s*|hrn\s*)",
        r"(?i)mrn/nic",
        r"(?i)case\s*no(?:\.| |$)",
        r"(?i)case\s*number(?:\.| |$)"
    ]

    
    # Common key-value pair separators
    separators_to_check = [":", "=", "|", "-"]
    matches_text = []
    matches_boxes = []
    # Initialize a dictionary to store the key-value pairs
    key_value_pairs = {}
    
    # Search for matches in the list of words and store matches
    for pattern in patterns:
        regex_pattern = re.compile(pattern, re.IGNORECASE)
        for index,word in enumerate(header_text):
            if regex_pattern.search(word):
                if len(word.split())< parameters.max_keyword_length:
                    sep_flag = 0
                    for index2, separator in enumerate(separators_to_check):
                        if separator in word:
                            sep_flag = 1
                            key, value = map(str.strip, word.split(separator, 1))
                            key_value_pairs[key] = value
                        elif sep_flag == 0 and index2 == len(separators_to_check)-1:
                            matches_text.append(word)
                            matches_boxes.append(header_boxes[index])
  
    return matches_text, matches_boxes, key_value_pairs


def find_key_vals_boxes(matches_text,matches_boxes,header_text,header_boxes,key_value_pairs):
    
    ##Calculate centroids of each key bounding box
    key_centroids = [calculate_centroid(box) for box in matches_boxes] 
    
    ##Calculate centroids of each key bounding box
    other_centroids = [calculate_centroid(box) for box in header_boxes] 

    for index, centroid1 in enumerate(key_centroids):
        for index2, centroid2 in enumerate(other_centroids):
            ymin = abs(centroid1[1] - centroid2[1])
            xmin = abs(centroid1[0] - centroid2[0])
            if ymin < 8 and xmin > 1:
                key_value_pairs[matches_text[index]] = header_text[index2]

    # Iterate through the dictionary and update empty values to "Not Found"
    for key, value in key_value_pairs.items():
        if value in (None, ""):
            key_value_pairs[key] = "Not Found"
        
    return key_value_pairs

def find_key_value_pairs(txts,boxes):

    #Identify the header segment
    header_text, header_boxes, ymax_header = identify_header(txts,boxes)

    #Finding all possible key values using regex 
    matches_text, matches_boxes, key_value_pairs = find_key_vals_regex(txts,header_text,header_boxes)

    #Find rest of the key value pairs using box locations
    key_value_pairs = find_key_vals_boxes(matches_text,matches_boxes,header_text,header_boxes,key_value_pairs)
    
    return key_value_pairs,ymax_header
