from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
from io import BytesIO
from torch import autocast
from contextlib import nullcontext
from authtoken import auth_token
import logging

app = Flask(__name__, static_url_path='/static')
CORS(app)  # Allow cross-origin requests

logging.basicConfig(level=logging.DEBUG)

modelid = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    modelid,
    revision="fp16" if torch.cuda.is_available() else "main",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    use_auth_token=auth_token
)
pipe.to(device)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')
    logging.debug(f"Received prompt: {prompt}")
    
    if not prompt:
        logging.error('Prompt is required')
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        with autocast(device) if torch.cuda.is_available() else nullcontext():
            result = pipe(prompt, guidance_scale=8.5)
            image = result.images[0]
        
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        logging.debug('Image generated successfully')
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
