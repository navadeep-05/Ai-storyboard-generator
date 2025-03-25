from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Netlify frontend

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")  # Get token from environment variable

def generate_image(prompt):
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"},
        json={
            "version": "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5",
            "input": {"prompt": prompt}
        }
    )
    data = response.json()
    prediction_url = data["urls"]["get"]
    while True:
        result = requests.get(prediction_url, headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"})
        result_data = result.json()
        if result_data["status"] == "succeeded":
            return result_data["output"][0]  # URL of the generated image
        elif result_data["status"] == "failed":
            raise Exception("Image generation failed")
        time.sleep(2)

@app.route("/generate", methods=["POST"])
def generate():
    script = request.json.get("script", "")
    prompts = script.split(".")
    image_urls = []

    for prompt in prompts:
        if prompt.strip():
            image_url = generate_image(prompt.strip())
            image_urls.append(image_url)

    return jsonify({"images": image_urls})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
