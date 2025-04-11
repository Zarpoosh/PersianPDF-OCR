from pdf2image import convert_from_path
from pytesseract import image_to_pdf_or_hocr
from PyPDF2 import PdfMerger
from PIL import Image
import os

# مسیر فایل ورودی و پوشه‌های کاری
INPUT_PDF_PATH = "input/myfile.pdf"
OUTPUT_FOLDER = "output"
LANG = "fas"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("📄 در حال پردازش OCR صفحات تصویری PDF...")

# مرحله 1: تبدیل PDF به عکس
images = convert_from_path(INPUT_PDF_PATH)

# مرحله 2: OCR و ذخیره صفحات به صورت PDF جدا
ocr_pdf_paths = []

for i, image in enumerate(images):
    print(f"🌀 صفحه {i+1}/{len(images)} در حال OCR...")

    pdf_bytes = image_to_pdf_or_hocr(image, lang=LANG, extension='pdf')
    
    output_temp_pdf = os.path.join(OUTPUT_FOLDER, f"page_{i+1}.pdf")
    with open(output_temp_pdf, 'wb') as f:
        f.write(pdf_bytes)

    ocr_pdf_paths.append(output_temp_pdf)

# مرحله 3: ادغام فایل‌های PDF به یک فایل
print("🧩 در حال ادغام فایل‌ها به یک PDF...")

merger = PdfMerger()
for pdf_path in ocr_pdf_paths:
    merger.append(pdf_path)

final_output = os.path.join(OUTPUT_FOLDER, "final_ocr_output.pdf")
merger.write(final_output)
merger.close()

print(f"✅ همه صفحات به یک فایل PDF تبدیل شدند: {final_output}")
