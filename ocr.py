import os
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger

# تنظیم مسیرها
INPUT_PDF_PATH = "input/myfile.pdf"
OUTPUT_DIR = "output"
OUTPUT_PDF_NAME = "final_ocr.pdf"
LANG = "fas"

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📄 در حال پردازش OCR صفحات تصویری PDF...")

# مرحله ۱: تبدیل مستقیم صفحات PDF تصویری به عکس‌ها
reader = PdfReader(INPUT_PDF_PATH)
total_pages = len(reader.pages)
images = convert_from_path(INPUT_PDF_PATH, dpi=150)  # همزمان به تصاویر تبدیل می‌کنه

merger = PdfMerger()
for i, image in enumerate(images):
    print(f"🌀 صفحه {i+1}/{total_pages} در حال OCR...")

    # OCR و تولید PDF موقت
    output_temp_pdf = os.path.join(OUTPUT_DIR, f"page_{i+1:03d}.pdf")
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, lang=LANG, extension='pdf')
    with open(output_temp_pdf, 'wb') as f:
        f.write(pdf_bytes)

    # اضافه کردن به فایل نهایی
    merger.append(output_temp_pdf)

# مرحله نهایی: ذخیره PDF نهایی
final_path = os.path.join(OUTPUT_DIR, OUTPUT_PDF_NAME)
merger.write(final_path)
merger.close()

print(f"\n✅ OCR کامل شد. فایل نهایی ساخته شد: {final_path}")
