from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Com:
    isLittleEndianWords: bool
    length: int
    register: int
    readCommand: Optional[int] = field(default=None)
    writeCommand: Optional[int] = field(default=None)

    def __post_init__(self):
        # Проверка диапазона для length
        if not (1 <= self.length <= 2):  # Замените диапазон на нужный
            raise ValueError("Length must be between 1 and 2")

        # Проверка диапазона для register
        if not (0 <= self.register <= 65535):  # Замените диапазон на нужный
            raise ValueError("Register must be between 0 and 65535")

        # Проверка диапазона для readCommand, если оно не None
        if self.readCommand is not None and not (self.readCommand == 3):
            raise ValueError("ReadCommand must be 3")

        # Проверка диапазона для writeCommand, если оно не None
        if self.writeCommand is not None and not (self.writeCommand == 16):
            raise ValueError("WriteCommand must be 16")
