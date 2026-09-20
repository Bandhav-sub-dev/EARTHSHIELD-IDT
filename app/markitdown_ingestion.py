
from pathlib import Path

from markitdown import MarkItDown

from app.utils.logger import info, error


class EarthShieldDocumentIngestor:

    def __init__(self):
        self.converter = MarkItDown()

    def extract(self, file_path):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"File does not exist: {file_path}"
            )

        try:

            result = self.converter.convert(
                str(file_path)
            )

            text = result.text_content

            info(
                f"Extracted {len(text)} characters "
                f"from {file_path.name}"
            )

            return text

        except Exception as exc:

            error(
                f"MarkItDown extraction failed: {exc}"
            )

            raise

    def extract_directory(self, directory):

        directory = Path(directory)

        results = {}

        if not directory.exists():
            return results

        supported = {
            ".pdf",
            ".docx",
            ".pptx",
            ".xlsx",
            ".html",
            ".htm",
            ".txt",
            ".md",
        }

        for file_path in directory.rglob("*"):

            if (
                file_path.is_file()
                and file_path.suffix.lower() in supported
            ):

                try:
                    results[file_path.name] = (
                        self.extract(file_path)
                    )

                except Exception:
                    continue

        return results
