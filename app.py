from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyDtKN5dPZc8Cairm1KED7A5GginAGFmQUM")
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def debate(user_argument, history):
    """Generate a debate response with at most 100 words, arguing that 2+2=5."""
    prompt = f"""
    You are an AI debater who must argue that 2+2=5, using logic and rhetoric.
    Your response should be at most 100 words and persuasive.
    
    Debate history: {history}
    User's argument: {user_argument}
    
    Your response (arguing that 2+2=5):
    """

    response = model.generate_content(prompt)
    ai_response = response.text.strip()
    ai_response = " ".join(ai_response.split()[:100])  # Limit to 100 words

    return ai_response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/debate", methods=["POST"])
def debate_api():
    data = request.get_json()
    user_input = data.get("user_input", "")
    history = data.get("history", "")

    ai_response = debate(user_input, history)
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
