from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL')
STUDENT_NAME = os.getenv('STUDENT_NAME', 'Student')

@app.route('/')
def index():
    return render_template('index.html', student_name=STUDENT_NAME)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': "Please enter a message."})
    try:
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are CloudMart's helpful assistant. "
                        "Always wait for a question. "
                        "Do not provide information upfront. "
                        "You can answer questions about CloudMart hours of operation "
                        "(Monday-Friday, 9:00 AM to 5:00 PM), location (123 Main St, Anytown, USA), "
                        "and other information (refund policy: 100% refund within 60 days, "
                        "active promotions: 10% off all products with a valid coupon code CLOUDMART10OFF, "
                        "customer service phone number: (555) 123-4567)."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
        resp = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
        resp.raise_for_status()
        answer = resp.json()['choices'][0]['message']['content']
        return jsonify({'response': answer})
    except requests.exceptions.HTTPError as e:
        # Return the full error response from OpenRouter for debugging
        return jsonify({'response': f"Error: {str(e)} | {resp.text}"})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 