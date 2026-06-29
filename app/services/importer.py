"""Generic spreadsheet import engine with validation and duplicate detection."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable
import pandas as pd

@dataclass(frozen=True)
class ImportResult:
    rows: list[dict]
    errors: list[str]
    duplicates: list[int]

class SpreadsheetImporter:
    def __init__(self, required_columns: Iterable[str], duplicate_key: str | None = None):
        self.required_columns = list(required_columns)
        self.duplicate_key = duplicate_key

    def preview(self, path: str | Path) -> ImportResult:
        suffix = Path(path).suffix.lower()
        frame = pd.read_csv(path) if suffix == ".csv" else pd.read_excel(path)
        errors = [f"Missing required column: {c}" for c in self.required_columns if c not in frame.columns]
        rows = frame.fillna("").to_dict(orient="records") if not errors else []
        duplicates = []
        if self.duplicate_key and self.duplicate_key in frame.columns:
            duplicates = [int(i) for i, v in frame[self.duplicate_key].duplicated().items() if v]
        return ImportResult(rows=rows, errors=errors, duplicates=duplicates)

    @staticmethod
    def validate_amount(value) -> Decimal:
        try:
            return Decimal(str(value).replace(",", "").strip() or "0")
        except InvalidOperation as exc:
            raise ValueError(f"Invalid amount: {value}") from exc
