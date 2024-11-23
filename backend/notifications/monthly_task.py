from flask_mail import Message
from models import Customer, ServiceRequest
from extension import mail
from flask import current_app

def send_monthly_report_email(customer_email, service_requests):
    with current_app.app_context():
        with open('static/mail/report.jpg', 'rb') as f:
            img_data = f.read()

        table = """
        <html>
            <body>
                <h2 style="color: blue;">Your Monthly Service Report</h2>
                <img src="cid:report_image" alt="Monthly Report" style="margin-bottom: 5px; max-width: 100%; height: auto;">
                <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th>Service</th>
                            <th>Status</th>
                            <th>Review</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        for req in service_requests:
            review = req.reviewed if req.reviewed == "yes" else "Not reviewed yet"
            table += f"""
                <tr>
                    <td>{req.service.serviceName}</td>
                    <td>{req.professionalStatus}</td>
                    <td>{review}</td>
                </tr>
            """
        table += """
                    </tbody>
                </table>
            </body>
        </html>
        """

        msg = Message(
            subject="Your Monthly Service Report",
            recipients=[customer_email],
            html=table
        )

        msg.attach(
            filename="report.jpg", 
            content_type="image/jpeg",  
            data=img_data,  
            disposition="inline", 
            headers={"Content-ID": "<report_image>"}  
        )

        # Send the email
        try:
            mail.send(msg)
            print(f"Monthly report sent to {customer_email}")
        except Exception as e:
            print(f"Error sending email to {customer_email}: {e}")

def monthly_email_task(app):
    with app.app_context():
        customers = Customer.query.all()
        for customer in customers:
            service_requests = ServiceRequest.query.filter_by(customerId=customer.id).all()

            if service_requests:
                send_monthly_report_email(customer.email, service_requests)
