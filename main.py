from flask import Flask, request, jsonify, send_file, Response
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import base64

# Set up the Flask app
app = Flask(__name__)

# Set up the Stable Diffusion API client
stability_api = client.StabilityInference(
    key='',  # Replace with your Stability API key
    verbose=True,  # Set to True to enable verbose logging
    engine="stable-diffusion-xl-beta-v2-2-2"  # Replace with the engine you want to use
)

# Define the API endpoint for generating images
@app.route('/generate-image', methods=['POST'])
def generate_image():

    # Get the prompt and other parameters from the request
    data = request.json  # Get the request payload
    prompt = data.get('prompt')  # Prompt to generate the image from
    seed = data.get('seed', None)  # Set to None to use a random seed
    steps = data.get('steps', 30)  # Number of steps to run the diffusion for
    cfg_scale = data.get('cfg_scale', 8.0)  # Scale of the diffusion model
    width = data.get('width', 512)  # Width of the generated image
    height = data.get('height', 512)  # Height of the generated image
    samples = data.get('samples', 1)  # Number of samples to generate

    # Generate the image using Stable Diffusion
    answers = stability_api.generate(  # Call the generate() method
        prompt=prompt,
        seed=seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=samples,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    # Retrieve the generated image(s) from the response
    generated_images = []
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                encoded_image = base64.b64encode(artifact.binary).decode('utf-8')
                generated_images.append(encoded_image)

    # Return the generated image(s) as the API response
    return jsonify(images=generated_images)


# Define the API endpoint for the plugin logo
@app.route('/logo.png', methods=['GET'])
def plugin_logo():
    filename = 'logo.png'
    return send_file(filename, mimetype='image/png')


# Define the API endpoint for the plugin manifest
@app.route('/ai-plugin.json', methods=['GET'])
def plugin_manifest():
    host = request.headers['Host']
    with open('./ai-plugin.json') as f:
        text = f.read()
        return Response(text, mimetype='text/json')


# Define the API endpoint for the OpenAPI specification
@app.route('/openapi.yaml', methods=['GET'])
def openapi_spec():
    host = request.headers['Host']
    with open('./openapi.yaml') as f:
        text = f.read()
        return Response(text, mimetype='text/yaml')


# Run the Flask app
if __name__ == '__main__':
    # Set debug=True to enable auto-reloading when you make changes to the code
    app.run(debug=True, host='127.0.0.1', port=5000)

