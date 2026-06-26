from flask import Flask, render_template, request, send_file, send_from_directory, redirect
import pdf_redactor
import re
from datetime import datetime, timezone
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    redacted_text = None
    pdf_ready = None
    simulate_ready = None

    if request.method == "POST":

        # ---------------- TEXT REDACTION ----------------
        if request.form.get("action") == "redact_text":
            text = request.form.get("text", "")

            patterns = {
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}": "[REDACTED EMAIL]",
                r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b": "[REDACTED SSN]",
                r"\b(?:\+91[- ]?)?\d{10}\b": "[REDACTED PHONE]",
                r"http[s]?://\S+": "[REDACTED LINK]",
                r"Name:\s*[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+": "Name: [REDACTED]"
            }

            for pattern, replacement in patterns.items():
                text = re.sub(pattern, replacement, text)

            redacted_text = text

        # ---------------- PDF REDACTION ----------------
        if request.form.get("action") == "redact_pdf":
            file = request.files.get("pdf")
            if file:
                input_path = os.path.join(UPLOAD_FOLDER, file.filename)
                output_filename = "redacted_" + file.filename
                output_path = os.path.join(UPLOAD_FOLDER, output_filename)

                file.save(input_path)

                options = pdf_redactor.RedactorOptions()

                options.metadata_filters = {
                    "Title": [lambda v: v.upper() if v else "UNTITLED"],
                    "Producer": [lambda v: "Redacted Generator"],
                    "CreationDate": [lambda v: datetime.now(timezone.utc)],
                    "Author": [lambda v: None],
                    "DEFAULT": [lambda v: None]
                }

                options.xmp_filters = [lambda xml: None]

                options.content_filters = [
                    (re.compile(u"[−–—~‐]"), lambda m: "-"),
                    (re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b"), lambda m: "XXX-XX-XXXX"),
                    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), lambda m: "[REDACTED EMAIL]"),
                    (re.compile(r"https?://[^\s]+"), lambda m: "[REDACTED LINK]"),
                    (re.compile(r"(?i)comment[:!]?.*"), lambda m: "[REDACTED COMMENT]"),
                    (re.compile(r"(?i)do not share.*"), lambda m: "[REDACTED WARNING]")
                ]

                with open(input_path, "rb") as inp, open(output_path, "wb") as outp:
                    options.input_stream = inp
                    options.output_stream = outp
                    pdf_redactor.redactor(options)

                return send_file(
                    output_path,
                    as_attachment=True,
                    download_name=output_filename,
                    mimetype="application/pdf"
                )

        # ---------------- SIMULATION REDACTION ----------------
        if request.form.get("action") == "simulate":
            file = request.files.get("simulate_pdf")
            if file:
                input_path = os.path.join(UPLOAD_FOLDER, file.filename)
                output_path = os.path.join(UPLOAD_FOLDER, "secure_sim_" + file.filename)

                file.save(input_path)

                options = pdf_redactor.RedactorOptions()
                options.content_filters = [
                    (re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b"), lambda m: "XXX-XX-XXXX"),
                    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), lambda m: "[REDACTED EMAIL]")
                ]

                with open(input_path, "rb") as inp, open(output_path, "wb") as outp:
                    options.input_stream = inp
                    options.output_stream = outp
                    pdf_redactor.redactor(options)

                simulate_ready = "/" + output_path

    return render_template(
        "index.html",
        redacted_text=redacted_text,
        pdf_ready=pdf_ready,
        simulate_ready=simulate_ready
    )


# ----------------------------------------------------------
# SERVE YOUR EXTERNAL SLIDER FOLDER
# ----------------------------------------------------------
@app.route('/slider/<path:filename>')
def slider_files(filename):
    return send_from_directory(
        r"C:/Uni/Sem3/SPS261/project/Website/slider_1",
        filename
    )

# Optional nicer URL
@app.route('/home')
def home():
    return redirect("/slider/index.html")


# ----------------------------------------------------------

if __name__ == "__main__":
    app.run(port=5003, debug=True)
