from flask import Flask, request, render_template_string
import boto3
import random

app = Flask(__name__)

# Initialize AWS clients (make sure region matches your SES/SNS region)
ses_client = boto3.client('ses', region_name='ap-south-1')
sns_client = boto3.client('sns', region_name='ap-south-1')

def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not email or not phone:
            return "Please provide both email and phone number"

        otp = generate_otp()

        # Send Email via SES
        try:
            ses_client.send_email(
                Source='tharun.kunuthuru@enhub.ai',
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': 'Your OTP Code'},
                    'Body': {'Text': {'Data': f'Your OTP is: {otp}'}}
                }
            )
        except Exception as e:
            return f"Failed to send email: {e}"

        # Send SMS via SNS
        try:
            sns_client.publish(
                PhoneNumber=phone,
                Message=f'Your OTP is: {otp}'
            )
        except Exception as e:
            return f"Failed to send SMS: {e}"

        return f"OTP sent to {email} and {phone}"

    # Simple HTML form
    return render_template_string('''
        <form method="post">
          Email: <input name="email" type="email" required><br>
          Phone: <input name="phone" type="text" placeholder="+911234567890" required><br>
          <input type="submit" value="Get OTP">
        </form>
    ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
