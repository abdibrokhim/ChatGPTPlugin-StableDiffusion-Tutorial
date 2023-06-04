import requests
import json
import base64

# Define the API endpoint URL
url = 'http://127.0.0.1:5000/generate-image'

# Set up the request payload
payload = {
    'prompt': 'Harry Potter is a wizard in training at Hogwarts School of Witchcraft and Wizardry. He is in his third year at Hogwarts. He is best friends with Ron Weasley and Hermione Granger. He is the son of James Potter and Lily Potter, who were killed on October 31, 1981. He is the Godson of Sirius Black. He is the cousin of Dudley Dursley, who is a bully. He is the nephew of Petunia Dursley and Vernon Dursley.',
    'seed': 992446758,
    'steps': 30,
    'cfg_scale': 8.0,
    'width': 512,
    'height': 512,
    'samples': 1
}

# Send the POST request to generate the image
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Get the generated images from the response
    data = response.json()
    generated_images = data['images']

    # Process the generated images
    for i, encoded_image in enumerate(generated_images):
        # Decode the base64-encoded image
        decoded_image = base64.b64decode(encoded_image)

        # Save the image to a file
        image_filename = 'demo_4.png'
        with open(image_filename, 'wb') as image_file:
            image_file.write(decoded_image)

        print(f'Saved generated image {i+1} as {image_filename}')
else:
    print(f'Request failed with status code {response.status_code}')


