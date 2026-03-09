import io
from flask import Flask, send_file, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)


@app.route("/")
def health():
    return jsonify({"status": "ok", "message": "Flask Playwright server is running"}), 200


@app.route("/download-quotation", methods=["GET"])
def download_quotation():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                ]
            )
            page = browser.new_page()

            # Login
            page.goto("https://app.inter-fast.fr/login")
            page.fill('#loginControl', 'a.kamoun@fullremotefactory.com')
            page.fill('#passwordControl', "Tunisie2026!")
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")

            # Navigate
            page.goto("https://app.inter-fast.fr/dashboard/billing/quotations/1651d077-355c-4fca-b83d-e875a0127b30")
            page.wait_for_load_state("networkidle")

            # Download
            with page.expect_download() as download_info:
                page.click('button[title="Télécharger"]')

            download = download_info.value
            filename = download.suggested_filename

            # In memory — no disk write
            file_bytes = io.BytesIO(download.path().read_bytes())
            browser.close()

            file_bytes.seek(0)
            return send_file(
                file_bytes,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename
            ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)