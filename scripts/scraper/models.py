from pydantic import BaseModel, field_validator
from typing import List


class Example(BaseModel):
    """Single example sentence with translations."""
    japanese: str
    romaji: str
    englishTranslation: str

    @field_validator('japanese', 'romaji', 'englishTranslation')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class GrammarPoint(BaseModel):
    """Complete grammar point with metadata."""
    id: str
    title: str
    titleRomaji: str
    explanationEN: str
    examples: List[Example]
    jlptLevel: str
    source: str = "JLPT Sensei"
    url: str

    @field_validator('examples')
    @classmethod
    def min_examples(cls, v: List[Example]) -> List[Example]:
        if len(v) < 2:
            raise ValueError('Must have at least 2 examples')
        return v

    @field_validator('jlptLevel')
    @classmethod
    def valid_level(cls, v: str) -> str:
        if v not in ['N5', 'N4', 'N3', 'N2', 'N1']:
            raise ValueError(f'Invalid JLPT level: {v}')
        return v


# Test the models work
if __name__ == '__main__':
    example = Example(
        japanese="これは本です。",
        romaji="Kore wa hon desu.",
        englishTranslation="This is a book."
    )

    grammar = GrammarPoint(
        id="test-grammar",
        title="は (wa)",
        titleRomaji="wa",
        explanationEN="Topic marker particle",
        examples=[example, example],
        jlptLevel="N5",
        url="https://example.com"
    )

    print("Models validated successfully!")
    print(f"Grammar: {grammar.title}")
