
# Prepaid Meter Bypass Detection System

This software is designed to detect when a prepaid meter is bypassed by monitoring the electricity consumption and verifying the connection to the prepaid meter.


This software is designed to detect when a prepaid meter is bypassed. It simulates the operation of a prepaid meter, including verifying the connection to the meter and detecting potential bypass events. The system uses SMS and email alerts to notify the system admin of any suspected bypass.

## Features

- Simulates electricity consumption and verifies the connection to the prepaid meter.
- Sends SMS and email alerts to the system admin when a bypass is detected.
- Logs bypass detection events for further analysis.


This code simulates a prepaid meter system and detects potential bypass events. Here's an explanation of the key parts:

Logging Configuration: The logging.basicConfig function sets up logging to write messages to a file (bypass_detection.log) with a specific format.

Twilio Configuration: Twilio credentials are loaded using config from the environment variables. These credentials are used to send SMS alerts.

Email Configuration: SMTP email configuration is set up to send email alerts. Email host, port, username, and password are loaded from the environment variables.



Verification Units: VERIFICATION_UNITS represents the number of units available for verification. This is decremented when verification is attempted.

Email and SMS Templates: Email and SMS templates are read from files (email-bypass.txt and sms_bypass.txt) to customize the alert messages.

Verification Function: The verify_connection function simulates the verification process. It returns a boolean indicating if the verification was successful and the meter ID if verification fails.

Simulation Loop: The code simulates a week of operation. Each day, it simulates electricity consumption and deducts credits. It also attempts to verify the connection to the meter and checks for bypass events.

Bypass Detection: If the consumed units exceed the remaining credit, a bypass is detected. An SMS alert is sent using Twilio, and an email alert is sent using SMTP. The email includes details such as the date, consumed units, remaining credit, and the address of the user.

Error Handling: Email sending is wrapped in a try-except block to handle any exceptions that may occur during the email sending process. If an error occurs, it is logged using the logging.error function.

Iteration and Reset: The code iterates through each day, resets consumed units at the start of a new week, and adds some variation to the remaining credit.