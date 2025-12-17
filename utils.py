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

# ---------- TXT → Converters ----------
class TXTToPDFConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        from fpdf import FPDF
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Arial",size=12)
        with open(input_path,"r",encoding="utf-8",errors="ignore") as f:
            for line in f:
                pdf.multi_cell(0,8,line.rstrip())
        out = os.path.join(output_dir,os.path.splitext)
        pdf.output(out)

class TXTToWordConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        from docx import Document
        doc = Document()
        with open(input_path,"r",encoding="utf-8",errors="ignore") as f:
            for line in f:
                doc.add_paragraph(line.rstrip())
        out = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".docx"
        )
        doc.save(out)

class TXTToHTMLConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        out = os.path.join(output_dir,os.path.splitext(os.path.basename(input_path))[0]+".html")
        with open(input_path,"r",encoding="utf-8",errors="ignore") as f:
            lines = f.readlines()
        with open(out,"w",encoding="utf-8") as f:
            f.write("<html><body>\n<pre>\n")
            for line in lines:
                f.write(line)
            f.write("</pre>\n</body></html>")

# ---------- HTML → Converters ----------
class HTMLToTXTConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        from bs4 import BeautifulSoup

        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f, "html.parser")

        text = soup.get_text(separator="\n", strip=True)

        out = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".txt"
        )

        with open(out, "w", encoding="utf-8") as f:
            f.write(text)


class HTMLToWordConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        from bs4 import BeautifulSoup
        from docx import Document

        doc = Document()

        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f, "html.parser")

        for element in soup.body.descendants:
            if element.name == "h1":
                doc.add_heading(element.get_text(), level=1)
            elif element.name == "h2":
                doc.add_heading(element.get_text(), level=2)
            elif element.name == "p":
                doc.add_paragraph(element.get_text())
            elif element.name == "li":
                doc.add_paragraph(element.get_text(), style="List Bullet")

        out = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".docx"
        )
        doc.save(out)


class HTMLToPDFConverter(ConverterBase):
    def convert(self, input_path, output_dir):
        import pdfkit
        # Construct output PDF path
        out = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        )

        # Use pdfkit to convert HTML to PDF
        pdfkit.from_file(input_path, out)
        print(f"Saved PDF to: {out}")

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
        }, 
        ".txt": {
            "pdf": TXTToPDFConverter(),
            "html": TXTToHTMLConverter(),
            "docx": TXTToWordConverter(),
        },
        ".html": {
            "pdf": HTMLToPDFConverter(),
            "docx": HTMLToWordConverter(),
            "txt": HTMLToTXTConverter(),
        },
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
