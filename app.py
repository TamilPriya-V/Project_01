from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
from pypdf import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads directory exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def extract_text_from_pdf(pdf_path):
    """Extracts text from the uploaded PDF file"""
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ''
        return text.strip()
    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}

def extract_important_info(pdf_path):
    """Sends extracted text to API and retrieves formatted JSON output"""
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        return {"error": "Could not extract text from PDF"}

    payload = {
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
        "messages": [
            {"role": "system", "content": "You should extract key information names and values from documents."},
            {"role": "user", "content": f"Extract key details from the following document in a structured format. Provide only name-value pairs without any additional commentary that is being generated in the background. Ensure the response is formatted with each key-value pair clearly structured {extracted_text}"}

        ],
        "temperature": 0.5,
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            extracted_data = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")

            # Convert **bold** markdown into HTML <b> tags and newlines into <br>
            extracted_data = extracted_data.replace("**", "<b>").replace("\n", "<br>")

            return {"extracted_data": extracted_data}
        else:
            return {"error": f"API error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"Failed to connect to API: {str(e)}"}

@app.route("/", methods=["GET", "POST"])
def index():
    """Renders HTML page and processes PDF upload"""
    extracted_data = None
    pdf_path = None

    if request.method == "POST":
        if "pdf_file" not in request.files:
            return jsonify({"error": "No file uploaded."})
        
        pdf_file = request.files["pdf_file"]
        if pdf_file.filename == "":
            return jsonify({"error": "No file selected."})
        
        pdf_filename = os.path.join(app.config["UPLOAD_FOLDER"], pdf_file.filename)
        pdf_file.save(pdf_filename)

        extracted_data = extract_important_info(pdf_filename)
        pdf_path = f"/uploads/{pdf_file.filename}"  # Pass relative path to template

    return render_template("index.html", extracted_data=extracted_data, pdf_path=pdf_path)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serves the uploaded PDF so it can be viewed in iframe"""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
