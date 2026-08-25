# 🤖 AI-Based Smart Attendance System

An AI-powered attendance management system combining **Face Recognition** and **Voice Recognition** with **Streamlit** and **Supabase**.

## ✨ Features

### 👨‍🏫 Teacher
- Teacher registration and login
- Create subjects and generate join codes
- View enrolled students
- Take attendance using face or voice recognition
- Review attendance before saving
- View attendance history and statistics

### 👨‍🎓 Student
- Student registration and login
- Join subjects using a unique subject code
- Register face and voice profiles
- View enrolled subjects and attendance

### 🤖 AI
- dlib face detection
- Pretrained face embeddings
- SVC-based face classification
- Librosa audio preprocessing
- Resemblyzer speaker embeddings
- Cosine-similarity voice matching

## 🧠 AI Pipeline

```text
FACE
Camera → dlib detector → facial landmarks → face embedding → SVC / similarity → Student → Attendance

VOICE
Audio → librosa → preprocess_wav → Resemblyzer → speaker embedding → cosine similarity → Student → Attendance
```

## 🏗️ Architecture

```text
Streamlit UI
   ├── Face Pipeline → dlib → Face Embedding → SVC / Similarity
   └── Voice Pipeline → Librosa → Resemblyzer → Cosine Similarity
                         ↓
                     Supabase
                         ↓
                Attendance Records
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Streamlit | Web application UI |
| Supabase | Database and backend services |
| PostgreSQL | Relational data storage |
| dlib | Face detection and recognition pipeline |
| scikit-learn | SVC classifier |
| NumPy | Numerical processing |
| Pandas | Data processing and reporting |
| Librosa | Audio processing |
| Resemblyzer | Voice embeddings |

## 📁 Project Structure

```text
AI-Attendance-System/
├── app.py
├── src/
│   ├── components/
│   ├── database/
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   ├── pages/
│   └── utils/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Attendance-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

## 🔐 Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

> ⚠️ Never commit your `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
venv/
__pycache__/
```

## 🗄️ Database

Main Supabase tables:

```text
students
teachers
subjects
subject_students
attendance_logs
```

### Database relationship

```text
Teachers
   ↓
Subjects
   ↓
subject_students
   ↓
Students
   ↓
attendance_logs
```

## 📷 Face Recognition Workflow

```text
Camera Image
     ↓
dlib Face Detector
     ↓
Face Landmark Detection
     ↓
Face Embedding
     ↓
SVC Classifier
     ↓
Student Identification
     ↓
Similarity Verification
     ↓
Attendance
```

### Face embedding

The system converts a detected face into a numerical embedding. These embeddings can be stored in Supabase and used during recognition.

### SVC classification

```python
from sklearn.svm import SVC

clf = SVC(
    kernel="linear",
    probability=True,
    class_weight="balanced"
)

clf.fit(X, y)
```

## 🎙️ Voice Recognition Workflow

```text
Audio Recording
      ↓
Librosa
      ↓
Audio Preprocessing
      ↓
Resemblyzer
      ↓
Voice Embedding
      ↓
Cosine Similarity
      ↓
Threshold Check
      ↓
Student Identification
      ↓
Attendance
```

### Voice embedding

```python
audio, sr = librosa.load(
    io.BytesIO(audio_bytes),
    sr=16000
)

wav = preprocess_wav(audio)

embedding = encoder.embed_utterance(wav)
```

### Voice matching

Cosine similarity compares a newly recorded voice embedding with the stored student voice embeddings.

## 👨‍🏫 Attendance Workflow

```text
Teacher Login
      ↓
Select Subject
      ↓
Choose Attendance Method
      ↓
Face / Voice Recognition
      ↓
AI Identification
      ↓
Review Attendance
      ↓
Confirm & Save
      ↓
Supabase
```

## 👨‍🎓 Student Workflow

```text
Student Login
      ↓
Join Subject
      ↓
Enter Subject Code
      ↓
Enroll
      ↓
Register Face
      ↓
Register Voice
      ↓
View Attendance
```

## 📊 Attendance Reporting

Attendance sessions can be grouped and displayed as:

```text
Time              Subject       Attendance
────────────────────────────────────────────
01:30 PM          DBMS          ✅ 40 / 45 Students
11:00 AM          Python        ✅ 42 / 45 Students
```

Attendance percentage:

```text
Present Students
──────────────── × 100
Total Students
```

## 🔒 Security

- Role-based student/teacher access
- Supabase database
- Environment variables for secrets
- Student-subject enrollment validation
- Stored face and voice embeddings
- Attendance confirmation before saving

## ⚠️ Recognition Considerations

### Face Recognition
Accuracy can be affected by:
- Poor lighting
- Camera quality
- Face angle
- Occlusion
- Multiple faces
- Incorrect face profiles

### Voice Recognition
Accuracy can be affected by:
- Background noise
- Microphone quality
- Multiple speakers
- Short recordings
- Similar voices

For better recognition, profiles should be registered in good lighting and low-noise environments.

## 🚀 Future Improvements

- [ ] Real-time attendance dashboard
- [ ] Attendance notifications
- [ ] Anti-spoofing
- [ ] Face liveness detection
- [ ] Noise reduction for voice recognition
- [ ] Excel/PDF attendance export
- [ ] Attendance analytics and charts
- [ ] Email notifications
- [ ] Mobile responsive interface
- [ ] Admin dashboard

## 👨‍💻 Author

**Parth Borkar**

AI-Based Smart Attendance System

## 📄 License

This project is developed for educational and academic purposes.
