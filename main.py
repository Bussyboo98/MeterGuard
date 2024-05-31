import random
import datetime
from twilio.rest import Client
from decouple import config
import smtplib
from email.mime.text import MIMEText
import logging



# Configure logging
logging.basicConfig(filename='bypass_detection.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# The line is configuring the logging module in Python. 
# Twilio credentials
#SMS configuration 
# account_sid = config('TWILIO_ACCOUNT_SID')
# auth_token = config('TWILIO_AUTH_TOKEN')
# twilio_number = config('TWILIO_PHONE_NUMBER')
# recipient_number = config('RECIPIENT_PHONE_NUMBER')

# client = Client(account_sid, auth_token)


# Email configuration
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
RECIPIENT_EMAIL = config('RECIPIENT_EMAIL')


# Define meter IDs and addresses
meter_addresses = {
    'meter1': 'Address 1',
    'meter2': 'Address 2',
    'meter3': 'Address 3',
    }

# Verification units
VERIFICATION_UNITS = 100 

# Read email bypass message from file
with open('email-bypass.txt', 'r') as file:
    email_bypass = file.read()

# Read SMS bypass message from file
with open('sms-bypass.txt', 'r') as file:
    sms_bypass= file.read()



# Function to verify connection to the prepaid meter
def verify_connection():
    if random.random() < 0.9:  # 90% chance of successful verification
        return True, None
    else:
        # Return a random meter ID for demonstration purposes
        meter_id = random.choice(list(meter_addresses.keys()))
        return False, meter_id



# Simulate data for a week
start_date = datetime.date.today()
end_date = start_date + datetime.timedelta(days=7)
current_date = start_date

# Initialize variables
remaining_credit = 100  # Initial credit
# remaining_credit = 10  # Initial credit  bypassed  iit send mail and sms

consumed_units = 0

# Simulate data for each day
while current_date < end_date:
    # Check if there are enough verification units
    if VERIFICATION_UNITS <= 0:
        logging.info("No verification units left. Cannot perform verification.")
        break  # Exit the loop if no verification units left
    
    
    # Simulate electricity consumption
    daily_consumption = random.randint(10, 50)  # Random consumption between 10 and 50 units
    consumed_units += daily_consumption


    # Simulate credit deduction
    credit_deduction = random.randint(5, 20)  # Random deduction between 5 and 20 units
    remaining_credit -= credit_deduction
    
    # Verify connection to the prepaid meter
    verification_result, meter_id = verify_connection()
    
    # Simulate credit deduction for verification only if verification is successful
    if verification_result:
        verification_deduction = random.randint(5, 20)  # Random deduction between 5 and 20 units
        VERIFICATION_UNITS -= verification_deduction
        
        


    if not verification_result:
        if meter_id:
            address = meter_addresses.get(meter_id, 'Unknown Address')
        else:
            address = 'Unknown Address'

        message = "Verification failed. Possible bypass detected on {current_date}. " \
                  "Address of the user: {address}".format(current_date=current_date, address=address)



    # Check for bypass
    if consumed_units > remaining_credit:
        # Send SMS alert to the admin using Twilio
        
        # try:
        # # Send SMS alert to the admin using Twilio
        #     sms_message = sms_bypass.format(current_date=current_date, consumed_units=consumed_units, remaining_credit=remaining_credit)
        #     client.messages.create(
        #         body=sms_message,
        #         from_=twilio_number,
        #         to=recipient_number
        #     )
        #     logging.info("SMS alert sent for bypass detected on %s", current_date)
        # except Exception as e:
        #     logging.error("Failed to send SMS alert: %s", str(e))

        # Send email alert to the admin using
        # This block of code is responsible for sending an email alert to the admin when a bypass is
        # detected in the prepaid meter system. 
        try:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                email_message = email_bypass.format(current_date=current_date, consumed_units=consumed_units, remaining_credit=remaining_credit, )
                msg = MIMEText(email_message)
                msg['From'] = EMAIL_HOST_USER
                msg['To'] = RECIPIENT_EMAIL
                msg['Subject'] = 'Prepaid Meter Bypass Detected'
                server.sendmail(EMAIL_HOST_USER, RECIPIENT_EMAIL , msg.as_string())
                logging.info("Sending email from %s to %s", EMAIL_HOST_USER, RECIPIENT_EMAIL)
                logging.info("Email alert sent for bypass detected on %s", current_date)
        # The `except Exception as e:` block in the code snippet is used for exception handling.
        except Exception as e:
            logging.error("Failed to send email alert: %s", str(e))



    # Move to the next day
    current_date += datetime.timedelta(days=1)

    # Reset consumed units if it's a new week
    if current_date.weekday() == 0:  # Monday
        consumed_units = 0

    # Add some variation in remaining credit
    remaining_credit += random.randint(-10, 10)  # Random change between -10 and 10 units

    # Ensure remaining credit doesn't go negative
    remaining_credit = max(remaining_credit, 0)

    # Print remaining credit at the end of each day
    print(f"On {current_date}, Remaining Credit: {remaining_credit}")




