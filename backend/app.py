from flask import Flask, request, jsonify, send_file
from scraper import scrape_jobs
import os

app = Flask(__name__)

# Output directory for CSV files
OUTPUT_DIR = "csv_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"message": "URL is required"}), 400

        # Filepath for the output CSV
        output_file = os.path.join(OUTPUT_DIR, "jobs.csv")

        # Perform scraping
        scrape_jobs(url, output_file)
        return jsonify({"message": "Scraping completed!", "csv_url": f"/download/jobs.csv"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"message": "File not found"}), 404
    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
