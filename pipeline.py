import fitz  
from PIL import Image
import numpy as np
from base_functions import apply_ocr
from key_value import find_key_value_pairs
from line_items import find_line_items
from json_func import add_to_json
import parameters
from pdf2image import convert_from_path
import pypdfium2 as pdfium
import sys

def run_pipeline(input_path, output_folder,ocr):

    try:# Load a document
        images = convert_from_path(input_path, dpi=300)
    except Exception as e:
        print(f"An error occurred while loading the PDF page: {e}, please check the input path")
        sys.exit(1)  # Exit with a non-zero status code
    
    # render a single page (in this case: the first one)
    for index, image in enumerate(images):

        page_number = index + 1;

        # Convert the Pillow image to a NumPy array
        np_image = np.array(image)
        
        #Apply OCR on the image and obtain it
        txts, boxes, scores = apply_ocr(ocr, np_image)

        #Obtain key_values from the header
        key_value_pairs, ymax_header = find_key_value_pairs(txts,boxes)

        #Obtain line_values from the table
        line_items = find_line_items(txts, boxes, ymax_header)
        
        add_to_json(page_number, key_value_pairs, line_items)

    print(f"Operation Successful. File has been saved at {output_folder}")