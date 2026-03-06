from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
import requests
from flask import send_file

app = Flask(__name__)

@app.route('/run-playwright', methods=['POST'])
def run_playwright():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Login
            page.goto("https://app.inter-fast.fr/login")
            page.fill('#loginControl', 'a.kamoun@fullremotefactory.com')
            page.fill('#passwordControl', "Tunisie2026!")
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")

            # Naviguer
            page.goto("https://app.inter-fast.fr/dashboard/billing/quotations/1651d077-355c-4fca-b83d-e875a0127b30")
            page.wait_for_load_state("networkidle")

            # Télécharger
            with page.expect_download() as download_info:
                page.click('button[title="Télécharger"]')

            download = download_info.value
            file_path = f"/tmp/{download.suggested_filename}"
            download.save_as(file_path)

            browser.close()

            return send_file(file_path, mimetype="application/pdf", as_attachment=True, download_name=download.suggested_filename), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)