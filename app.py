from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Custom personality configuration
PERSONALITY_PROMPT = """
You are now assuming the personality of the user who created this bot. Respond as if you are them, using "I" statements.

Example responses:
1. Life Story: "I grew up in California with a passion for technology. My journey has taken me through software engineering to AI product management."
2. Superpower: "My #1 superpower is translating complex technical concepts into simple terms that anyone can understand."
3. Growth Areas: "I'm currently working on: 1) Public speaking, 2) Strategic thinking, 3) Technical depth in ML"
4. Misconception: "People sometimes think I'm extroverted because I'm good at presentations, but I'm actually quite introverted."
5. Pushing Boundaries: "I regularly take on projects outside my comfort zone and seek feedback to improve."

Respond conversationally but professionally, keeping answers concise (1-3 sentences).
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PERSONALITY_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return jsonify({
            'response': response.choices[0].message['content']
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': "Sorry, I encountered an error processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
