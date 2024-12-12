import argparse
import os
from fpdf import FPDF
import fitz
from PIL import Image
from datetime import datetime

CM_TO_POINTS = 28.3465
datestamp = datetime.now().strftime("%d-%m-%Y_%H:%M")

region1_cm = (0.3, 0.0, 10.3, 14.15)
region2_cm = (10.7, 0.0, 20.75, 14.15)

region1 = fitz.Rect(*[coord * CM_TO_POINTS for coord in region1_cm])
region2 = fitz.Rect(*[coord * CM_TO_POINTS for coord in region2_cm])

parser = argparse.ArgumentParser(description='Process a PDF file to extract labels.')
parser.add_argument('input_file', type=str, help='The input PDF file')
args = parser.parse_args()

if not os.path.isfile(args.input_file):
    print(f"Error: The file {args.input_file} does not exist.")
    exit(1)

if not args.input_file.lower().endswith('.pdf'):
    print("Error: The input file must be a PDF.")
    exit(1)

pdf_document = fitz.open(args.input_file)

if len(pdf_document) == 0:
    print("The PDF document is empty. Exiting.")
    exit()

a6_width_points = 1240 * 72 / 300
a6_height_points = 1748 * 72 / 300
a6_size = (1240, 1748)

output_pdf = FPDF(orientation='P', unit='pt', format=(a6_width_points, a6_height_points))

for page_number in range(len(pdf_document)):
    
    page = pdf_document[page_number]

    if page.rect.width < 11 * CM_TO_POINTS:
        output_pdf.add_page()
        pix = page.get_pixmap(dpi=400)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = img.resize(a6_size, Image.LANCZOS)
        img_path = f"{page_number + 1}_A6.png"
        img.save(img_path)
        output_pdf.image(img_path, 0, 0, a6_width_points, a6_height_points)
        os.remove(img_path)
        continue

    pix1 = page.get_pixmap(clip=region1, dpi=400)
    pix2 = page.get_pixmap(clip=region2, dpi=400)

    img1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)
    img2 = Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples)

    img1 = img1.resize(a6_size, Image.LANCZOS)
    img2 = img2.resize(a6_size, Image.LANCZOS)

    img1_path = f"{page_number + 1}_Label.png"
    img2_path = f"{page_number + 1}_CN22.png"
    img1.save(img1_path)
    img2.save(img2_path)

    output_pdf.add_page()
    output_pdf.image(img1_path, 0, 0, a6_width_points, a6_height_points)
    output_pdf.add_page()
    output_pdf.image(img2_path, 0, 0, a6_width_points, a6_height_points)

    os.remove(img1_path)
    os.remove(img2_path)

output_pdf.output(f"ebay labels - {datestamp}.pdf")

print("ebay labels successfully converted to A6")