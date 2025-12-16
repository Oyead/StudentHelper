import os
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QFileDialog


def select_file():
    path, _ = QFileDialog.getOpenFileName(
        None,
        "Select a file",
        "",
        "All Files (*);;Word Files (*.docx);;PDF Files (*.pdf)"
    )
    return path if path else None


# ---------- Base Converter ----------

class ConverterBase(ABC):
    @abstractmethod
    def convert(self, input_path, output_dir):
        pass


# ---------- Word → Converters ----------
class WordToPDFConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        from docx import Document
        from fpdf import FPDF

        doc = Document(input_path)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for p in doc.paragraphs:
            pdf.multi_cell(0, 8, p.text)

        out = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        )
        pdf.output(out)


class WordToTXTConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        from docx import Document

        doc = Document(input_path)
        out = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".txt"
        )

        with open(out, "w", encoding="utf-8") as f:
            for p in doc.paragraphs:
                f.write(p.text + "\n")


class WordToHTMLConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        from docx import Document

        doc = Document(input_path)
        out = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".html"
        )

        with open(out, "w", encoding="utf-8") as f:
            f.write("<html><body>\n")
            for p in doc.paragraphs:
                f.write(f"<p>{p.text}</p>\n")
            f.write("</body></html>")

# ---------- PDF → Converters ----------
class PDFToTXTConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        import PyPDF2
        out_path = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0]+".txt"
        )
        text = ""
        with open(input_path,"rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text+=page.extract_text() + "\n"
        with open(out_path,"w",encoding="utf-8") as f:
            f.write(text)

class PDFToHTMLConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        import PyPDF2

        out_path = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".html"
        )

        html_content = "<html><body>\n"
        with open(input_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                html_content += f"<p>{page.extract_text()}</p>\n"
        html_content += "</body></html>"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    
class PDFToWordConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        # PDF → Word is more complex, simple approach: text only
        from docx import Document
        import PyPDF2

        doc = Document()
        with open(input_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                doc.add_paragraph(page.extract_text() or "")

        out_path = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".docx"
        )
        doc.save(out_path)
# ---------- Manager ----------

class ConversionManager:
    converters = {
        # Word input
        ".docx": {
            "pdf": WordToPDFConverter(),
            "txt": WordToTXTConverter(),
            "html": WordToHTMLConverter(),
        },
        # PDF input
        ".pdf": {
            "txt": PDFToTXTConverter(),
            "html": PDFToHTMLConverter(),
            "docx": PDFToWordConverter(),
        }
    }

    @classmethod
    def convert(cls, input_path, output_dir, target_format):
        ext = os.path.splitext(input_path)[1].lower()
        if ext not in cls.converters:
            raise ValueError(f"Unsupported input file: {ext}")

        if target_format not in cls.converters[ext]:
            raise ValueError(f"Unsupported output format: {target_format}")

        cls.converters[ext][target_format].convert(input_path, output_dir)


# ---------- Public API ----------

def convert(input_path, output_dir, target_format):
    ConversionManager.convert(input_path, output_dir, target_format)
