import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import gmail_password as pw

#User input email
# receiver_email = input("Email:")

async def send_email(receiver_email: str, record: dict, template: dict, filename: str)->bool:
    """
    This function sends the pdf file
    from the inspector to the email
    passed in as a parameter
    """    
    #Gmail and password of bot
    sender_email = "tele.bot202@gmail.com"
    password = pw.password

    project_title = record[0]['value']
    date_done = record[-1]['value']
    submitter = record[-2]['value']
    # email_address = next(filter(lambda x: x['key']=='email', tracked['record']))['value']

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = "Form Telegram Bot"
    message["To"] = receiver_email
    message["Subject"] = "{}: {} on {}".format(project_title, template['document_title'], date_done)
    
    body = """Hi,

Please see the attached report for the inspection conducted at {} on {}. 

Thank you.
    
Regards,
{}""".format(project_title, date_done, submitter)

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open('./generated pdf/' + filename + '.pdf', "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}.pdf",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)     
    
    return True
        
# send_email(receiver_email)

        




