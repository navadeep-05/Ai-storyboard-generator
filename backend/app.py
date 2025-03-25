from flask import Flask, request, jsonify
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS to allow Netlify frontend to connect

# Load Stable Diffusion model (requires GPU or cloud hosting)
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")  # Use GPU if available

@app.route("/generate", methods=["POST"])
def generate():
    script = request.json.get("script", "")
    prompts = script.split(".")  # Split into scenes
    image_urls = []

    # Ensure static directory exists
    if not os.path.exists("static"):
        os.makedirs("static")

    for i, prompt in enumerate(prompts):
        if prompt.strip():
            image = pipe(prompt.strip(), num_inference_steps=50).images[0]
            image_path = f"static/scene_{i}.png"
            image.save(image_path)
            # Return the URL relative to the backend
            image_urls.append(f"/{image_path}")

    return jsonify({"images": image_urls})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
