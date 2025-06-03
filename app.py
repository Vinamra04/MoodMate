from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import random
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return "You said: " + str(user_text)

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Alternative model if needed
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['logged_in'] = True
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        password_hash = generate_password_hash(password)
        cursor = db.cursor()
        cursor.execute("INSERT INTO Users (username, email, password_hash, age, gender) VALUES (%s, %s, %s, %s, %s)", 
                       (username, email, password_hash, age, gender))
        db.commit()
        
        # Get the user_id of the newly created user
        cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        
        # Set session variables
        session['logged_in'] = True
        session['user_id'] = user_id
        session['username'] = username
        session['new_user'] = True
        
        # Redirect to welcome page instead of survey
        return redirect(url_for('welcome'))
    return render_template('signup.html')

@app.route('/welcome')
def welcome():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    # Only show welcome for new users
    if not session.get('new_user'):
        return redirect(url_for('dashboard'))
    
    return render_template('welcome.html')

@app.route('/survey')
def survey():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    # Only show survey for new users
    if not session.get('new_user'):
        return redirect(url_for('dashboard'))
    
    # Get survey questions
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Survey_Questions")
    questions = cursor.fetchall()
    
    return render_template('survey.html', questions=questions)

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    responses = json.loads(request.form['responses'])
    
    # Store responses in database
    cursor = db.cursor()
    for response in responses:
        cursor.execute("INSERT INTO User_Survey_Responses (user_id, question_id, answer) VALUES (%s, %s, %s)",
                      (user_id, response['question_id'], response['answer']))
    db.commit()
    
    # Determine mood based on responses
    mood_id = determine_mood_from_survey(user_id)
    
    # Store the determined mood in user history
    cursor.execute("INSERT INTO User_Mood_History (user_id, mood_id) VALUES (%s, %s)", (user_id, mood_id))
    db.commit()
    
    # Remove new_user flag
    session.pop('new_user', None)
    
    # Redirect to survey results
    return redirect(url_for('survey_results', mood_id=mood_id))

@app.route('/survey_results/<int:mood_id>')
def survey_results(mood_id):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    cursor = db.cursor(dictionary=True)
    
    # Get mood details
    cursor.execute("SELECT * FROM Moods WHERE mood_id = %s", (mood_id,))
    mood = cursor.fetchone()
    
    # Get recommendations for this mood
    cursor.execute("SELECT * FROM Recommendations WHERE mood_id = %s", (mood_id,))
    recommendations = cursor.fetchall()
    
    return render_template('survey_results.html', mood=mood, recommendations=recommendations)

