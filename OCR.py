import os
import PyPDF2
from PIL import Image
import pytesseract
import chardet
import fitz 
import langid

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the path to the Tesseract data directory
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

'''
Based on cmd : 
browse to pics folder
> tessract image_name.png output_file_name
'''

#########################################################################
# Function Implementation
#####################################################

# Extracting text from PDF file
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            
            # Retrieving raw text from pdf
            raw_text = page.extract_text()
            
            # Detecting text encoding
            encoding_info = chardet.detect(raw_text.encode())
            detected_encoding = encoding_info['encoding']
            
            # Check if detected encoding is not None
            if detected_encoding is not None:
                # Encodes text with detected encoding then, decodes it as Unicode string
                decoded_text = raw_text.encode(detected_encoding, 'replace').decode(detected_encoding)
                text += decoded_text
            else:
                # If encoding cannot be detected, append the raw text
                text += raw_text

    return text     


def perform_ocr(image_path):
    image = Image.open(image_path)
    ocr_output_txt = pytesseract.image_to_string(image, lang='ara')
    return(ocr_output_txt)


#Classification Function
def classify_document(text):
    # The document will be classified according to specific words indicating the theme 'Societal science' 'Exact Science'
    if 'جغرافيا' in text or 'اﻟﻌﺎﺻﻣﺔ' in text or 'فلسفة' in text or 'ﻓﯾﻠﺳوف' in text or 'تاريخ' in text or 'المؤرخين ' in text :  
        return "Societal science"
    elif  'ميكانيكية' in text or 'الجبر' in text or 'فيزياء' in text or 'رياضيات' in text or 'فيزيائية' in text or 'كيمياء' in text or 'علوم الحياة و الأرض' or 'طب' in text :
        return  "Exact Science"
    else:
        return "other"
 
def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

## classisfies and saves pdf text output to corresponding to category folder
def classify_and_save_pdf(category, content,pdf_path):
    output_folder = os.path.join('output', category)
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, pdf_path[12:-4]+'.txt')
    save_to_file(content, output_file)


## classisfies and saves image text output to corresponding to category folder
def classify_and_save_img(category, content,image_path):
    output_folder = os.path.join('output', category)
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, image_path[15:-4]+'.txt')
    save_to_file(content, output_file)

###################____     PDF treatment fct    ____########################## 
###############################################################################
def pdf_treatment(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    print(' pdf text',pdf_text)
    pdf_category = classify_document(pdf_text)
    print('pdf cate : ',pdf_category)
    classify_and_save_pdf(pdf_category, pdf_text ,pdf_path)


###################____     Image treatment fct    ____########################## 
###############################################################################
def img_treatment(image_path):
    ocr_text = perform_ocr(image_path)
    print(' img text',ocr_text)
    img_category = classify_document(ocr_text)
    print('img cate : ',img_category)
    classify_and_save_img(img_category, ocr_text,image_path)


#########################################################################
# input
#####################################################

#  PDF file path
#PDF_List=["PDF dataset\Quantum.pdf","PDF dataset\Carthage.pdf","PDF dataset\Albert Camus.pdf","PDF dataset\Communication.pdf"]
PDF_List=[]
    

# Image path
#img_List=["images dataset\Geo.png","images dataset\Algebra.png"]
img_List=[]



#########################################################################
# Function call
#####################################################

for image_path in img_List :
    img_treatment(image_path)



for pdf_path in PDF_List :
    pdf_treatment(pdf_path)



#########################################################################
# Printing output
#####################################################

print('done')