from flask import Flask, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId
from bson.json_util import dumps
import bcrypt
import requests
import certifi
import os
import json
from groq import Groq

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
cors = CORS(app, origins='*')


# MongoDB connection
client = MongoClient('mongodb+srv://artsyoli11:Uh28xxh8yP6O4H6l@rideclaremontcluster.mwq7krb.mongodb.net/?retryWrites=true&w=majority&appName=rideClaremontCluster&ssl=true&tlsAllowInvalidCertificates=true')
db = client['rideclaremont']  
users_collection = db['users']
entries_collection = db['entries']

groqClient = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

conversation_history = []

# # Load Whisper ASR model
# asr_model = client.load_model("whisper-large-v3")

# # Load LLaMA 3.1 NLP model
# nlp_model = client.load_model("llama3-groq-70b-8192-tool-use-preview")



@app.route('/voice-assistant', methods=['POST'])
def voice_assistant():
    audio_file = request.files['audio']
    audio_data = audio_file.read()
    
    try:
        # Step 1: Transcribe the audio using the Whisper model
        translation = groqClient.audio.translations.create(
            file=(audio_file.filename, audio_data),
            model="whisper-large-v3",
            prompt="Specify context or spelling",  # Optional, customize as needed
            response_format="json",  # Optional
            temperature=0.0  # Optional
        )
        
        user_text = translation.text
        print("User Transcription:", user_text)

        conversation_history.append({"role": "user", "content": user_text})
        
        # Step 2: Generate a response using the LLaMA model
        chat_completion = groqClient.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            model="llama3-8b-8192",  # You can choose a different LLaMA model as needed
        )
        
        response_text = chat_completion.choices[0].message.content
        print("Generated Response:", response_text)
        
        conversation_history.append({"role": "assistant", "content": response_text})

        # Return the transcribed text and generated response
        #return jsonify({
            #"transcription": text,
            #"response": response_text
        #})
        return jsonify({"conversation_history": conversation_history})
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/clear-history', methods=['POST'])
def clear_history():
    global conversation_history
    conversation_history = []  # Clear the history
    return jsonify({"message": "Conversation history cleared."})

# Routes
@app.route('/getRequests', methods=['GET'])
def get_requests():
    try:
        # Query MongoDB for all entries (example)
        cursor = entries_collection.find({})
        entries_list = list(cursor)
        
        # Serialize MongoDB documents to JSON
        entries_json = json.dumps(entries_list, default=str)
        
        return entries_json, 200  # Return JSON response with status code 200 (OK)
    
    except Exception as e:
        print(f"Error retrieving requests: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500  # Return error response with status code 500

@app.route('/saveRequest', methods=['POST'])
def save_request():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        departure_date = data.get('departureDate')
        transportation = data.get('transportation')

        # Save request to MongoDB
        entry = {
            'name': name,
            'email': email,
            'phone': phone,
            'departureDate': departure_date,
            'transportation': transportation,
            # 'timestamp': datetime.datetime.utcnow()
        }
        result = entries_collection.insert_one(entry)
        
        return jsonify({'message': 'Request saved successfully!', 'entry_id': str(result.inserted_id)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes
@app.route('/')
def index():
    return "Welcome!"

@app.route('/register', methods=['POST'])
def register():
    # Retrieve user data from request
    username = request.json['username']
    password = request.json['password']

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user into database
    users_collection.insert_one({'username': username, 'password': hashed_password})
    
    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    # Retrieve user data from request
    username = request.json['username']
    password = request.json['password']

    # Find user in the database
    user = users_collection.find_one({'username': username})

    if user:
        # Check if password matches
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # Store user data in session
            session['username'] = username
            return jsonify({'message': 'Login successful!'})
    
    return jsonify({'message': 'Invalid username/password combination'}), 401

@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'username' in session:
        return f"Welcome {session['username']}!"
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove user data from session
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully!'})


def get_ai_snippets_for_query(query):
    headers = {"X-API-Key": "a504b5cb-9ed3-41c8-a466-aa8992c1e6d3<__>1PVqZSETU8N2v5f4AQnANCQx"}
    params = {"query": query}
    return requests.get(
        f"https://api.ydc-index.io/search",
        params=params,
        headers=headers,
    ).json()
    
results = get_ai_snippets_for_query("reasons to smile")
print(results)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    bot_response = get_ai_snippets_for_query(user_message)
    return jsonify(bot_response)

if __name__=="__main__":
    app.run(debug=True, port=8000)