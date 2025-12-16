import os
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QFileDialog


def select_file():
    path, _ = QFileDialog.getOpenFileName(
        None,
        "Select a file",
        "",
        "All Files (*);;Word Files (*.docx)"
    )
    return path if path else None


# ---------- Base Converter ----------

class ConverterBase(ABC):
    @abstractmethod
    def convert(self, input_path, output_dir):
        pass


# ---------- Concrete Converters ----------

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


# ---------- Manager ----------

class ConversionManager:
    converters = {
        "pdf": WordToPDFConverter(),
        "txt": WordToTXTConverter(),
        "html": WordToHTMLConverter(),
    }

    @classmethod
    def convert(cls, input_path, output_dir, target_format):
        ext = os.path.splitext(input_path)[1].lower()

        if ext not in (".doc", ".docx"):
            raise ValueError("Unsupported input file")

        if target_format not in cls.converters:
            raise ValueError("Unsupported output format")

        cls.converters[target_format].convert(input_path, output_dir)


# ---------- Public API ----------

def convert(input_path, output_dir, target_format):
    ConversionManager.convert(input_path, output_dir, target_format)
