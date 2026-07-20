import fitz  # PyMuPDF
from docx import Document
from utils.logger import logger

class FileHandler:
    """
    Handles reading and writing of supported files.
    """

    # READ PDF
    def read_pdf(self, file_path: str) -> str:
        """
        Read a PDF file and return all extracted text.
        """
        try:
            text = ""
            with fitz.open(file_path) as pdf:
                for page in pdf:
                    text += page.get_text()

            logger.info(f"PDF file read successfully: {file_path}")
            return text

        except Exception as e:
            logger.error(f"Error reading PDF file: {e}")
            raise
    
    # READ DOCX
    def read_docx(self, file_path: str) -> str:
        """
        Read a DOCX file and return all extracted text.
        """
        try:
            document = Document(file_path)
            lines = []
            
            for paragraph in document.paragraphs:
                lines.append(paragraph.text)
                text = "\n".join(lines)

            logger.info(f"DOCX file read successfully: {file_path}")
            return text

        except Exception as e:
            logger.error(f"Error reading DOCX file: {e}")
            raise


    def read_file(self, file_path: str) -> str:
        """
        Read a supported file (PDF or DOCX) and return its text.
        """
        if file_path.endswith(".pdf"):
            return self.read_pdf(file_path)

        elif file_path.endswith(".docx"):
            return self.read_docx(file_path)

        else:
            logger.error(f"Unsupported file format: {file_path}")
            raise ValueError(
                "Unsupported file format. Only PDF and DOCX files are supported."
            )
        
    # SAVE REPORT
    def save_report(self, output_path: str, content: str) -> None:
        """
        Save analysis report to a text file.
        """
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(content)

            logger.info(f"Report saved successfully: {output_path}")

        except Exception as e:
            logger.error(f"Error saving report: {e}")
            raise