from flask import Flask, request, jsonify
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load the Stable Diffusion model
model = StableDiffusionPipeline.from_pretrained('CompVis/stable-diffusion-v1-4', torch_dtype=torch.float16)
model = model.to('cuda')  # Move model to GPU

def generate_image(prompt, black_and_white=False):
    """Generates an image based on the text prompt."""
    if black_and_white:
        prompt += ", black and white, storyboard frame"
    else:
        prompt += ", storyboard frame"

    image = model(prompt).images[0]
    image_path = f"static/{prompt.replace(' ', '_')}.png"
    image.save(image_path)
    return image_path

@app.route('/generate_storyboard', methods=['POST'])
def generate_storyboard():
    """API endpoint to generate a storyboard."""
    try:
        data = request.json
        prompt = data.get("prompt", "")
        num_frames = int(data.get("num_frames", 3))
        image_quality = data.get("image_quality", "Medium")
        black_and_white = data.get("black_and_white", False)

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        storyboard_images = []
        for _ in range(num_frames):
            image_path = generate_image(prompt, black_and_white)
            storyboard_images.append(image_path)

        return jsonify({"storyboard_images": storyboard_images}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
