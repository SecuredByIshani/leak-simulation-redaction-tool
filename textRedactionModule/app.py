from flask import Flask, render_template, request, send_file
import re
import os
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# REGEX PATTERNS FOR REDACTION
# -----------------------------

PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
    "PHONE": r"\b(?:\+?\d{1,3})?[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "ID": r"\b\d{2,3}-\d{2}-\d{4}\b",
    "NAME": r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b"
}

def redact_text(text):
    """Returns text with sensitive info replaced using regex patterns."""
    for key, pattern in PATTERNS.items():
        text = re.sub(pattern, f"[{key} REDACTED]", text)
    return text


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # ---- Option 1: Text Redaction ----
        if "text_input" in request.form:
            original = request.form["text_input"]
            redacted = redact_text(original)
            return f"""
            <h2>Redacted Text</h2>
            <pre>{redacted}</pre>
            <br><a href="/">Go Back</a>
            """

        # ---- Option 2: File Upload ----
        uploaded = request.files.get("file")
        if uploaded:
            file_bytes = uploaded.read().decode("utf-8", errors="ignore")
            redacted_output = redact_text(file_bytes)

            # Return as downloadable .txt
            return send_file(
                BytesIO(redacted_output.encode()),
                mimetype="text/plain",
                as_attachment=True,
                download_name="redacted_output.txt"
            )

    # -----------------------------
    # HTML FORM
    # -----------------------------
    return """
    <h2>Text Redaction Tool</h2>

    <form method="POST">
        <textarea name="text_input" rows="8" cols="60" placeholder="Enter text here"></textarea><br>
        <button type="submit">Redact Text</button>
    </form>

    <hr>

    <form method="POST" enctype="multipart/form-data">
        <h3>Upload a .txt file to redact:</h3>
        <input type="file" name="file" accept=".txt" required>
        <button type="submit">Upload & Redact</button>
    </form>
    """


# -----------------------------
# RUN ON CUSTOM PORT (5002)
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5002)
