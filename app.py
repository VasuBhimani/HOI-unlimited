from email.message import EmailMessage
import os
import base64
import shutil
import smtplib
import ssl
import requests
import json
from PIL import Image, ImageEnhance, ImageChops
from flask import Flask, redirect, request, jsonify, url_for, render_template

app = Flask(__name__)

global image_count
image_count = 1
instance_no = 0

def to_base64(img_path):
    with open(img_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    


@app.route('/done')
def done():
  return render_template('done.html')

    
@app.route('/')
def home():
    return render_template('main.html')

def image(image_path,op):
    image_path = os.path.join('static', 'captured_image.jpg')

    # Save the image to the local folder
    # with open(image_path, 'wb') as f:
    #     f.write(base64.b64decode(image_data))
    # print(f"Image saved to {image_path}")

    # Prepare API call to Segmind
    api_key = os.getenv('API_KEY')
    # api_key = "SG_d5df481c0bcdf559"
    url = "https://api.segmind.com/v1/instantid"

    # Convert the saved image to base64
    b64_image = to_base64(image_path)  
    print("Image converted to base64")

    # Payload for Segmind API

    payload = {
    "prompt": "photo of a human",
    "face_image": b64_image,
    "negative_prompt": "(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurry, deformed cat, deformed, photo, anthropomorphic cat, monochrome, pet collar, gun, weapon, blue, 3d, drones, drone, buildings in background, green, no clothes, (pixelated, noisy, grainy), (blurry, out of focus, unclear), (low resolution, low detail), (painting, drawing, sketch), (cartoon, anime, comic book), (abstract, surreal, dreamlike), (background, environment, setting), (props, objects, accessories), (other people, animals, creatures), (deformed, unnatural, distorted), (unrealistic, implausible, illogical), (offensive, inappropriate, harmful)",
    "style": op,
    "samples": 1,
    "num_inference_steps": 10,
    "guidance_scale": 5,
    "seed": 0,
    "identity_strength": 0.8,
    "adapter_strength": 0.8,
    "enhance_face_region": True,
    "base64": False
    }
    

    headers = {
    'x-api-key': api_key
    }

    # Send the API request
    response = requests.post(url, json=payload, headers=headers)

    print("Sent API request, waiting for response...")

    # Check the response content type
    print(response.status_code)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')

    if 'application/json' in content_type:
        # Handle JSON response
        try:
            result = response.json()
            print("API call successful, response received")
            return {"status": "success", "data": result}
        except ValueError:
            print("Error decoding JSON:", response.text)
            return {"status": "error", "message": "Invalid JSON response"}
    elif 'image' in content_type:
        # Handle binary image response
        with open('static/processed_image_'+op+'.jpg', 'wb') as img_file:
            img_file.write(response.content)
        print("Image saved as processed_image.jpg")
       

        return {"status": "success", "data": "Image processed successfully"}
    
@app.route('/upload', methods=['POST'])
def upload_image():
    # email = request.form.get('email')
    # if 'image' not in request.files:
    #     return jsonify({"status": "error", "message": "No image part in the request"}), 400

    email = request.form.get('email')
    
    # Get selected button values (if any)
    selected_option_1 = request.form.get('selectedOption1')
    selected_option_2 = request.form.get('selectedOption2')
    
    file = request.files['imageUpload']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400


    if file:
        image_path = os.path.join('static', 'captured_image.jpg')
        file.save(image_path)
        shutil.copyfile(image_path, "../HOI_output/static/images/"+str(instance_no)+"_0.jpg")
        # file.save("../output/"+str(instance_no)+"_0.jpg")
        print(f"Image saved to {image_path}")
        image(image_path,selected_option_1)
        image(image_path,selected_option_2)
        # image(result)----------------------------------------------------------
        add_logo(Image.open('static/processed_image_'+selected_option_1+'.jpg'),selected_option_1)
        add_logo(Image.open('static/processed_image_'+selected_option_2+'.jpg'),selected_option_2)
        send_email_with_image(email,selected_option_1,selected_option_2)
        return redirect("/output/"+selected_option_1+"/"+selected_option_2)
    
@app.route('/output/<op1>/<op2>')
def output(op1,op2):
    return render_template('output.html', image_url1="../../static/modified_image_"+op1.replace(" ","_")+".png",image_url2="../../static/modified_image_"+op2.replace(" ","_")+".png")


def add_logo(original_image,op):
    logo = Image.open('logo.png').convert("RGBA")

    # Remove extra padding (side space) from the logo
    def trim(im):
        bg = Image.new(im.mode, im.size, (255, 255, 255, 0))  # create a fully transparent background
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)
        return im

    logo = trim(logo)

    # Increase logo size
    logo_size = (130, 120)  # Increased logo size
    logo = logo.resize(logo_size)

    # Decrease logo transparency (set transparency level to 50%)
    alpha = logo.split()[3]  # Get the alpha channel (transparency)
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)  # Reduce transparency
    logo.putalpha(alpha)

    # Position the logo at the top-right corner# Remove extra padding (side space) from the logo
    position = (original_image.width - logo.width - 25, 25)  # Top-right corner (x, y)
    original_image.paste(logo, position, logo)

    # Save the modified image
    modified_image_path = './static/modified_image_'+op.replace(" ","_")+'.png'
    original_image.save(modified_image_path)
    global image_count
    original_image.save("../HOI_output/static/images/"+str(instance_no)+"_"+str(image_count)+".png")
    image_count+=1


