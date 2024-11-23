from flask_mail import Message
from models import Professional, ServiceRequest
from extension import mail
from flask import current_app

def send_notification_email(professional_email, service_requests):
    with current_app.app_context():
        with open('static/mail/task_schedule.jpg', 'rb') as f:
            img_data = f.read()

        table = """
        <html>
            <body>
                <h3>Your Scheduled Service Requests</h3>
                <img src="cid:task_schedule_image" alt="Task Schedule" style="max-width: 100%; height: auto;">
                <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th>Service</th>
                            <th>Request Date</th>
                            <th>Request Status</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        for req in service_requests:
            table += f"""
                <tr>
                    <td>{req.service.serviceName}</td>
                    <td>{req.requestDate}</td>
                    <td>{req.professionalStatus}</td>
                </tr>
            """
        table += """
                    </tbody>
                </table>
            </body>
        </html>
        """

        msg = Message(
            subject="Service Requests Update",
            recipients=[professional_email],
            html=table  
        )

        msg.attach(
            filename='task_schedule.jpg',    
            content_type='image/jpeg',      
            data=img_data,                  
            disposition='inline',           
            headers={'Content-ID': '<task_schedule_image>'}  
        )

        # Send the email
        try:
            mail.send(msg)
            print(f"Email sent to {professional_email}")
        except Exception as e:
            print(f"Error sending email to {professional_email}: {e}")

def daily_email_task(app):
    with app.app_context():
        professionals = Professional.query.all()
        for professional in professionals:
            service_requests = ServiceRequest.query.filter_by(
                professionalId=professional.id, professionalStatus="accepted"
            ).all()
            if service_requests:
                send_notification_email(professional.email, service_requests)
