"""Mail Service"""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from fastapi import HTTPException

from app.core.settings import settings


class MailService:
    """Service to send emails."""

    def __init__(self):
        """Initialize the mail service."""
        self.sender_email = settings.email.MAIL_USER_INFO
        self.sender_password = settings.email.MAIL_PASS_INFO

    def send_finished_assessment_email(self, receiver_email: str, assessment_title: str):
        """Send a finished assessment email to the user with HTML content."""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "[MOCKHAT] Assessment finished"

            # HTML del correo con estilos inline
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                     <div style="text-align: center; margin-bottom: 30px;">
                        <img src="https://app.mockhat.com/assets/images/mockhat.png"
                             alt="MOCKHAT Logo"
                             style="width: 150px; height: auto;">
                    </div>
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                        <h2 style="color: #333; margin-bottom: 20px;">Assessment finished</h2>
                        <p>The assessment <strong>{assessment_title}</strong> has been finished.</p>
                        <p>You can see the results <a href="{settings.app.FRONTEND_URL}">in the app</a> </p>
                        </div>
                </body>
            </html>
            """

            part2 = MIMEText(html, 'html', 'utf-8')
            msg.attach(part2)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email,
                                receiver_email, msg.as_string())

        except smtplib.SMTPAuthenticationError as e:
            logging.error("Authentication error: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending finished assessment email") from e

        except smtplib.SMTPException as e:
            logging.error("Error al enviar el correo: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending finished assessment email") from e

        except Exception as e:
            logging.error("Error al enviar el correo: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending finished assessment email") from e

    def send_invite_user_to_account_email(self, receiver_email: str, token: str, account_name: str):
        """Send a invite user to account email to the user with HTML content."""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "[MOCKHAT] Invite to account"

            # HTML del correo con estilos inline
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img src="https://app.mockhat.com/assets/images/mockhat.png"
                             alt="MOCKHAT Logo"
                             style="width: 150px; height: auto;">
                    </div>
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                        <h2 style="color: #333; margin-bottom: 20px;">Invite to account</h2>
                        <p>You have been invited to join the account <strong>{account_name}</strong>.</p>
                        <p>Click the button below to accept the invite:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{settings.app.FRONTEND_URL}/auth/invite-user-to-account?token={token}"
                               style="background-color: #007bff; color: white; padding: 12px 30px;
                                      text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Accept Invite
                            </a>
                        </div>
                        <p style="color: #666; font-size: 0.9em;">
                            If the button doesn't work, copy and paste this link in your browser:<br>
                            <a href="{settings.app.FRONTEND_URL}/auth/invite-user-to-account?token={token}" style="color: #007bff;">
                                {settings.app.FRONTEND_URL}/auth/invite-user-to-account?token={token}
                            </a>
                        </p>
                    </div>
                </body>
            </html>
            """

            part2 = MIMEText(html, 'html', 'utf-8')
            msg.attach(part2)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email,
                                receiver_email, msg.as_string())

        except smtplib.SMTPAuthenticationError as e:
            logging.error("Authentication error: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending invite user to account email") from e

        except smtplib.SMTPException as e:
            logging.error("Error al enviar el correo: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending invite user to account email") from e

        except Exception as e:
            logging.error("Error al enviar el correo: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending invite user to account email") from e

    def send_forgot_password_email(self, receiver_email: str, token: str):
        """Send a forgot password email to the user with HTML content."""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "[MOCKHAT] Reset your password"

            # HTML del correo con estilos inline
            html = f"""
            <html >
                <body style = "font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;" >
                     <div style = "text-align: center; margin-bottom: 30px;" >
                        <img src = "https://app.mockhat.com/assets/images/mockhat.png"
                             alt = "MOCKHAT Logo"
                             style = "width: 150px; height: auto;" >
                    </div>
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;"> 
                        <h2 style="color: #333; margin-bottom: 20px;">Reset your password</h2>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{settings.app.FRONTEND_URL}/auth/reset-password?token={token}"   
                               style="background-color: #007bff; color: white; padding: 12px 30px; 
                                      text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Reset Password
                            </a>
                        </div>
                        <p style="color: #666; font-size: 0.9em;">  
                            If the button doesn't work, copy and paste this link in your browser:<br>
                            <a href="{settings.app.FRONTEND_URL}/auth/reset-password?token={token}" style="color: #007bff;">
                                {settings.app.FRONTEND_URL}/auth/reset-password?token={token}
                            </a>
                        </p>
                    </div>  
                </body>
            </html>
            """

            part2 = MIMEText(html, 'html', 'utf-8')
            msg.attach(part2)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email,
                                receiver_email, msg.as_string())

        except smtplib.SMTPAuthenticationError as e:
            logging.error("Authentication error: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending forgot password email") from e

        except smtplib.SMTPException as e:
            logging.error("Error al enviar el correo: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending forgot password email") from e

        except Exception as e:
            logging.error("Error al enviar el correo: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending forgot password email") from e

    def send_verify_register_email(self, receiver_email: str, token: str):
        """Send a verify register email to the user with HTML content."""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "[MOCKHAT] Verify your email"

            # HTML del correo con estilos inline
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img src="https://app.mockhat.com/assets/images/mockhat.png" 
                             alt="MOCKHAT Logo" 
                             style="width: 150px; height: auto;">
                    </div>
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                        <h2 style="color: #333; margin-bottom: 20px;">Verify your email address</h2>
                        <p style="color: #666; line-height: 1.6;">
                            Welcome to MOCKHAT! Please click the button below to verify your email address:
                        </p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{settings.app.FRONTEND_URL}/auth/verify-register?token={token}"
                               style="background-color: #007bff; color: white; padding: 12px 30px; 
                                      text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Verify Email
                            </a>
                        </div>
                        <p style="color: #666; font-size: 0.9em;">
                            If the button doesn't work, copy and paste this link in your browser:<br>
                            <a href="{settings.app.FRONTEND_URL}/auth/verify-register?token={token}" style="color: #007bff;">
                                {settings.app.FRONTEND_URL}/auth/verify-register?token={token}
                            </a>
                        </p>
                    </div>
                </body>
            </html>
            """

            part2 = MIMEText(html, 'html', 'utf-8')
            msg.attach(part2)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email,
                                receiver_email, msg.as_string())

        except smtplib.SMTPAuthenticationError as e:
            logging.error("Authentication error: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending verification email") from e

        except smtplib.SMTPException as e:
            logging.error("Error al enviar el correo: %s", e)
            raise HTTPException(
                status_code=500, detail="Error sending verification email") from e

        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error sending verification email") from e
