import os
import subprocess
from PyQt5.QtWidgets import QFileDialog
from abc import ABC,abstractmethod
class Parser(ABC):
    @abstractmethod
    def parse(self,path):
        """Return a documentModel representation of the file  """
        pass
class Renderer(ABC):
    @abstractmethod
    def render(self,document,output_path):
        """Write the DocumentModel to output file """
        pass
class DocxParser(Parser):
    def parse(self,path):
        from docx import Document
        doc=Document(path)
        document_model = {
            "metadata":{"title":doc.core_properties.title},
            "pages":[{"blocks":[p.text for p in doc.paragraphs]}]

        }
        return document_model
class PdfParser(Parser):
    def parse(self,path):
        import fitz
        pdf =fitz.open(path)
        document_model={"pages":[]}
        for page in pdf:
            document_model["pages"].append({"blocks":[page.get_text()]})
        return document_model

class DocxRenderer(Renderer):
    def render(self,document,output_path):
        from docx import Document
        doc=Document()
        for page in document.get("pages",[]):
            for block in page.get("blocks",[]):
                doc.add_paragraph(block)
        doc.save(output_path)

class PdfRenderer(Renderer):
    def render(self,document,output_path):
        import fpdf
        pdf=fpdf.FPDF()
        pdf.add_page()
        for page in document.get("pages",[]):
            for block in page.get("blocks",[]):
                pdf.set_font("Arial",size=12)
                pdf.multi_cell(0,10,block)
        pdf.output(output_path)
class Converter:
    parsers = {
        "docx":DocxParser(),
        "pdf":PdfParser()
    }
    renderers = {
        "docx"
    }
    @classmethod
    def convert(cls,input_path,input_type,output_type,output_path):
        parser = cls.parsers.get(input_type)
        renderer = cls.renderers.get(output_type)
        if not parser or not renderer:
            raise ValueError("Unspported format")
        document = parser.parse(input_path)
        renderer.render(document,output_path)
# def select_file():
#     file_path, _ = QFileDialog.getOpenFileName(
#         None,
#         "Select a file",
#         "",
#         "All files (*.*)"
#     )
#     if file_path:
#         print("Selected file:", file_path)
#         fileType = os.path.splitext(file_path)[1][1:]
#         fileName = os.path.basename(file_path)
#         print("File Type:", fileType)
#         print("File Name:", fileName)
#         return file_path
#     return None
# def convert(filepath,output_dir):
#     libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

#     subprocess.run([
#         libreoffice_path,
#         "--headless",
#         "--convert-to",
#         "pdf",
#         filepath,
#         "--outdir",
#         output_dir
#     ],check=True)
#     base_name = os.path.splitext(os.path.basename(filepath))[0]
#     output_path = os.path.join(output_dir, base_name + ".pdf")

#     return output_path