def determine_mood_from_survey(user_id):
    cursor = db.cursor(dictionary=True)
    
    # Get user's responses
    cursor.execute("""
        SELECT sq.question_id, sq.positive_mood_id, sq.negative_mood_id, usr.answer
        FROM User_Survey_Responses usr
        JOIN Survey_Questions sq ON usr.question_id = sq.question_id
        WHERE usr.user_id = %s
        ORDER BY usr.recorded_at DESC
        LIMIT 5
    """, (user_id,))
    
    responses = cursor.fetchall()
    
    # Count votes for each mood
    mood_votes = {}
    for response in responses:
        mood_id = response['positive_mood_id'] if response['answer'] else response['negative_mood_id']
        if mood_id in mood_votes:
            mood_votes[mood_id] += 1
        else:
            mood_votes[mood_id] = 1
    
    # Find mood with most votes
    if not mood_votes:
        return 5  # Default to 'Relaxed' if no votes
    
    return max(mood_votes, key=mood_votes.get)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    # If new user, redirect to survey
    if session.get('new_user'):
        return redirect(url_for('survey'))
    
    # Get user's mood history
    user_id = session['user_id']
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.mood_name, umh.recorded_at
        FROM User_Mood_History umh
        JOIN Moods m ON umh.mood_id = m.mood_id
        WHERE umh.user_id = %s
        ORDER BY umh.recorded_at DESC
        LIMIT 10
    """, (user_id,))
    mood_history = cursor.fetchall()
    
    return render_template('dashboard.html', username=session['username'], mood_history=mood_history)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    if not session.get('logged_in'):
        return 'Unauthorized', 401
    user_id = session['user_id']
    mood_id = request.form['mood_id']
    cursor = db.cursor()
    cursor.execute("INSERT INTO User_Mood_History (user_id, mood_id) VALUES (%s, %s)", (user_id, mood_id))
    db.commit()

    cursor.execute("SELECT rec_text, rec_type FROM Recommendations WHERE mood_id = %s", (mood_id,))
    recommendations = cursor.fetchall()
    return jsonify(recommendations)

@app.route('/moodbot')
def moodbot():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    return render_template('moodbot.html', username=session['username'])

@app.route('/api/moodbot_chat', methods=['POST'])
def moodbot_chat():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id']
    user_message = request.json.get('message', '')
    
    print(f"Received chat message from user {user_id}: {user_message[:50]}...")
    
    # Get user's mood history
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.mood_name, umh.recorded_at
        FROM User_Mood_History umh
        JOIN Moods m ON umh.mood_id = m.mood_id
        WHERE umh.user_id = %s
        ORDER BY umh.recorded_at DESC
        LIMIT 10
    """, (user_id,))
    mood_history = cursor.fetchall()
    
    print(f"Retrieved {len(mood_history)} mood history entries for user {user_id}")
    
    # Format mood history for the AI
    mood_history_text = "User's recent mood history:\n"
    for i, mood in enumerate(mood_history):
        mood_date = mood['recorded_at'].strftime('%Y-%m-%d %H:%M')
        mood_history_text += f"{i+1}. {mood['mood_name']} - {mood_date}\n"
    
    # Get all possible recommendations for the user
    cursor.execute("""
        SELECT DISTINCT r.rec_text, r.rec_type, m.mood_name, m.mood_id, m.description
        FROM Recommendations r
        JOIN Moods m ON r.mood_id = m.mood_id
        ORDER BY m.mood_id ASC
    """)
    all_recommendations = cursor.fetchall()
    
    # Get user's most recent moods to prioritize recommendations
    recent_moods = []
    if mood_history:
        for mood in mood_history[:3]:  # Get three most recent moods
            recent_moods.append(mood['mood_name'])
    
    # Format recommendations for the AI, prioritizing those matching recent moods
    recommendations_text = "Available recommendations based on user's mood history:\n"
    
    # Add recommendations from recent moods first
    for mood_name in recent_moods:
        recommendations_text += f"\nRecommendations for recent mood '{mood_name}':\n"
        mood_recs = [r for r in all_recommendations if r['mood_name'] == mood_name]
        for i, rec in enumerate(mood_recs):
            recommendations_text += f"- {rec['rec_type']}: {rec['rec_text']}\n"
    
    # Add other recommendations
    recommendations_text += "\nOther available recommendations:\n"
    for rec in all_recommendations:
        if rec['mood_name'] not in recent_moods:
            recommendations_text += f"- {rec['rec_type']} for {rec['mood_name']}: {rec['rec_text']}\n"
    
    # Get user information for more personalized responses
    cursor.execute("SELECT username, age, gender FROM Users WHERE user_id = %s", (user_id,))
    user_info = cursor.fetchone()
    
    # Prepare prompt for Gemini
    prompt = f"""
    You are MoodBot, a supportive mental health assistant that helps users based on their mood history.
    
    USER INFORMATION:
    Username: {user_info['username']}
    Age: {user_info['age']}
    Gender: {user_info['gender']}
    
    USER'S MOOD HISTORY (from most recent to oldest):
    {mood_history_text}
    
    AVAILABLE RECOMMENDATIONS:
    {recommendations_text}
    
    The user says: "{user_message}"
    
    Your task:
    1. Analyze the user's mood history to identify patterns or trends
    2. Consider the user's current message to understand their immediate needs
    3. Provide a warm, empathetic response that feels like a caring friend rather than a clinical assistant
    4. Suggest 1-2 specific recommendations that would be most helpful based on their mood history and current message
    
    Guidelines:
    - Be conversational and supportive, validating their emotions
    - If they've had frequent negative moods like 'Sad', 'Anxious', or 'Stressed', acknowledge this pattern gently
    - If they show improvement, celebrate their progress
    - For recurring negative moods, consider suggesting professional support in addition to recommendations
    - Keep your response concise (under 150 words) and focused on making the user feel heard and supported
    
    Important: Your primary goal is to help improve the user's mental well-being based on their unique mood patterns.
    """
    
    print(f"Generated prompt of length: {len(prompt)} characters")
    
    # Fallback recommendations if API fails
    fallback_responses = {
        "recent_recommendations": [rec['rec_text'] for rec in all_recommendations[:5]],
        "generic_responses": [
            "I understand that you might be going through a challenging time. Based on your mood history, it seems like taking a short break for self-care could be beneficial.",
            "Thank you for sharing that with me. It's important to remember that your feelings are valid, and prioritizing your mental health is never selfish.",
            "I appreciate you opening up about this. Have you had a chance to try any of the activities suggested on your dashboard? They were selected specifically based on patterns in your mood.",
            "That's completely understandable. Many people in similar situations have found relief through simple mindfulness exercises. Would you like me to suggest some that might help?",
            "I'm here to support your journey toward better mental health. Remember that progress isn't always linear, and small steps can lead to meaningful improvements over time.",
            "Based on your mood patterns, I notice that you've experienced some ups and downs lately. This is a normal part of the human experience, and there are specific strategies that might help.",
            "It sounds like you're dealing with quite a lot right now. Sometimes, simply acknowledging our emotions can be an important first step toward managing them.",
            "Your mental wellbeing matters, and it's brave of you to seek support. Would you like me to suggest some resources that others have found helpful in similar situations?"
        ]
    }
    
    # Call Gemini API
    try:
        print("Calling Gemini API...")
        response = call_gemini_api(prompt)
        print(f"Received response from Gemini API ({len(response)} characters)")
        return jsonify({"response": response})
    except Exception as e:
        print(f"ERROR calling Gemini API: {str(e)}")
        
        # Generate fallback response
        import random
        fallback = random.choice(fallback_responses["generic_responses"])
        
        # Add a recommendation if available
        if fallback_responses["recent_recommendations"]:
            rec = random.choice(fallback_responses["recent_recommendations"])
            fallback += f"\n\nYou might try: {rec}"
        
        return jsonify({
            "response": fallback,
            "error": str(e),
            "fallback": True
        })

