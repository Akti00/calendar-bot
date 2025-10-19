from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os, datetime

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_command():
    data = request.get_json()
    command = data.get("command", "").lower()

    creds = Credentials(
        None,
        refresh_token=os.environ["REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=creds)

    if "добавь" in command and "работу" in command:
        tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        start = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        end = tomorrow.replace(hour=17, minute=0, second=0, microsecond=0)
        event = {
            "summary": "Работа",
            "start": {"dateTime": start.isoformat() + "Z"},
            "end": {"dateTime": end.isoformat() + "Z"}
        }
        service.events().insert(calendarId="primary", body=event).execute()
        return jsonify({"status": "ok", "message": "Событие 'Работа' добавлено!"})

    return jsonify({"status": "ok", "message": f"Команда '{command}' получена."})

