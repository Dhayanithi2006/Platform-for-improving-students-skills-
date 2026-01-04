"""
SkillTwin Backend - Clean Version
Proactive Learning & Evaluation Platform
"""
import os
import sys
import uuid
import json
from datetime import datetime
from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import tempfile
from werkzeug.datastructures.file_storage import FileStorage
from typing import Any, Literal

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all origins in development
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Origin", "X-Requested-With"],
        "supports_credentials": True
    }
})

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/skilltwin.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'skilltwin-dev-secret-2024')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize database
db = SQLAlchemy(app)

# Allowed file extensions
ALLOWED_EXTENSIONS: set[str] = {'pdf', 'txt'}

def allowed_file(filename) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ DATABASE MODELS ============
class Student(db.Model):
    __tablename__: str = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False, default='demo123')
    name = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(50))
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    enrollment_date = db.Column(db.Date)
    goals = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    performances = db.relationship('StudentPerformance', backref='student', lazy=True, cascade='all, delete-orphan')
    tests = db.relationship('MockTest', backref='student', lazy=True, cascade='all, delete-orphan')
    activities = db.relationship('StudentActivity', backref='student', lazy=True, cascade='all, delete-orphan')
    paper_analyses = db.relationship('PaperAnalysis', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'class_level': self.class_level,
            'student_id': self.student_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'goals': self.goals,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Topic(db.Model):
    __tablename__: str = 'topics'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(100), nullable=False)
    topic_name = db.Column(db.String(200), nullable=False)
    difficulty_level = db.Column(db.Integer, default=2)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'topic_name': self.topic_name,
            'difficulty_level': self.difficulty_level,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StudentPerformance(db.Model):
    __tablename__: str = 'student_performance'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), db.ForeignKey('users.student_id', ondelete='CASCADE'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    mastery_score = db.Column(db.Float, default=0.0)
    questions_attempted = db.Column(db.Integer, default=0)
    questions_correct = db.Column(db.Integer, default=0)
    total_time_spent = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    topic = db.relationship('Topic', lazy='joined')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'topic': self.topic.to_dict() if self.topic else None,
            'mastery_score': self.mastery_score,
            'questions_attempted': self.questions_attempted,
            'questions_correct': self.questions_correct,
            'accuracy': round((self.questions_correct / self.questions_attempted * 100), 2) if self.questions_attempted > 0 else 0,
            'total_time_spent': self.total_time_spent,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class MockTest(db.Model):
    __tablename__: str = 'mock_tests'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(50), db.ForeignKey('users.student_id', ondelete='CASCADE'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    test_type = db.Column(db.String(50), default='adaptive')
    questions = db.Column(db.JSON, default=list)
    answers = db.Column(db.JSON, default=list)
    scores = db.Column(db.JSON, default=dict)
    ability_estimate = db.Column(db.Float, default=0.5)
    total_score = db.Column(db.Float)
    time_taken = db.Column(db.Integer)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'test_type': self.test_type,
            'questions': self.questions,
            'answers': self.answers,
            'scores': self.scores,
            'ability_estimate': self.ability_estimate,
            'total_score': self.total_score,
            'time_taken': self.time_taken,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration': (self.completed_at - self.started_at).total_seconds() if self.completed_at and self.started_at else None
        }

class Question(db.Model):
    __tablename__: str = 'questions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)
    correct_answer = db.Column(db.String(10), nullable=False)
    explanation = db.Column(db.Text)
    marks = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'topic': self.topic,
            'difficulty': self.difficulty,
            'question_text': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'marks': self.marks,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StudentActivity(db.Model):
    __tablename__: str = 'student_activities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), db.ForeignKey('users.student_id', ondelete='CASCADE'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    activity_metadata = db.Column(db.JSON, default=dict)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'activity_metadata': self.activity_metadata,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PaperAnalysis(db.Model):
    __tablename__: str = 'paper_analyses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(50), db.ForeignKey('users.student_id', ondelete='CASCADE'))
    filename = db.Column(db.String(255))
    original_filename = db.Column(db.String(255))
    subject = db.Column(db.String(100))
    analysis_data = db.Column(db.JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'subject': self.subject,
            'analysis_data': self.analysis_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ============ HELPER FUNCTIONS ============
def seed_sample_data() -> bool:
    """Seed database with sample data"""
    try:
        # Check if demo student already exists
        demo_student = Student.query.filter_by(email="demo@skilltwin.com").first()
        if demo_student:
            print("Database already seeded with demo data.")
            return True
        
        print("Seeding database with sample data...")
        
        # Create demo student
        demo_student = Student(
            email="demo@skilltwin.com",
            name="Demo Student",
            password="demo123",
            class_level="10th Grade",
            student_id="student_001",
            enrollment_date=datetime(2024, 1, 15).date(),
            goals="Master all subjects and achieve excellent grades"
        )
        db.session.add(demo_student)
        db.session.flush()
        
        # Create sample topics
        topics: list[Topic] = [
            Topic(subject="Physics", topic_name="Thermodynamics", difficulty_level=3),
            Topic(subject="Physics", topic_name="Optics", difficulty_level=2),
            Topic(subject="Physics", topic_name="Mechanics", difficulty_level=2),
            Topic(subject="Mathematics", topic_name="Calculus", difficulty_level=4),
            Topic(subject="Mathematics", topic_name="Algebra", difficulty_level=2),
            Topic(subject="Chemistry", topic_name="Organic Chemistry", difficulty_level=3),
        ]
        
        for topic in topics:
            db.session.add(topic)
        db.session.flush()
        
        # Create performance data
        performances: list[StudentPerformance] = [
            StudentPerformance(
                student_id=demo_student.student_id,
                topic_id=topics[0].id,  # Thermodynamics
                mastery_score=65,
                questions_attempted=50,
                questions_correct=32,
                total_time_spent=120
            ),
            StudentPerformance(
                student_id=demo_student.student_id,
                topic_id=topics[1].id,  # Optics
                mastery_score=45,
                questions_attempted=40,
                questions_correct=18,
                total_time_spent=90
            ),
            StudentPerformance(
                student_id=demo_student.student_id,
                topic_id=topics[2].id,  # Mechanics
                mastery_score=80,
                questions_attempted=60,
                questions_correct=48,
                total_time_spent=180
            ),
            StudentPerformance(
                student_id=demo_student.student_id,
                topic_id=topics[3].id,  # Calculus
                mastery_score=70,
                questions_attempted=55,
                questions_correct=38,
                total_time_spent=150
            )
        ]
        
        for perf in performances:
            db.session.add(perf)
        
        # Create sample questions
        questions: list[Question] = [
            Question(
                id="Q001",
                subject="Physics",
                topic="Thermodynamics",
                difficulty="medium",
                question_text="Calculate the work done in an isothermal expansion of an ideal gas from volume V1 to V2.",
                options=["nRT ln(V2/V1)", "PΔV", "nCvΔT", "Zero"],
                correct_answer="A",
                explanation="For isothermal expansion of ideal gas, work done = nRT ln(V2/V1)",
                marks=3
            ),
            Question(
                id="Q002",
                subject="Physics",
                topic="Optics",
                difficulty="easy",
                question_text="What is the formula for focal length of a spherical mirror?",
                options=["1/f = 1/u + 1/v", "f = R/2", "f = 2R", "f = R"],
                correct_answer="B",
                explanation="For spherical mirrors, focal length f = R/2 where R is radius of curvature",
                marks=2
            ),
            Question(
                id="Q003",
                subject="Mathematics",
                topic="Calculus",
                difficulty="hard",
                question_text="What is the derivative of sin(2x)?",
                options=["2cos(2x)", "cos(2x)", "2sin(2x)", "-2cos(2x)"],
                correct_answer="A",
                explanation="Using chain rule: d/dx[sin(2x)] = cos(2x) * 2 = 2cos(2x)",
                marks=4
            ),
            Question(
                id="Q004",
                subject="Chemistry",
                topic="Organic Chemistry",
                difficulty="medium",
                question_text="What is the molecular formula of methane?",
                options=["CH4", "C2H6", "CH3", "C2H4"],
                correct_answer="A",
                explanation="Methane is the simplest alkane with one carbon and four hydrogen atoms",
                marks=2
            ),
            Question(
                id="Q005",
                subject="Mathematics",
                topic="Algebra",
                difficulty="easy",
                question_text="Solve for x: 2x + 5 = 15",
                options=["x = 5", "x = 10", "x = 7.5", "x = 3"],
                correct_answer="A",
                explanation="2x = 15 - 5 = 10, so x = 5",
                marks=1
            )
        ]
        
        for question in questions:
            db.session.add(question)
        
        # Create sample activities
        activities: list[StudentActivity] = [
            StudentActivity(
                student_id=demo_student.student_id,
                activity_type="login",
                description="Student logged into the system",
                activity_metadata={"ip": "127.0.0.1"},
                duration=0,
                created_at=datetime.utcnow()
            ),
            StudentActivity(
                student_id=demo_student.student_id,
                activity_type="test_completed",
                description="Completed physics mock test",
                activity_metadata={"subject": "Physics", "score": 75},
                duration=1800,
                created_at=datetime.utcnow()
            )
        ]
        
        for activity in activities:
            db.session.add(activity)
        
        db.session.commit()
        print("Sample data seeded successfully!")
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============ SIMPLE ML ENGINE ============
class SimplePredictor:
    """Simple performance predictor without numpy/scikit-learn"""
    
    def __init__(self) -> None:
        self.base_score = 70
    
    def predict(self, student_data: dict) -> dict:
        """Predict student performance"""
        engagement = student_data.get('engagement_score', 0.5)
        avg_score = student_data.get('average_quiz_score', 70)
        mastery = student_data.get('average_mastery', 60)
        
        # Simple weighted prediction
        predicted_score = (avg_score * 0.4 + mastery * 0.4 + engagement * 20)
        predicted_score = min(100, max(0, predicted_score))
        
        return {
            'predicted_score': round(predicted_score, 1),
            'confidence': 0.75,
            'recommendations': self.generate_recommendations(predicted_score)
        }
    
    def generate_recommendations(self, score: float) -> list[str]:
        """Generate study recommendations"""
        if score >= 80:
            return ["Focus on advanced topics", "Practice challenging problems"]
        elif score >= 60:
            return ["Review weak areas", "Practice regularly"]
        else:
            return ["Focus on basics", "Get additional help"]
    
    def assess_risk(self, predicted_score: float) -> str:
        """Assess academic risk level"""
        if predicted_score >= 80:
            return 'low'
        elif predicted_score >= 60:
            return 'medium'
        else:
            return 'high'

class SimpleAdaptiveEngine:
    """Simple adaptive test engine"""
    
    def __init__(self) -> None:
        self.ability_estimate = 0.5
        self.consecutive_correct = 0
        self.consecutive_wrong = 0
    
    def get_next_difficulty(self, previous_correct, response_time=30) -> str:
        """Determine next question difficulty"""
        learning_rate = 0.15
        
        if previous_correct:
            self.ability_estimate: float = min(1, self.ability_estimate + learning_rate)
            self.consecutive_correct += 1
            self.consecutive_wrong = 0
        else:
            self.ability_estimate: float = max(0, self.ability_estimate - learning_rate)
            self.consecutive_wrong += 1
            self.consecutive_correct = 0
        
        # Adjust for streaks
        if self.consecutive_correct >= 3:
            self.ability_estimate: float = min(1, self.ability_estimate + 0.1)
        elif self.consecutive_wrong >= 3:
            self.ability_estimate: float = max(0, self.ability_estimate - 0.1)
        
        # Select difficulty
        if self.ability_estimate < 0.3:
            return 'easy'
        elif self.ability_estimate < 0.7:
            return 'medium'
        else:
            return 'hard'
    
    def reset(self) -> None:
        """Reset engine state"""
        self.ability_estimate = 0.5
        self.consecutive_correct = 0
        self.consecutive_wrong = 0

# Initialize engines
predictor = SimplePredictor()
adaptive_engine = SimpleAdaptiveEngine()

# ============ AUTHENTICATION ROUTES ============
@app.route('/api/auth/login', methods=['POST'])
def login() -> tuple[Response, Literal[400]] | Response | tuple[Response, Literal[500]]:
    """User login endpoint"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        # For demo, create user if doesn't exist
        student = Student.query.filter_by(email=email).first()
        
        if not student:
            # Create new user for demo
            student = Student(
                email=email,
                name=data.get('name', email.split('@')[0].title()),
                password=data.get('password', 'demo123'),
                class_level=data.get('class_level', '10th Grade'),
                student_id=f"student_{uuid.uuid4().hex[:8]}"
            )
            db.session.add(student)
        else:
            # Update last login
            student.last_login = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': student.to_dict(),
            'token': str(uuid.uuid4()),
            'message': 'Login successful'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout() -> Response:
    """User logout endpoint"""
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# ============ STUDENT DASHBOARD ROUTES ============
@app.route('/api/dashboard/<student_id>', methods=['GET'])
def get_dashboard(student_id) -> tuple[Response, Literal[404]] | Response | tuple[Response, Literal[500]]:
    """Get comprehensive dashboard data"""
    try:
        # Try to find student by student_id first, then by id
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            # Try by id (UUID case)
            student = Student.query.get(student_id)
        
        if not student:
            # Fallback to demo student
            student = Student.query.filter_by(email="demo@skilltwin.com").first()
            if not student:
                return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        # Use the student's student_id for all queries
        actual_student_id = student.student_id
        
        # Get performance data
        performances = StudentPerformance.query.filter_by(student_id=actual_student_id).all()
        
        # Calculate overall stats
        if performances:
            overall_mastery: float = sum(p.mastery_score for p in performances) / len(performances)
            total_questions: int = sum(p.questions_attempted for p in performances)
            correct_answers: int = sum(p.questions_correct for p in performances)
            total_time: float = sum(p.total_time_spent for p in performances) / 60
        else:
            overall_mastery = 0
            total_questions = 0
            correct_answers = 0
            total_time = 0
        
        # Get recent activities
        recent_activities = StudentActivity.query.filter_by(student_id=actual_student_id)\
            .order_by(StudentActivity.created_at.desc())\
            .limit(5).all()
        
        # Get recent tests
        recent_tests = MockTest.query.filter_by(student_id=actual_student_id)\
            .order_by(MockTest.started_at.desc())\
            .limit(3).all()
        
        # Get weak topics
        weak_topics: list[Any] = sorted(performances, key=lambda x: x.mastery_score)[:3] if performances else []
        
        return jsonify({
            'success': True,
            'dashboard': {
                'student': student.to_dict(),
                'stats': {
                    'overall_mastery': round(overall_mastery, 1),
                    'questions_attempted': total_questions,
                    'accuracy_rate': round(correct_answers/total_questions*100, 1) if total_questions > 0 else 0,
                    'total_study_time': round(total_time, 1),
                    'streak_days': 7,
                    'weekly_goal_progress': 65
                },
                'upcoming_exams': [
                    {
                        'subject': 'Physics',
                        'date': '2024-06-15',
                        'topic': 'Unit 3: Thermodynamics',
                        'preparedness': 65,
                        'days_left': 5
                    },
                    {
                        'subject': 'Mathematics',
                        'date': '2024-06-20',
                        'topic': 'Calculus Integration',
                        'preparedness': 80,
                        'days_left': 10
                    },
                    {
                        'subject': 'Chemistry',
                        'date': '2024-06-25',
                        'topic': 'Organic Chemistry',
                        'preparedness': 45,
                        'days_left': 15
                    }
                ],
                'recent_activities': [act.to_dict() for act in recent_activities],
                'recent_tests': [test.to_dict() for test in recent_tests],
                'weak_topics': [{
                    'topic': p.topic.topic_name if p.topic else 'Unknown',
                    'subject': p.topic.subject if p.topic else 'General',
                    'mastery': p.mastery_score,
                    'accuracy': round((p.questions_correct / p.questions_attempted * 100), 2) if p.questions_attempted > 0 else 0
                } for p in weak_topics],
                'quick_actions': [
                    {'action': 'Start Mock Test', 'icon': 'test', 'route': '/test'},
                    {'action': 'Analyze Paper', 'icon': 'paper', 'route': '/paper-analysis'},
                    {'action': 'View Analytics', 'icon': 'chart', 'route': '/analytics'},
                    {'action': 'Daily Quiz', 'icon': 'quiz', 'route': '/quiz'},
                    {'action': 'Study Plan', 'icon': 'plan', 'route': '/study-plan'},
                    {'action': 'Resources', 'icon': 'resources', 'route': '/resources'}
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ PERFORMANCE PREDICTION ROUTES ============
@app.route('/api/performance/predict/<student_id>', methods=['GET'])
def predict_performance(student_id) -> tuple[Response, Literal[404]] | Response | tuple[Response, Literal[500]]:
    """Get performance prediction for student"""
    try:
        # Try to find student by student_id first, then by id
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            # Try by id (UUID case)
            student = Student.query.get(student_id)
        
        if not student:
            # Fallback to demo student
            student = Student.query.filter_by(email="demo@skilltwin.com").first()
            if not student:
                return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        # Use the student's student_id for all queries
        actual_student_id = student.student_id
        
        # Get student performance data
        performances = StudentPerformance.query.filter_by(student_id=actual_student_id).all()
        
        # Prepare data for prediction
        student_data = {
            'engagement_score': 0.7,
            'average_quiz_score': 75,
            'average_mastery': sum(p.mastery_score for p in performances) / len(performances) if performances else 60,
            'consistency_score': 0.8,
            'total_study_time': sum(p.total_time_spent for p in performances) / 60 if performances else 10
        }
        
        # Get prediction
        prediction = predictor.predict(student_data)
        
        # Get weak topics
        weak_topics: list[Any] = sorted(performances, key=lambda x: x.mastery_score)[:3] if performances else []
        
        # Generate recommendations
        recommendations: list[str] = [
            f"Focus on {weak_topics[0].topic.topic_name if weak_topics else 'key topics'} for 30 minutes daily",
            "Take adaptive mock test on weak topics",
            "Review summarized notes for difficult concepts",
            "Watch concept explanation videos",
            "Solve previous year question papers",
            "Join study group discussions"
        ]
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'risk_level': predictor.assess_risk(prediction['predicted_score']),
            'weak_topics': [{
                'topic': p.topic.topic_name if p.topic else 'Unknown',
                'mastery': p.mastery_score,
                'subject': p.topic.subject if p.topic else 'General',
                'questions_attempted': p.questions_attempted,
                'accuracy': round((p.questions_correct / p.questions_attempted * 100), 2) if p.questions_attempted > 0 else 0
            } for p in weak_topics],
            'recommendations': recommendations[:3],
            'improvement_tips': [
                'Study during peak concentration hours',
                'Use spaced repetition for better retention',
                'Practice with time limits',
                'Review mistakes regularly'
            ]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ HEALTH CHECK ============
@app.route('/api/health', methods=['GET'])
def health_check() -> Response:
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

# ============ MAIN APPLICATION ============
if __name__ == '__main__':
    print("Starting SkillTwin Backend Server...")
    print("="*60)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created/verified successfully!")
        
        # Seed sample data
        seed_sample_data()
    
    print("="*60)
    print("Server running on http://0.0.0.0:5000")
    print("="*60)
    print("Available API Endpoints:")
    print("  - Health check: GET /api/health")
    print("  - Login: POST /api/auth/login")
    print("  - Dashboard: GET /api/dashboard/<student_id>")
    print("  - Performance Prediction: GET /api/performance/predict/<student_id>")
    print("="*60)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
