import re
import json
import thread
from flask import request
from werkzeug.exceptions import BadRequest

from .app import app, secret_webhook_uuid
from .models import Document


@app.route('/webhook/%s' % secret_webhook_uuid, methods=['POST', 'GET'])
def webhook():
    """
    Borrowed from Django-Draftin
    github.com/whatisjasongoldstein/django-draftin

    Expected payload:

    {   
    "id": your_document_id,
    "name": "The Name of your Document",
    "content": "The plain-text markdown of your document",
    "content_html": "Your document rendered as HTML",
    "user": {
        id: 1, 
        email: 'usersemail@example.com'
    },
    "created_at": "2013-05-23T14:11:54-05:00",
    "updated_at": "2013-05-23T14:11:58-05:00"
    }
    """

    try:
        data = json.loads(request.form.get("payload"))
    except Exception:
        raise BadRequest("Something is wrong with your post.")

    try:
        doc = Document.get(draft_id=data["id"])
    except Document.DoesNotExist:
        doc = Document(draft_id=data["id"])

    doc.title = data["name"]
    doc.content = data["content"]
    doc.content_html = data["content_html"]
    doc.draftin_user_id = data["user"]["id"]
    doc.draftin_user_email = data["user"]["email"]
    doc.created_at = data["created_at"]
    doc.updated_at = data["updated_at"]
    doc.save()

    thread.start_new_thread(doc.download_images, ())

    return "ok"