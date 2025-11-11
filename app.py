from flask import Flask, render_template, request, jsonify
import wikipedia
import random
import re

app = Flask(__name__)

# Some friendly fallback replies
small_talk = {
    "greeting": ["Hello there!", "Hi! How can I help you today?", "Hey, nice to see you!"],
    "feeling": ["I'm just a bot, but I'm feeling great!", "I'm doing awesome, thanks for asking!"],
    "thanks": ["You're welcome!", "Glad I could help!", "Anytime!"],
    "unknown": ["I'm not sure about that.", "Let me think...", "Could you ask that differently?"]
}

# Intent detection
def detect_intent(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["hi", "hello", "hey"]):
        return "greeting"
    elif "how are you" in user_input:
        return "feeling"
    elif "thank" in user_input:
        return "thanks"
    else:
        return "wiki"

# Generate chatbot reply
def generate_reply(user_input):
    intent = detect_intent(user_input)

    if intent in small_talk:
        return random.choice(small_talk[intent])
    elif intent == "wiki":
        try:
            result = wikipedia.summary(user_input, sentences=2)
            return result
        except wikipedia.DisambiguationError as e:
            return f"That topic is too broad. Try something specific like: {e.options[0]}"
        except Exception:
            return random.choice(small_talk["unknown"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_message = request.form["msg"]
    bot_reply = generate_reply(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
