from flask import Flask, render_template, request
import boto3
import random
import os

app = Flask(__name__)

# Load from environment or hardcode
AWS_REGION = "us-east-1"
SES_SENDER = os.getenv("SES_SENDER", "verified_email@example.com")

# Clients
ses_client = boto3.client('ses', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)

def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        otp = generate_otp()

        subject = "Your OTP Code"
        body = f"Your OTP code is {otp}"

        # Send Email
        ses_client.send_email(
            Source=SES_SENDER,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )

        # Send SMS
        sns_client.publish(
            PhoneNumber=phone,
            Message=body
        )

        return f"<h3>OTP sent to {email} and {phone}</h3>"

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
