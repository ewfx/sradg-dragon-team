import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


class MailSender:
    def __init__(self,smtp_server,smtp_port,sender_email,passwd):
        self._sender_email = sender_email
        self._smtp_server = smtplib.SMTP(smtp_server,smtp_port)
        self._smtp_server.starttls()
        self._smtp_server.login(sender_email,passwd)


    def send_email_with_csv(self,receiver_email,csv_file_path,subject = "Automated Email for Anomaly found",body = "This is an automated email sent to notify that anomaly detected in the following data attached"):
        try:
            message = MIMEMultipart()
            message['From'] = self._sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body,'plain'))
            with open(csv_file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={random_filename}")
                message.attach(part)

            self._smtp_server.sendmail(self._sender_email, receiver_email, message.as_string() )
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self._smtp_server.quit()
