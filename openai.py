import base64
import requests
import os

# OpenAI API Key
api_key = "OPENAI_API_KEY"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to process images in a folder
def process_images_in_folder(folder_path):
    for image_filename in os.listdir(folder_path):
        if image_filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Add more image formats if needed
            image_path = os.path.join(folder_path, image_filename)
            print(f"Processing image: {image_filename}")
            base64_image = encode_image(image_path)
            
            # Prepare the payload for each image
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """WRITE A PROMPT"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            }
            
            # Set up headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            # Send request to OpenAI API
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            # Print the response from the API
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                print(f"Response for {image_filename}:\n{content}\n")
            else:
                print(f"Failed to process {image_filename}. Status Code: {response.status_code}")

# Path to the folder containing images
folder_path = "FOLDER PATH"

# Process all images in the folder
process_images_in_folder(folder_path)


    