# MoodMate: AI-powered Mental Health Mood Tracker

## Overview
MoodMate is a modern web platform designed to help users understand, track, and improve their mental health. Leveraging AI, MoodMate provides personalized mood tracking, actionable recommendations, and supportive conversations through a chatbot. The platform offers a safe, private, and user-friendly environment for emotional well-being.

---

## Features
- **User Authentication**: Secure sign up, login, and session management.
- **Onboarding Survey**: Personalized mood assessment for new users.
- **Mood Tracking**: Log and visualize your moods over time.
- **Personalized Recommendations**: Get actionable suggestions (music, exercise, meditation, etc.) based on your mood.
- **AI Chatbot (MoodBot)**: Chat with an empathetic AI for support and advice, powered by Google Gemini.
- **Dashboard**: Central hub for mood history, recommendations, and quick actions.
- **Responsive UI**: Modern, mobile-friendly design with smooth animations.




## Screenshots
<!-- Add screenshots/gifs of your app here -->
---
![1](https://github.com/user-attachments/assets/d3d67a07-050d-4622-9d0e-8d56a2c875d8)
![3](https://github.com/user-attachments/assets/3584324d-7cc0-48fe-abfd-242e891a3552)
![Screenshot 2025-06-03 172250](https://github.com/user-attachments/assets/a598fa4b-5e04-40b7-860d-b681cc6d71be)
![Screenshot 2025-06-03 172309](https://github.com/user-attachments/assets/409c1b93-f187-4d48-8eb8-2a6d6bf6e570)
![Screenshot 2025-06-03 172336](https://github.com/user-attachments/assets/534f934d-89a2-48bb-ba33-0860aa51aa2f)
![Screenshot 2025-06-03 172400](https://github.com/user-attachments/assets/0460b7ae-f3e9-4181-9c6a-c422e04a18a1)

---

## Technologies Used

### Backend
- **Python (Flask)**: Web framework for routing and API endpoints
- **MySQL**: Relational database for user data, moods, and recommendations
- **Werkzeug**: Secure password hashing
- **Requests**: For API calls (e.g., Gemini)
- **python-dotenv**: Securely manage environment variables

### Frontend
- **HTML/CSS (Jinja2 Templates)**: Dynamic page rendering
- **Tailwind CSS**: Utility-first CSS framework for modern design
- **Custom CSS & JS**: For unique UI effects and interactivity

### AI Integration
- **Google Gemini API**: Empathetic, context-aware chatbot responses

### Build Tools
- **PostCSS & Autoprefixer**: CSS processing
- **Tailwind CLI**: CSS build pipeline

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Vinamra04/MoodMate.git
cd MoodMate
```

### 2. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (for Tailwind CSS)
npm install
```

### 3. Set Up Environment Variables
- Copy `.env.example` to `.env`:
  ```bash
  cp .env.example .env
  ```
- Fill in your own values for the API keys and database credentials in `.env`.

### 4. Set Up the Database
- Import the provided `db.sql` file into your MySQL server:
  ```bash
  mysql -u youruser -p yourdatabase < db.sql
  ```

### 5. Build Tailwind CSS
```bash
npm run build
```

### 6. Run the Application
```bash
python app.py
```

The app will be available at [http://localhost:5000](http://localhost:5000)

---

## Environment Variables
The following variables must be set in your `.env` file:

| Variable           | Description                        |
|--------------------|------------------------------------|
| GEMINI_API_KEY     | Google Gemini API key              |
| FLASK_SECRET_KEY   | Flask session secret key           |
| DB_HOST            | MySQL database host                |
| DB_USER            | MySQL database user                |
| DB_PASSWORD        | MySQL database password            |
| DB_NAME            | MySQL database name                |

---

## Usage
- **Sign up** and complete the onboarding survey.
- **Log your mood** daily and receive personalized recommendations.
- **Chat with MoodBot** for support and advice.
- **Track your mood history** and reflect on emotional trends.

---

## Credits
- **Aaditya Tiwary** – Backend, core logic ([GitHub](https://github.com/AadityaTiwary1))
- **Vinamra Srivastava** – Frontend, UI/UX, AI integration, immersive user experience ([GitHub](https://github.com/Vinamra04))

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Contact
For questions or support, please contact:
- [aadityatiwary79@gmail.com](mailto:aadityatiwary79@gmail.com)
- [vinamra.srivastava18@gmail.com](mailto:vinamra.srivastava18@gmail.com) 
