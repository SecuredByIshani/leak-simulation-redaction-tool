# text_redactor.py
import re
from flask import Blueprint, render_template, request, current_app

bp = Blueprint("text_redactor", __name__, template_folder="templates")

# --- Regex patterns for PII detection ---
PATTERNS = {
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    # International-ish phone numbers (simple): +91 98765 43210 or 98765-43210 or (987) 654-3210
    "PHONE": re.compile(r"\b(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,4}\)?[\s\-]?)?\d{3,4}[\s\-]?\d{3,4}\b"),
    # US SSN-ish: 123-45-6789 or 123 45 6789
    "SSN": re.compile(r"(?<!\d)(?!000|666|9\d{2})(\d{3})(?:[-\s]?)(?!00)(\d{2})(?:[-\s]?)(?!0{4})(\d{4})(?!\d)"),
    # Generic ID-ish patterns (simple): sequence of letters+digits like AB123456 or roll numbers like 2019CS123
    "ID_SIMPLE": re.compile(r"\b[A-Z]{1,4}\d{3,8}\b"),
    # Dates (YYYY-MM-DD, DD/MM/YYYY)
    "DATE": re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b"),
    # Aadhaar-like (India) 12 digits in groups or plain 12 digits
    "AADHAAR": re.compile(r"(?<!\d)(\d{4}[-\s]?\d{4}[-\s]?\d{4})(?!\d)"),
    # Credit card (very simple Luhn-like format groups of 4)
    "CREDIT_CARD": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
}

# Order matters for redaction replacement (avoid nested overlap problems)
REPLACEMENT_LABEL = {
    "EMAIL": "[REDACTED-EMAIL]",
    "PHONE": "[REDACTED-PHONE]",
    "SSN": "[REDACTED-SSN]",
    "ID_SIMPLE": "[REDACTED-ID]",
    "DATE": "[REDACTED-DATE]",
    "AADHAAR": "[REDACTED-AADHAAR]",
    "CREDIT_CARD": "[REDACTED-CARD]",
}


def detect_entities(text):
    """
    Return a list of detected entities as dicts:
    [{ "type": "EMAIL", "match": "abc@example.com", "start": 10, "end": 25 }, ...]
    """
    found = []
    for etype, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            found.append({
                "type": etype,
                "match": m.group(0),
                "start": m.start(),
                "end": m.end()
            })
    # sort by start position
    found.sort(key=lambda x: x["start"])
    return found


def secure_redact(text):
    """
    Replace detected spans with secure labels (removes underlying data).
    This uses a safe method that processes spans from right -> left to maintain indices.
    """
    entities = detect_entities(text)
    if not entities:
        return text, entities

    # Merge overlapping entities: we will keep the earliest-start and latest-end of overlapping cluster
    merged = []
    for ent in entities:
        if not merged:
            merged.append(ent.copy())
            continue
        last = merged[-1]
        if ent["start"] <= last["end"]:  # overlap or contiguous
            last["end"] = max(last["end"], ent["end"])
            # if types differ, append types info into match (optional)
            last["type"] = f"{last['type']}|{ent['type']}" if ent["type"] not in last["type"] else last["type"]
            last["match"] = text[last["start"]:last["end"]]
        else:
            merged.append(ent.copy())

    # Build redacted text by walking through merged spans
    out = []
    cursor = 0
    for ent in merged:
        out.append(text[cursor:ent["start"]])
        # choose label based on first known pattern in merged type
        main_type = ent["type"].split("|")[0]
        label = REPLACEMENT_LABEL.get(main_type, "[REDACTED]")
        out.append(label)
        ent["redaction_label"] = label
        cursor = ent["end"]
    out.append(text[cursor:])
    redacted = "".join(out)
    return redacted, merged


@bp.route("/text-redact", methods=["GET", "POST"])
def text_redact():
    result = None
    original = ""
    entities = []
    redacted = ""
    if request.method == "POST":
        original = request.form.get("text", "") or ""
        # detect + redact
        redacted, entities = secure_redact(original)
        result = {
            "original": original,
            "redacted": redacted,
            "entities": entities,
            "counts": {}
        }
        # counts by type
        for e in entities:
            t = e["type"].split("|")[0]
            result["counts"][t] = result["counts"].get(t, 0) + 1

    return render_template("text_redact.html", result=result)
