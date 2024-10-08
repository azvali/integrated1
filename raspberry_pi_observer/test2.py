import requests
import base64
from picamera2 import Picamera2
from time import sleep
from datetime import datetime





current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
image_path = f"/home/yousef/Desktop/captured_image_{current_time}.jpg"
    
api_key = {OPENAI_API_KEY}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def capture_image():
    picam2 = Picamera2()
    picam2.start()
    sleep(2)  
    
    
    
    
    
    picam2.capture_file(image_path)
    picam2.stop()
    
    return image_path



capture_image()


base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Look at this image of a parking lot and guess the availability of parking spaces. Based on what you can infer from the image, respond with one of the following: 'very high,' 'high,' 'medium,' 'low,' or 'very low,' depending on how full or empty the parking lot appears to be. If the image is not an image of a parking lot respond with \"Not a parking lot.\" Only respond with a 1 word response."
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
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

if response.status_code == 200:
    response_json = response.json()
   
    description = response_json['choices'][0]['message']['content']
    print(description)
else:
    print(f"Error: {response.status_code}")
    print(response.text)