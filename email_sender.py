import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()


def send_email(data) -> bool:
    """
    Send an email when using the contact form

    :param data: (dict) information to put in the email
    :return: {bool} True if success
    """
    # constants
    html = Template(Path('email_template.html').read_text())
    email = EmailMessage()
    email['to'] = 'fromjackg@gmail.com'
    name = data['name']
    email['from'] = name
    email['subject'] = 'Message from ' + name

    email.set_content(html.substitute({
        'name': name,
        'email': data['email'],
        'message': data['message'].strip()}), 'html'
    )

    pwd = os.getenv('GMAIL_PWD')

    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('fromjackg@gmail.com', pwd)
            smtp.send_message(email)
            print('email sent')
        success = True
    except:
        success = False
        print('oh nooooooo')
    print(success)
    return success


# if __name__ == '__main__':
#     data = {
#         'name': 'the file',
#         'email': 'fromjackg@gmail.com',
#         'message': 'placeholder'
#     }
#     send_email(data)
