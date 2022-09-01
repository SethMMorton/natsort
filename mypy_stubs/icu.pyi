from typing import overload

@overload
def Locale() -> str: ...
@overload
def Locale(x: str) -> str: ...

class UCollAttribute:
    NUMERIC_COLLATION: int

class UCollAttributeValue:
    ON: int

class DecimalFormatSymbols:
    kGroupingSeparatorSymbol: int
    kDecimalSeparatorSymbol: int
    def __init__(self, locale: str) -> None: ...
    def getSymbol(self, symbol: int) -> str: ...

class Collator:
    @classmethod
    def createInstance(cls, locale: str) -> Collator: ...
    def getSortKey(self, source: str) -> bytes: ...
    def setAttribute(self, attr: int, value: int) -> None: ...
