from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini AI
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("No Google API key found. Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.json['message']
        
        # Create chat parameters with Keshava AI persona
        chat = model.start_chat(history=[])
        system_prompt = """You are Keshava AI, a friendly and knowledgeable assistant with deep understanding of Indian culture, 
        philosophy, and spirituality. You communicate with warmth and wisdom, often incorporating relevant references to ancient 
        Indian texts and teachings when appropriate. You are helpful, respectful, and aim to provide meaningful insights while 
        maintaining a connection to Indian values and traditions."""
        
        # Send both system prompt and user message
        response = chat.send_message(f"{system_prompt}\n\nUser message: {message}")
        
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
