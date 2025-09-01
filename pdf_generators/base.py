from abc import ABC, abstractmethod
from typing import List

class PDFGenerator(ABC):
    @abstractmethod
    def generate(self, image_files: List[str], output_pdf_path: str):
        """
        이미지 파일 리스트를 받아 PDF로 저장합니다.
        """
        pass
