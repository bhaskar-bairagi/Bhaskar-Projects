"""Small, deterministic payment reconciliation exercise (no cloud account needed)."""
from __future__ import annotations

import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
from io import StringIO


def read_csv(text: str, required: set[str]) -> list[dict[str, str]]:
    reader = csv.DictReader(StringIO(text))
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError(f"Expected columns: {', '.join(sorted(required))}")
    rows = list(reader)
    if any(not row.get("transaction_id") for row in rows):
        raise ValueError("Every row needs a transaction_id")
    if any(count > 1 for count in Counter(row["transaction_id"] for row in rows).values()):
        raise ValueError("Duplicate transaction_id in one input")
    return rows


def amount(value: str) -> Decimal:
    try:
        result = Decimal(value)
    except (InvalidOperation, TypeError):
        raise ValueError(f"Invalid amount: {value!r}") from None
    if not result.is_finite():
        raise ValueError(f"Invalid amount: {value!r}")
    if result.as_tuple().exponent < -2:
        raise ValueError(f"Amount must have at most two decimals: {value!r}")
    return result


def reconcile(ledger_text: str, settlement_text: str) -> list[dict[str, str]]:
    required = {"transaction_id", "amount", "currency"}
    ledger = read_csv(ledger_text, required)
    settlement = read_csv(settlement_text, required)
    left = {row["transaction_id"]: row for row in ledger}
    right = {row["transaction_id"]: row for row in settlement}
    results = []
    for transaction_id in sorted(left.keys() | right.keys()):
        book, bank = left.get(transaction_id), right.get(transaction_id)
        if book:
            amount(book["amount"])
        if bank:
            amount(bank["amount"])
        if not book:
            status = "settlement_only"
        elif not bank:
            status = "ledger_only"
        elif book["currency"].strip().upper() != bank["currency"].strip().upper():
            status = "currency_mismatch"
        elif amount(book["amount"]) != amount(bank["amount"]):
            status = "amount_mismatch"
        else:
            status = "matched"
        results.append({"transaction_id": transaction_id, "status": status,
                        "ledger_amount": book["amount"] if book else "",
                        "settlement_amount": bank["amount"] if bank else "",
                        "ledger_currency": book["currency"].upper() if book else "",
                        "settlement_currency": bank["currency"].upper() if bank else ""})
    return results


def to_csv(rows: list[dict[str, str]]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["transaction_id", "status", "ledger_amount",
                                               "settlement_amount", "ledger_currency", "settlement_currency"])
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()