def call_gemini_api(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800
        }
    }
    
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    print(f"Calling Gemini API with URL: {url[:60]}...")  # Log URL (truncated for security)
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        print(f"Gemini API response status: {response.status_code}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 chars of response for debugging
        
        if response.status_code == 200:
            response_json = response.json()
            print("Received JSON response from Gemini API")
            
            if "candidates" in response_json and len(response_json["candidates"]) > 0:
                candidate = response_json["candidates"][0]
                if "content" in candidate:
                    content = candidate["content"]
                    if "parts" in content and len(content["parts"]) > 0:
                        for part in content["parts"]:
                            if "text" in part:
                                return part["text"]
                    else:
                        print("Error: No 'parts' in content")
                else:
                    print("Error: No 'content' in first candidate")
            else:
                print("Error: No 'candidates' in response or empty candidates list")
                
            # If we get here but have a proper JSON response, try to extract a meaningful message
            if "error" in response_json:
                error_info = response_json.get("error", {})
                error_message = error_info.get("message", "Unknown error")
                print(f"API returned error: {error_message}")
                raise Exception(f"API error: {error_message}")
                
            # If we get here, response structure is unexpected but we have a response to show
            print(f"Unexpected response structure: {json.dumps(response_json)[:200]}...")
            return "I received your message but couldn't generate a proper response. Please try asking in a different way."
        
        else:
            error_detail = response.text
            print(f"API Error {response.status_code}: {error_detail}")
            raise Exception(f"API returned status code {response.status_code}: {error_detail}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {str(e)}")
        raise Exception(f"Network error when calling Gemini API: {str(e)}")
    
    # If we get here, something went wrong
    raise Exception(f"Failed to get proper response from Gemini API: {response.text if 'response' in locals() else 'No response'}")

@app.route('/api/test_gemini', methods=['GET'])
def test_gemini():
    """Test endpoint to check if Gemini API is working"""
    try:
        test_prompt = "Respond with 'Hello, I am MoodBot and I am working correctly.' Nothing more, nothing less."
        response = call_gemini_api(test_prompt)
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "api_key": GEMINI_API_KEY[:5] + "..." + GEMINI_API_KEY[-5:], "api_url": GEMINI_API_URL})

if __name__ == '__main__':
    app.run(debug=True)
