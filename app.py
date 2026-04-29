from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

chat_history = []

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "")

    chat_history.append({"role": "user", "content": incoming_msg})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Reply in Marathi and English."},
            *chat_history
        ]
    )

    reply = response.choices[0].message.content

    chat_history.append({"role": "assistant", "content": reply})

    resp = MessagingResponse()
    resp.message(reply)

    return str(resp)

@app.route("/")
def home():
    return "Bot Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
