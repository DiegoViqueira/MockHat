"""Report generator"""
import logging

from markdown_pdf import MarkdownPdf, Section


class ReportGenerator:
    """Class to generate reports in different formats."""

    @staticmethod
    def save_markdown(content: str, file_path: str) -> bool:
        """Save the content in markdown format."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            logging.info("Report saved in %s", file_path)
            return True
        except Exception as e:
            logging.error("Error saving markdown %s: %s",
                          file_path, str(e))
            return False

    @staticmethod
    def save_json(content: str, file_path: str) -> bool:
        """Save the content in json format."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            logging.info("Report saved in %s", file_path)
            return True
        except Exception as e:
            logging.error("Error saving json %s: %s",
                          file_path, str(e))
            return False

    @staticmethod
    def generate_pdf(content: str, output_path: str) -> bool:
        """Generates a PDF from the markdown content."""
        try:
            pdf = MarkdownPdf(toc_level=2)
            if not content.startswith("# "):
                content = f"# Evaluation\n\n{content}"
            pdf.add_section(Section(content))
            pdf.save(output_path)
            logging.info("PDF generated in %s", output_path)
            return True
        except Exception as e:
            logging.error("Error generating PDF %s: %s",
                          output_path, str(e))
            return False
