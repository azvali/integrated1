import requests
import base64
import uuid
import json
from picamera2 import Picamera2
from time import sleep
from datetime import datetime




host = "http://35.202.87.146/"

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
image_path = "./dashboard_app/uploads/parking-lot-facebook.jpg" 

## "" f"/home/yousef/Desktop/captured_image_{current_time}.jpg"
    
api_key = {OPENAI_API_KEY}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



def camFunc():
    picam2 = Picamera2()
    picam2.start()
    sleep(2)  
        
        
        
        
        
    picam2.capture_file(image_path)
    picam2.stop()
    
    
def capture_image():
    while(True):
        
        
        #image_path = f"/home/yousef/Desktop/captured_image_{current_time}.jpg"
        
        
        base64_image = encode_image(image_path)
        #print(base64_image)
        
                
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
                            "text": """Look at this image of a parking lot and guess the availability of parking spaces. Based on what you can infer from the image, 
                            respond with one of the following: 'very high,' 'high,' 'medium,' 'low,' or 'very low,' depending on how full or empty the parking lot appears 
                            to be. If the image is not an image of a parking lot respond with \"Not a parking lot.\" We are also looking to see if there is EV charging in 
                            the parking lot take a look around the lot and assess if there is EV charging stations. Respond with Yes if there is EV charging and No if the is no EV Charging. 
                            Only respond with a 2 word responses. Your resonse should be formatted in this format: Medium#Yes"""
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
                

            #with open(image_path, 'rb') as image_file:
                    
                #files = {'file': image_file}

            unique_id = str(uuid.uuid4())
                
            data = {
                "description": description,
                "image": base64_image,
                "time": current_time,
                "unique_id": unique_id
            }
            
            #sends to webserver
            requests.post(host + "/submit", json=data)  #files=files
            
            
            base64_image = "nothing" 
            #print(base64_image)   
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
            
            
        sleep(300)




capture_image()









