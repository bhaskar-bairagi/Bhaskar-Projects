"""Beginner-friendly invoice extraction with visible fallbacks."""

from __future__ import annotations

import base64
import re
import unicodedata
from io import BytesIO

from pydantic import BaseModel, Field


class Invoice(BaseModel):
    """Flexible schema: unknown values are allowed instead of failing the PDF."""

    invoice_date: str | None = None
    vendor: str | None = None
    invoice_number: str | None = None
    total_amount: str | None = None
    currency: str | None = None
    notes: list[str] = Field(default_factory=list)


def clean_name(text: str | None) -> str:
    if not text:
        return "unknown"
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-") or "unknown"


def suggested_filename(invoice: Invoice) -> str:
    invoice_date = clean_name(invoice.invoice_date) if invoice.invoice_date else "unknown-date"
    return f"{invoice_date}_{clean_name(invoice.vendor)}_{clean_name(invoice.invoice_number)}.pdf"


def _prompt() -> str:
    return (
        "Extract only facts visible in this invoice. Dates must use YYYY-MM-DD when possible. "
        "Use the seller as vendor, the final amount due or charged as total_amount, and a "
        "three-letter currency code. Do not invent values. Return null for unknown fields and "
        "explain ambiguity briefly in notes."
    )


def _extract_from_pdf(client, pdf_bytes: bytes, filename: str, model: str) -> Invoice:
    encoded = base64.b64encode(pdf_bytes).decode("ascii")
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": _prompt()},
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": filename,
                        "file_data": f"data:application/pdf;base64,{encoded}",
                        "detail": "high",
                    },
                    {"type": "input_text", "text": "Extract this invoice."},
                ],
            },
        ],
        text_format=Invoice,
    )
    if response.output_parsed is None:
        raise ValueError("The PDF response contained no parsed invoice")
    return response.output_parsed


def _read_pdf_text(pdf_bytes: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()


def _extract_from_text(client, text: str, model: str) -> Invoice:
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": _prompt()},
            {"role": "user", "content": f"Invoice text:\n\n{text[:30000]}"},
        ],
        text_format=Invoice,
    )
    if response.output_parsed is None:
        raise ValueError("The text response contained no parsed invoice")
    return response.output_parsed


def extract_invoice_robust(
    pdf_bytes: bytes, filename: str, api_key: str, model: str = "gpt-5.6"
) -> tuple[Invoice, str, list[str]]:
    """Try visual PDF extraction, then text extraction, while keeping diagnostics."""
    from openai import OpenAI

    if not pdf_bytes.startswith(b"%PDF"):
        raise ValueError("The selected file does not appear to be a valid PDF")
    if len(pdf_bytes) > 50 * 1024 * 1024:
        raise ValueError("The PDF is larger than the 50 MB request limit")

    client = OpenAI(api_key=api_key, max_retries=2, timeout=90)
    warnings: list[str] = []
    try:
        invoice = _extract_from_pdf(client, pdf_bytes, filename, model)
        return invoice, "PDF vision", warnings
    except Exception as first_error:
        warnings.append(f"PDF vision attempt failed: {type(first_error).__name__}: {first_error}")

    try:
        text = _read_pdf_text(pdf_bytes)
        if len(text) < 30:
            raise ValueError("Almost no selectable text was found; this may be a scanned PDF")
        invoice = _extract_from_text(client, text, model)
        warnings.append(f"Used local text fallback ({len(text)} characters extracted)")
        return invoice, "Local text fallback", warnings
    except Exception as second_error:
        warnings.append(f"Text fallback failed: {type(second_error).__name__}: {second_error}")
        raise RuntimeError("Both extraction methods failed:\n- " + "\n- ".join(warnings)) from second_error


def extract_invoice(pdf_bytes: bytes, filename: str, api_key: str, model: str) -> Invoice:
    """Compatibility wrapper used by the Streamlit app."""
    invoice, _, _ = extract_invoice_robust(pdf_bytes, filename, api_key, model)
    return invoice


def invoice_to_row(invoice: Invoice, original_filename: str) -> dict[str, object]:
    return {
        "date": invoice.invoice_date,
        "vendor": invoice.vendor,
        "invoice_number": invoice.invoice_number,
        "amount": invoice.total_amount,
        "currency": invoice.currency,
        "original_filename": original_filename,
        "suggested_filename": suggested_filename(invoice),
        "notes": "; ".join(invoice.notes),
    }