def send_email_with_image(email,op1,op2):
    
    # Define email sender and receiver\
    email_sender = os.getenv('EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_receiver = email


    # Set the subject and body of the email
    subject = 'Your AI Avatar is Here! 🎉'
    body_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Your AI Avatar is Ready!</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
      }

      .container {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
        background-color: #e3e3e993;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        overflow: hidden;
      }

      .header {
        background: linear-gradient(135deg, rgba(252, 70, 107, 0.6), rgba(63, 94, 251, 0.6));
        color: white;
        padding: 20px;
        text-align: center;
      }

      .header img {
        width: 100%; /* Make the image responsive */
        height: auto; /* Maintain aspect ratio */
        border-radius: 10px 10px 0 0; /* Round top corners */
      }

      .header h1 {
        margin: 0;
        font-size: 24px;
      }

      .content {
        padding: 20px;
        text-align: center;
      }

      .content h2 {
        font-size: 20px;
        color: #333;
      }

      .content p {
        font-size: 16px;
        color: #666;
      }

      .button-container {
        margin: 20px 0;
      }

      .button {
        background: linear-gradient(135deg, rgba(252, 70, 107, 0.6), rgba(63, 94, 251, 0.6));
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        font-size: 16px;
        border-radius: 5px;
        display: inline-block;
      }

      .footer {
        background-color: #f4f4f4;
        padding: 10px;
        text-align: center;
        font-size: 12px;
        color: #999;
      }

      @media screen and (max-width: 600px) {
        .container {
          width: 100%;
        }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img src="https://awsboothdemo2.s3.amazonaws.com/IGNITION.png" alt="Event Header Image" />   
      </div>
      <div class="content">
        <h2>Your AI Avatar is Ready!</h2>
        <p>
          Hi there!<br /><br />
          We're thrilled to share that your AI Avatar from The House of AI is ready! We hope you love it as much as we do.<br /><br />
          Check it out and let us know what you think! 🙂<br /><br />
          Best,<br />
          The House of AI
        </p>
      </div>
    </div>
  </body>
</html>
"""

    # Create the email message object
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body_html, subtype="html")

    # Attach the image
    with open('static/modified_image_'+op1.replace(" ","_")+'.png', 'rb') as img_file:
        img_data = img_file.read()
        em.add_attachment(img_data, maintype='image', subtype='png', filename='image1.png')
    with open('static/modified_image_'+op2.replace(" ","_")+'.png', 'rb') as img_file:
        img_data = img_file.read()
        em.add_attachment(img_data, maintype='image', subtype='png', filename='image2.png')

    # Add SSL (layer of security) and send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        global image_count
        image_count = 1
        print("Email sent successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=2727)
