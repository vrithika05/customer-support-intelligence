from flask import Flask
from config import Config
from .models import db
from .services.ml import get_model


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        get_model()
        from .routes import bp
        app.register_blueprint(bp)
        seed_database()
    return app


def seed_database():
    from .models import User, Ticket
    if User.query.count() == 0:
        db.session.add(User(name='Admin User', email='admin@example.com', password='admin123', role='admin'))
    if Ticket.query.count() == 0:
        rows = [
            ('Aarav Sharma','aarav@example.com','Unable to login','I cannot login to my account after resetting my password.','Technical','Negative','High','Resolved',2,1.2,5.5),
            ('Diya Patel','diya@example.com','Great support','The agent helped me quickly and the issue is completely solved.','Support','Positive','Low','Resolved',5,0.4,1.8),
            ('Rahul Kumar','rahul@example.com','Billing clarification','Please explain the latest charge on my account.','Billing','Neutral','Medium','Open',0,3.0,0),
            ('Ananya Rao','ananya@example.com','Refund pending','My refund has not arrived and I am very disappointed.','Billing','Negative','High','In Progress',1,12.0,0),
            ('Vikram Singh','vikram@example.com','Feature question','How can I export my monthly report?','Product','Neutral','Low','Resolved',4,1.0,3.0),
            ('Meera Iyer','meera@example.com','Excellent experience','Thank you for the fast and helpful response.','Support','Positive','Low','Resolved',5,0.3,1.2),
            ('Kiran Das','kiran@example.com','Application error','The dashboard crashes whenever I open reports.','Technical','Negative','High','In Progress',2,5.5,0),
            ('Sneha Reddy','sneha@example.com','Account settings','I need help changing my profile information.','Account','Neutral','Medium','Open',0,2.2,0),
        ]
        for r in rows:
            db.session.add(Ticket(customer_name=r[0], customer_email=r[1], subject=r[2], description=r[3], category=r[4], sentiment=r[5], priority=r[6], status=r[7], csat=r[8], response_time_hours=r[9], resolution_time_hours=r[10]))
    db.session.commit()
