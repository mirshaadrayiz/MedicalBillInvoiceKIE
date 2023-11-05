import os

##INITIALIZING PARAMETERS

##Path Parameters
output_path = os.getcwd()                                      ##Desired output path for the json file
input_path = os.path.join(os.getcwd(), 'pdfdoc.pdf')            ##Input path where your pdf file is located
json_file_name = "medical_bills_final.json"                      ##Your json file name

##Config Parameters
max_keyword_length = 5