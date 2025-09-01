import img2pdf
from typing import List
from .base import PDFGenerator

class Img2PDFGenerator(PDFGenerator):
    def generate(self, image_files: List[str], output_pdf_path: str):
        if not image_files:
            return
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_files))
