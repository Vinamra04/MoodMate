CREATE TABLE Users ( user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) NOT NULL UNIQUE, email VARCHAR(100) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, age INT CHECK (age >= 13), gender ENUM('Male', 'Female', 'Other'), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

CREATE TABLE Moods ( mood_id INT AUTO_INCREMENT PRIMARY KEY, mood_name VARCHAR(50) NOT NULL UNIQUE, description TEXT );

CREATE TABLE Recommendations ( rec_id INT AUTO_INCREMENT PRIMARY KEY, mood_id INT NOT NULL, rec_text TEXT NOT NULL, rec_type ENUM('Music', 'Exercise', 'Meditation', 'Therapy', 'Diet', 'Reading'), FOREIGN KEY (mood_id) REFERENCES Moods(mood_id) ON DELETE CASCADE );

CREATE TABLE User_Mood_History ( history_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, mood_id INT NOT NULL, recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE, FOREIGN KEY (mood_id) REFERENCES Moods(mood_id) ON DELETE CASCADE );

CREATE TABLE Survey_Questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    positive_mood_id INT,
    negative_mood_id INT,
    FOREIGN KEY (positive_mood_id) REFERENCES Moods(mood_id) ON DELETE SET NULL,
    FOREIGN KEY (negative_mood_id) REFERENCES Moods(mood_id) ON DELETE SET NULL
);

CREATE TABLE User_Survey_Responses (
    response_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    answer BOOLEAN NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES Survey_Questions(question_id) ON DELETE CASCADE
);

INSERT INTO Moods (mood_name, description) VALUES
('Happy', 'Feeling joyful and content'),
('Sad', 'Feeling down or upset'),
('Anxious', 'Feeling worried or uneasy'),
('Angry', 'Feeling mad or frustrated'),
('Relaxed', 'Feeling calm and at ease'),
('Stressed', 'Feeling overwhelmed or tense'),
('Motivated', 'Feeling driven and focused'),
('Lonely', 'Feeling isolated or alone'),
('Excited', 'Feeling thrilled or enthusiastic'),
('Bored', 'Feeling uninterested or restless');

INSERT INTO Recommendations (mood_id, rec_text, rec_type) VALUES
-- Happy
(1, 'Listen to upbeat pop music', 'Music'),
(1, 'Go for a dance class', 'Exercise'),
(1, 'Practice gratitude meditation', 'Meditation'),
(1, 'Celebrate with friends', 'Therapy'),
(1, 'Try a smoothie bowl', 'Diet'),
(1, 'Read a motivational book', 'Reading'),

-- Sad
(2, 'Listen to soothing piano music', 'Music'),
(2, 'Take a nature walk', 'Exercise'),
(2, 'Breathe deeply for 10 minutes', 'Meditation'),
(2, 'Talk to a counselor', 'Therapy'),
(2, 'Eat a warm bowl of soup', 'Diet'),
(2, 'Read a comforting novel', 'Reading'),

-- Anxious
(3, 'Listen to calming ambient music', 'Music'),
(3, 'Try yoga for anxiety relief', 'Exercise'),
(3, 'Use guided breathing exercises', 'Meditation'),
(3, 'Write down your worries', 'Therapy'),
(3, 'Drink herbal tea', 'Diet'),
(3, 'Read a book on mindfulness', 'Reading'),

-- Angry
(4, 'Listen to rock or metal music', 'Music'),
(4, 'Punch a boxing bag or run', 'Exercise'),
(4, 'Count to ten and breathe', 'Meditation'),
(4, 'Talk to a therapist', 'Therapy'),
(4, 'Eat dark chocolate', 'Diet'),
(4, 'Read about anger management', 'Reading'),

-- Relaxed
(5, 'Enjoy jazz or classical music', 'Music'),
(5, 'Stretch or do light yoga', 'Exercise'),
(5, 'Practice body scan meditation', 'Meditation'),
(5, 'Connect with a friend', 'Therapy'),
(5, 'Have a green smoothie', 'Diet'),
(5, 'Read a lighthearted story', 'Reading'),

-- Stressed
(6, 'Listen to lo-fi beats', 'Music'),
(6, 'Go for a brisk walk', 'Exercise'),
(6, 'Use a meditation app', 'Meditation'),
(6, 'Speak with a therapist', 'Therapy'),
(6, 'Eat omega-3 rich food', 'Diet'),
(6, 'Read about stress management', 'Reading'),

-- Motivated
(7, 'Listen to motivational tracks', 'Music'),
(7, 'Hit the gym', 'Exercise'),
(7, 'Visualize your goals', 'Meditation'),
(7, 'Discuss ideas with a mentor', 'Therapy'),
(7, 'Eat protein-packed meals', 'Diet'),
(7, 'Read a success story', 'Reading'),

-- Lonely
(8, 'Listen to acoustic music', 'Music'),
(8, 'Join a local sports club', 'Exercise'),
(8, 'Practice loving-kindness meditation', 'Meditation'),
(8, 'Reach out to a friend', 'Therapy'),
(8, 'Share a meal with someone', 'Diet'),
(8, 'Read an uplifting novel', 'Reading'),

-- Excited
(9, 'Play energetic party music', 'Music'),
(9, 'Go for a hike or adventure sport', 'Exercise'),
(9, 'Do a quick breathing session', 'Meditation'),
(9, 'Share your excitement with someone', 'Therapy'),
(9, 'Try a new exotic recipe', 'Diet'),
(9, 'Read a thrilling novel', 'Reading'),

-- Bored
(10, 'Listen to a new music genre', 'Music'),
(10, 'Try a new workout routine', 'Exercise'),
(10, 'Do a creative visualization meditation', 'Meditation'),
(10, 'Talk to someone interesting', 'Therapy'),
(10, 'Cook something you\'ve never tried', 'Diet'),
(10, 'Read a mystery book', 'Reading');

INSERT INTO Survey_Questions (question_text, positive_mood_id, negative_mood_id) VALUES
('Do you feel energetic today?', 7, 2),
('Have you been feeling calm and at peace recently?', 5, 3),
('Do you feel excited about your future?', 9, 8),
('Have you been feeling irritable or easily annoyed?', 4, 1),
('Do you feel overwhelmed by your responsibilities?', 6, 5);