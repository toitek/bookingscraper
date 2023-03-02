import csv
import re
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    # define the hostel name to search
    hostel_name = 'Shantee House'

    # define an empty list to store the hostels
    hostels = []

    # read the data from the CSV file
    with open('Hungary_data.csv', 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            hostels.append(row)

        # sort the hostels by price and rating
        hostels = sorted(hostels, key=lambda k: (float(re.sub(r'[^\d.]', '', k.get('MTPrice', '') or k.get('FSPrice', '') or k.get('SSPrice', ''))), float(k['ratings'])), reverse=False)

        # Find the rank of the input hostel based on price
        price_rank = None
        for i, h in enumerate(hostels):
            if h['Name'] == hostel_name:
                price_rank = i+1
                break

        # Find the rank of the input hostel based on rating
        rating_rank = None
        hostels_by_rating = sorted(hostels, key=lambda k: float(k['ratings']), reverse=True)
        for i, h in enumerate(hostels_by_rating):
            if h['Name'] == hostel_name:
                rating_rank = i+1
                break

        # Compose the email message with the hostel details
        msg = MIMEMultipart()
        msg['Subject'] = 'Your hostel details'
        msg['From'] = 'your@gmail.com'
        msg['To'] = 'your@gmail.com'

        msg_text = MIMEText(f'Your {hostel_name} hostel details:\n\n'
                            f'Price rank: {price_rank}\n'
                            f'Rating rank: {rating_rank}\n'
                            f'Hostels with a lower price:\n'
                            f'______\n'
                            f'Name :: Price :: Rating\n'
                            f'::::\n')
        msg.attach(msg_text)

        for h in hostels[:price_rank-1]:
            msg_text = MIMEText(f'{h["Name"]} :: {h["MTPrice"] or h["FSPrice"] or h["SSPrice"]} :: {h["ratings"]}\n')
            msg.attach(msg_text)

        # send the email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'your@gmail.com'
        # follow readme steps
        smtp_password = 'app_password'

        from_email = 'your@gmail.com'
        to_email = 'your@gmail.com'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())

        print('Email sent successfully!')

## uncomment this: if you want to get the results on monday 08.00 am

# # Schedule the email to be sent every Monday at 8:00 AM
# schedule.every().monday.at("08:00").do(send_email)

# # Loop indefinitely to run the scheduled jobs
# while True:
#     # Check if there are any scheduled jobs to run
#     schedule.run_pending()