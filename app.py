from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from incident_log_api.config import DATABASE_URL
from incident_log_api.db import db
from incident_log_api.models import Incident

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)
migrate = Migrate(app, db)

VALID_SEVERITIES = ["Low", "Medium", "High"]

@app.route("/incidents", methods=["GET"])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([
        {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "severity": i.severity,
            "reported_at": i.reported_at.isoformat()
        } for i in incidents
    ])

@app.route("/incidents", methods=["POST"])
def create_incident():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    severity = data.get("severity")

    if not title or not description or severity not in VALID_SEVERITIES:
        return jsonify({"error": "Invalid input"}), 400

    incident = Incident(title=title, description=description, severity=severity)
    db.session.add(incident)
    db.session.commit()

    return jsonify({
        "id": incident.id,
        "title": incident.title,
        "description": incident.description,
        "severity": incident.severity,
        "reported_at": incident.reported_at.isoformat()
    }), 201

@app.route("/incidents/<int:incident_id>", methods=["GET"])
def get_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        abort(404)

    return jsonify({
        "id": incident.id,
        "title": incident.title,
        "description": incident.description,
        "severity": incident.severity,
        "reported_at": incident.reported_at.isoformat()
    })

@app.route("/incidents/<int:incident_id>", methods=["DELETE"])
def delete_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        abort(404)

    db.session.delete(incident)
    db.session.commit()
    return '', 204
