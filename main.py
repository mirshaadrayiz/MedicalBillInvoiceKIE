from paddleocr import PaddleOCR
from pipeline import run_pipeline
import pypdfium2 as pdfium
import parameters
import sys

if __name__ == "__main__":

    input_path = parameters.input_path
    output_path = parameters.output_path
    
    # Initializing OCR library and creating an object ocr
    ocr = PaddleOCR(lang='en', use_angle_cls=True, use_gpu=True)
    run_pipeline(input_path,output_path,ocr)
