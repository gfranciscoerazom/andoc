from pathlib import Path

class Doc:
    def __init__(self, text: str, path: Path, line: int | None = None):
        self.text = text
        self.path = path
        self.line = line

    def __str__(self):
        return self.text

    def __hash__(self) -> int:
        return hash((self.text, self.path, self.line))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Doc):
            return NotImplemented
        return self.text == other.text and self.path == other.path and self.line == other.line

    def write_to_andoc_file(self):
        """
        Writes the doc to the andoc file.
        """
        pass