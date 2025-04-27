from incident_log_api.app import app, db
from incident_log_api.models import Incident

with app.app_context():
    db.create_all()

    db.session.add_all([
        Incident(title="Bias in hiring algorithm", description="Discrimination against minorities", severity="High"),
        Incident(title="Chatbot spreading misinformation", description="Chatbot gave wrong medical advice", severity="Medium")
    ])
    db.session.commit()
