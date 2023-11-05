# MEDICAL BILLS KIE
The algorithm uses regular expressions combined with bounding box locations to extraction key information from medical invoices.
PaddleOCR is used as the OCR engine to extract text from the invoices.


## HOW TO RUN
Set initialization parameters in parameters.py file and run it

output_path = os.getcwd()                                      
input_path = os.path.join(os.getcwd(), 'pdfdc.pdf')            
json_file_name = "medical_bills_new.json"                      

Run main.py

### ASSUMPTIONS
All tables will have a column labeled "Description," regardless of its case format. <br>
All text in the table rows will be left aligned while all numbers will be right aligned <br>


### LIBRARIES
PaddleOCR <br>
OpenCV  <br>
os 	<br>
PIL <br>
skimage	<br>
re 	<br>
numpy	<br>
json  <br>
math <br>
collections	<br>
fitz  # PyMuPDF	 <br>		
logging	 <br>
jdeskew	 <br>


NOTE: Use the pip install -r requirements.txt command to install all Python modules and packages required from the requirements.txt file.


### BASE FUNCTIONS
def preprocess(image) ----- Applies preprocessing techniques on the image <br>
def apply_ocr(ocr, image) ----- Applies OCR on the image and returns texts,boxes and scores <br>
def calculate_centroid(box) ----- Calculates and returns the centroid of a given bounding box <br>
def euclidean_distance(centroid_1, centroid_2) ----- Calculates and returns the euclidean distnace between 2 points <br><br> 



### KEY VALUE PAIR FUNCTIONS 
def identify_header(txts,boxes) ----- Identifies the header segment of an image <br>
def find_key_vals_regex(txts, header_text, header_boxes) ---- Uses regular expressions to extract potential key values <br>
def find_key_vals_boxes(matches_text,matches_boxes,header_text,header_boxes,key_value_pairs) ---- Uses bounding box locations to find partners for identified keys <br>
def find_key_value_pairs(txts,boxes) ----- Main function for key value extraction <br><br> 



### LINE ITEM FUNCTIONS 
def identify_table(txts,boxes,ymax_header) ---- Identifies the table segment of an image <br>
def find_description_items(table_text, table_boxes) ---- Finds the column 'DESCRIPTION' and all row elements belonging to it <br>
def find_table_titles(bounding_box_desc,table_text,table_boxes) ---- Finds all other table titles in addition to 'DESCRIPTION' <br>
def find_description_siblings(table_text, table_boxes) ---- For each description row element, corresponding row elements belonging to other found titles are obtained. Returns 							    a python dictionary with the titles as keys and the row elements as a list of values for each title. <br>
def find_line_items(table_text, table_boxes) ----- Main function for line item extraction <br> <br> 


### JSON FUNCTION
def add_to_json(page_number, key_values, final_line_values) ---- Adds all identified key value pairs and line values to a json file <br> <br> 

## MAIN FUNCTIONS 
def run_pipeline(pdf_document, output_folder,ocr) ---- Runs the pipeline when the main() function is called
def main(): ---- Runs the whole process 
