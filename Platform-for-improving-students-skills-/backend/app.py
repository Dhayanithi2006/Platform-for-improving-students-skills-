"""
SkillTwin Backend - Complete Updated Version
Proactive Learning & Evaluation Platform
"""
import os
import sys
import uuid
import json
from datetime import datetime
from flask import Flask, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, Response, request, jsonify, send_from_directory
from flask.wrappers import Response
from flask.wrappers import Response
from flask.wrappers import Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import tempfile

from sqlalchemy.orm.relationships import RelationshipProperty

from sqlalchemy.orm.relationships import RelationshipProperty

from sqlalchemy.orm.relationships import RelationshipProperty

from sqlalchemy.orm.relationships import RelationshipProperty

from sqlalchemy.orm.relationships import RelationshipProperty

from werkzeug.datastructures.file_storage import FileStorage
from typing import Any, Literal

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all origins in development
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all origins for development
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Origin", "X-Requested-With"],
        "supports_credentials": True
    }
})

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///skilltwin.db')
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
    __tablename__: str = 'users'  # Changed from 'students' to 'users' to match our database
    
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
    student_id = db.Column(db.String(36), db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
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
    student_id = db.Column(db.String(36), db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    activity_metadata = db.Column(db.JSON, default=dict)  # Changed from 'metadata'
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
    student_id = db.Column(db.String(36), db.ForeignKey('students.id', ondelete='CASCADE'))
    filename = db.Column(db.String(255))
    original_filename = db.Column(db.String(255))
    subject = db.Column(db.String(100))
    analysis_data = db.Column(db.JSON, default=dict)  # Changed from 'metadata'
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
            school="SkillTwin Academy"
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
                student_id=demo_student.id,
                topic_id=topics[0].id,  # Thermodynamics
                mastery_score=65,
                questions_attempted=50,
                questions_correct=32,
                total_time_spent=120
            ),
            StudentPerformance(
                student_id=demo_student.id,
                topic_id=topics[1].id,  # Optics
                mastery_score=45,
                questions_attempted=40,
                questions_correct=18,
                total_time_spent=90
            ),
            StudentPerformance(
                student_id=demo_student.id,
                topic_id=topics[2].id,  # Mechanics
                mastery_score=80,
                questions_attempted=60,
                questions_correct=48,
                total_time_spent=180
            ),
            StudentPerformance(
                student_id=demo_student.id,
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
                subject="Physics",
                topic="Mechanics",
                difficulty="medium",
                question_text="A ball is thrown vertically upward with velocity 20 m/s. What maximum height will it reach? (g = 10 m/s²)",
                options=["10 m", "20 m", "30 m", "40 m"],
                correct_answer="B",
                explanation="Using v² = u² - 2gh, at max height v = 0. So h = u²/2g = (20)²/(2*10) = 20 m.",
                marks=3
            ),
            Question(
                id="Q004",
                subject="Mathematics",
                topic="Calculus",
                difficulty="hard",
                question_text="Find the derivative of f(x) = x³ sin(x)",
                options=["3x² sin(x) + x³ cos(x)", "3x² cos(x)", "x³ cos(x)", "3x² sin(x) - x³ cos(x)"],
                correct_answer="A",
                explanation="Using product rule: d(uv)/dx = u'v + uv'. Here u = x³, v = sin(x). So f'(x) = 3x² sin(x) + x³ cos(x).",
                marks=4
            )
        ]
        
        for question in questions:
            db.session.add(question)
        
        # Create sample activities
        activities: list[StudentActivity] = [
            StudentActivity(
                student_id=demo_student.id,
                activity_type="test_completed",
                description="Completed Physics Adaptive Test",
                activity_metadata={"score": 75, "subject": "Physics", "duration": 1200},
                duration=1200,
                created_at=datetime.utcnow()
            ),
            StudentActivity(
                student_id=demo_student.id,
                activity_type="video_watched",
                description="Watched Thermodynamics tutorial",
                activity_metadata={"topic": "Thermodynamics", "duration": 900},
                duration=900,
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

# ============ SIMPLE ML ENGINE (No external dependencies) ============
class SimplePredictor:
    """Simple performance predictor without numpy/scikit-learn"""
    
    def __init__(self) -> None:
        pass
    
    def predict(self, student_data):
        """Simple prediction based on mastery scores"""
        avg_mastery = student_data.get('average_mastery', 50)
        engagement = student_data.get('engagement_score', 0.5)
        
        # Simple linear prediction
        base_score = avg_mastery * 0.8 + engagement * 20
        base_score: int = max(0, min(100, base_score))
        
        # Add some randomness
        import random
        variation: float = random.uniform(-5, 5)
        predicted_score: float = base_score + variation
        
        return {
            'predicted_score': round(predicted_score, 1),
            'confidence_interval': [
                round(predicted_score - 5, 1),
                round(predicted_score + 5, 1)
            ],
            'confidence': round(85 + random.uniform(-10, 10), 1)
        }
    
    def assess_risk(self, predicted_score) -> str:
        """Assess risk level"""
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
                school=data.get('school', 'SkillTwin Academy')
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

@app.route('/api/auth/register', methods=['POST'])
def register() -> tuple[Response, Literal[400]] | tuple[Response, Literal[409]] | Response | tuple[Response, Literal[500]]:
    """User registration endpoint"""
    try:
        data = request.json
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        existing = Student.query.filter_by(email=data['email']).first()
        if existing:
            return jsonify({'success': False, 'error': 'Email already registered'}), 409
        
        student = Student(
            email=data['email'],
            name=data['name'],
            password=data['password'],
            class_level=data.get('class_level'),
            school=data.get('school')
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': student.to_dict(),
            'message': 'Registration successful'
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
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        # Get performance data
        performances = StudentPerformance.query.filter_by(student_id=student_id).all()
        
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
        recent_activities = StudentActivity.query.filter_by(student_id=student_id)\
            .order_by(StudentActivity.created_at.desc())\
            .limit(5).all()
        
        # Get recent tests
        recent_tests = MockTest.query.filter_by(student_id=student_id)\
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
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        # Get student performance data
        performances = StudentPerformance.query.filter_by(student_id=student_id).all()
        
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

@app.route('/api/performance/update', methods=['POST'])
def update_performance() -> tuple[Response, Literal[400]] | tuple[Response, Literal[404]] | Response | tuple[Response, Literal[500]]:
    """Update student performance after activity"""
    try:
        data = request.json
        student_id = data.get('student_id')
        topic_id = data.get('topic_id')
        correct = data.get('correct', False)
        time_spent = data.get('time_spent', 0)
        
        if not student_id or not topic_id:
            return jsonify({'success': False, 'error': 'Student ID and Topic ID required'}), 400
        
        # Find or create performance record
        performance = StudentPerformance.query.filter_by(
            student_id=student_id,
            topic_id=topic_id
        ).first()
        
        if not performance:
            # Get topic first
            topic = Topic.query.get(topic_id)
            if not topic:
                return jsonify({'success': False, 'error': 'Topic not found'}), 404
            
            performance = StudentPerformance(
                student_id=student_id,
                topic_id=topic_id,
                mastery_score=50,
                questions_attempted=0,
                questions_correct=0,
                total_time_spent=0
            )
            db.session.add(performance)
        
        # Update performance
        performance.questions_attempted += 1
        if correct:
            performance.questions_correct += 1
        
        # Calculate new mastery score
        accuracy: os.Any | int = performance.questions_correct / performance.questions_attempted if performance.questions_attempted > 0 else 0
        performance.mastery_score = round(accuracy * 100, 2)
        
        # Update time spent
        performance.total_time_spent += time_spent // 60
        
        # Record activity
        activity = StudentActivity(
            student_id=student_id,
            activity_type='question_answered',
            description=f"Answered question on topic {topic_id}",
            activity_metadata={'topic_id': topic_id, 'correct': correct, 'time_spent': time_spent},
            duration=time_spent
        )
        db.session.add(activity)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'performance': performance.to_dict(),
            'message': 'Performance updated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ ADAPTIVE TEST ROUTES ============
@app.route('/api/tests/adaptive/start', methods=['POST'])
def start_adaptive_test() -> tuple[Response, Literal[400]] | Response | tuple[Response, Literal[500]]:
    """Start an adaptive test"""
    try:
        data = request.json
        student_id = data.get('student_id')
        subject = data.get('subject', 'Physics')
        test_type = data.get('test_type', 'adaptive')
        
        if not student_id:
            return jsonify({'success': False, 'error': 'Student ID required'}), 400
        
        # Reset adaptive engine
        adaptive_engine.reset()
        
        # Get first question based on subject and initial difficulty
        first_question = Question.query.filter_by(
            subject=subject,
            difficulty='medium'
        ).first()
        
        if not first_question:
            # Fallback to any question in subject
            first_question = Question.query.filter_by(subject=subject).first()
            
        if not first_question:
            # Create a mock question
            first_question = Question(
                subject=subject,
                topic="Thermodynamics" if subject == "Physics" else "Calculus",
                difficulty="medium",
                question_text=f"Sample {subject} question for adaptive testing",
                options=["Option A", "Option B", "Option C", "Option D"],
                correct_answer="B",
                explanation="This is a sample question for testing"
            )
            db.session.add(first_question)
            db.session.flush()
        
        # Create test session
        test = MockTest(
            student_id=student_id,
            subject=subject,
            test_type=test_type,
            questions=[first_question.to_dict()],
            ability_estimate=adaptive_engine.ability_estimate
        )
        db.session.add(test)
        
        # Record activity
        activity = StudentActivity(
            student_id=student_id,
            activity_type='test_started',
            description=f"Started {test_type} test in {subject}",
            activity_metadata={'test_id': test.id, 'subject': subject, 'test_type': test_type},
            duration=0
        )
        db.session.add(activity)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'test_id': test.id,
            'question': first_question.to_dict(),
            'question_number': 1,
            'total_questions': 10,
            'ability_estimate': adaptive_engine.ability_estimate,
            'time_limit': 600
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tests/adaptive/submit', methods=['POST'])
def submit_adaptive_answer() -> tuple[Response, Literal[400]] | tuple[Response, Literal[404]] | Response | tuple[Response, Literal[500]]:
    """Submit answer and get next question"""
    try:
        data = request.json
        test_id = data.get('test_id')
        answer = data.get('answer')
        question_id = data.get('question_id')
        response_time = data.get('response_time', 30)
        
        if not test_id or not answer or not question_id:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        test = MockTest.query.get(test_id)
        if not test:
            return jsonify({'success': False, 'error': 'Test not found'}), 404
        
        # Get current question
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'success': False, 'error': 'Question not found'}), 404
        
        # Determine if answer was correct
        is_correct = answer.strip().upper() == question.correct_answer.strip().upper()
        
        # Update test record
        if not test.answers:
            test.answers = []
        if not test.questions:
            test.questions = []
        
        test.answers.append({
            'question_id': question_id,
            'answer': answer,
            'correct': is_correct,
            'response_time': response_time
        })
        
        # Update ability estimate and get next difficulty
        next_difficulty: str = adaptive_engine.get_next_difficulty(is_correct, response_time)
        
        # Check if test is complete
        questions_completed: int = len(test.answers)
        test_completed: bool = questions_completed >= 10
        
        next_question = None
        if not test_completed:
            # Get next question
            next_question = Question.query.filter_by(
                subject=test.subject,
                difficulty=next_difficulty
            ).first()
            
            # If no question at that difficulty, get closest
            if not next_question:
                difficulties: list[str] = ['easy', 'medium', 'hard']
                current_idx: int = difficulties.index(next_difficulty) if next_difficulty in difficulties else 1
                
                # Try adjacent difficulties
                for offset in [0, 1, -1, 2, -2]:
                    idx = current_idx + offset
                    if 0 <= idx < len(difficulties):
                        next_question = Question.query.filter_by(
                            subject=test.subject,
                            difficulty=difficulties[idx]
                        ).first()
                        if next_question:
                            break
            
            if next_question:
                test.questions.append(next_question.to_dict())
        
        # Update ability estimate in test
        test.ability_estimate = adaptive_engine.ability_estimate
        
        if test_completed:
            test.completed_at = datetime.utcnow()
            test.time_taken = sum(a.get('response_time', 0) for a in test.answers)
            
            # Calculate score
            correct_answers: int = sum(1 for a in test.answers if a.get('correct', False))
            test.total_score = (correct_answers / len(test.answers)) * 100 if test.answers else 0
            
            # Update performance
            activity = StudentActivity(
                student_id=test.student_id,
                activity_type='test_completed',
                description=f"Completed {test.test_type} test in {test.subject}",
                activity_metadata={'test_id': test.id, 'score': test.total_score, 'subject': test.subject},
                duration=test.time_taken
            )
            db.session.add(activity)
        
        db.session.commit()
        
        response_data = {
            'success': True,
            'correct': is_correct,
            'explanation': question.explanation,
            'ability_estimate': adaptive_engine.ability_estimate,
            'questions_completed': questions_completed,
            'test_completed': test_completed
        }
        
        if not test_completed and next_question:
            response_data['next_question'] = next_question.to_dict()
            response_data['next_difficulty'] = next_difficulty
        elif test_completed:
            response_data['final_score'] = test.total_score
            response_data['correct_answers'] = correct_answers
            response_data['total_questions'] = len(test.answers)
            response_data['time_taken'] = test.time_taken
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tests/history/<student_id>', methods=['GET'])
def get_test_history(student_id) -> Response | tuple[Response, Literal[500]]:
    """Get test history for student"""
    try:
        tests = MockTest.query.filter_by(student_id=student_id)\
            .order_by(MockTest.started_at.desc())\
            .limit(20).all()
        
        return jsonify({
            'success': True,
            'tests': [test.to_dict() for test in tests]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ PAPER ANALYSIS ROUTES ============
@app.route('/api/papers/upload', methods=['POST'])
def upload_and_analyze_paper() -> tuple[Response, Literal[400]] | Response | tuple[Response, Literal[500]]:
    """Upload and analyze question paper"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file: FileStorage = request.files['file']
        student_id: str | None = request.form.get('student_id')
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # For demo, just analyze without actual PDF parsing
            analysis = {
                'metadata': {
                    'subject': 'Physics',
                    'total_questions_estimated': 50,
                    'analysis_timestamp': datetime.utcnow().isoformat(),
                    'paper_difficulty_overall': 'Medium'
                },
                'topic_distribution': {
                    'Physics_Thermodynamics': 30.0,
                    'Physics_Optics': 25.0,
                    'Physics_Mechanics': 25.0,
                    'Physics_Modern_Physics': 20.0
                },
                'difficulty_analysis': {
                    'easy': 40.0,
                    'medium': 40.0,
                    'hard': 20.0,
                    'unknown': 0.0
                },
                'score_prediction': {
                    'expected_score': 75.0,
                    'score_range': [68.0, 82.0],
                    'confidence': 0.85
                },
                'recommendations': [
                    {
                        'topic': 'Thermodynamics',
                        'subject': 'Physics',
                        'weight_in_paper': 30.0,
                        'current_mastery': 65.0,
                        'priority': 'high',
                        'recommended_time': '2 hours',
                        'resources': [
                            'Video: Thermodynamics concepts explained',
                            'Notes: Thermodynamics formula sheet',
                            'Practice: 10 problems on Thermodynamics'
                        ],
                        'action_items': [
                            'Watch 20-minute video on Thermodynamics',
                            'Solve 5 basic problems on Thermodynamics',
                            'Create summary notes for Thermodynamics'
                        ]
                    }
                ],
                'key_insights': [
                    'Most important topic: Physics_Thermodynamics (30.0% weightage)',
                    'Paper has mostly easy to moderate difficulty questions',
                    'Focus on 1 high-priority topics for maximum improvement'
                ],
                'study_plan': {
                    'total_days': 7,
                    'daily_target': '2-3 hours',
                    'schedule': [
                        {
                            'day': 'Day 1-2',
                            'focus': 'High Priority Topics',
                            'topics': ['Thermodynamics'],
                            'activities': ['Concept learning', 'Basic practice', 'Note making']
                        },
                        {
                            'day': 'Day 3-4',
                            'focus': 'Medium Priority Topics',
                            'topics': ['Optics', 'Mechanics'],
                            'activities': ['Problem solving', 'Previous year questions', 'Revision']
                        },
                        {
                            'day': 'Day 5',
                            'focus': 'Mixed Practice',
                            'topics': ['All weak topics'],
                            'activities': ['Mock test', 'Time-bound practice', 'Error analysis']
                        },
                        {
                            'day': 'Day 6',
                            'focus': 'Low Priority Topics',
                            'topics': ['Modern Physics'],
                            'activities': ['Quick revision', 'Formula review', 'Important questions']
                        },
                        {
                            'day': 'Day 7',
                            'focus': 'Final Revision',
                            'topics': ['All important topics'],
                            'activities': ['Complete paper solving', 'Time management practice', 'Relaxation']
                        }
                    ]
                }
            }
            
            # Save analysis to database
            paper_analysis = PaperAnalysis(
                student_id=student_id,
                filename=file.filename,
                original_filename=file.filename,
                subject=analysis['metadata']['subject'],
                analysis_data=analysis
            )
            db.session.add(paper_analysis)
            
            # Record activity
            if student_id:
                activity = StudentActivity(
                    student_id=student_id,
                    activity_type='paper_analyzed',
                    description=f"Analyzed paper: {file.filename}",
                    activity_metadata={
                        'filename': file.filename,
                        'subject': analysis['metadata']['subject'],
                        'predicted_score': analysis['score_prediction']['expected_score']
                    },
                    duration=60
                )
                db.session.add(activity)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'analysis_id': paper_analysis.id,
                'filename': file.filename,
                'analysis': analysis,
                'message': 'Paper analyzed successfully'
            })
        
        return jsonify({'success': False, 'error': 'Invalid file type. Only PDF files are allowed.'}), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/papers/quick-analyze', methods=['POST'])
def quick_analyze_paper() -> tuple[Response, Literal[400]] | Response | tuple[Response, Literal[500]]:
    """Analyze paper from text content"""
    try:
        data = request.json
        paper_text = data.get('paper_text', '')
        student_id = data.get('student_id')
        
        if not paper_text:
            return jsonify({'success': False, 'error': 'No paper text provided'}), 400
        
        # Simple analysis based on text
        subject: str = 'Physics' if 'physics' in paper_text.lower() else 'Mathematics' if 'mathematics' in paper_text.lower() else 'General'
        
        analysis = {
            'metadata': {
                'subject': subject,
                'total_questions_estimated': paper_text.count('?') or 10,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'paper_difficulty_overall': 'Medium'
            },
            'topic_distribution': {
                'Physics_Thermodynamics': 30.0,
                'Physics_Optics': 25.0,
                'Physics_Mechanics': 25.0,
                'Physics_Modern_Physics': 20.0
            },
            'difficulty_analysis': {
                'easy': 40.0,
                'medium': 40.0,
                'hard': 20.0,
                'unknown': 0.0
            },
            'score_prediction': {
                'expected_score': 75.0,
                'score_range': [68.0, 82.0],
                'confidence': 0.85
            },
            'recommendations': [
                {
                    'topic': 'Thermodynamics',
                    'subject': 'Physics',
                    'weight_in_paper': 30.0,
                    'current_mastery': 65.0,
                    'priority': 'high',
                    'recommended_time': '2 hours',
                    'resources': [
                        'Video: Thermodynamics concepts explained',
                        'Notes: Thermodynamics formula sheet'
                    ],
                    'action_items': [
                        'Watch 20-minute video on Thermodynamics',
                        'Solve 5 basic problems on Thermodynamics'
                    ]
                }
            ]
        }
        
        # Save analysis to database
        paper_analysis = PaperAnalysis(
            student_id=student_id,
            filename='text_input.txt',
            original_filename='text_input.txt',
            subject=subject,
            analysis_data=analysis
        )
        db.session.add(paper_analysis)
        
        # Record activity
        if student_id:
            activity = StudentActivity(
                student_id=student_id,
                activity_type='paper_analyzed',
                description="Analyzed paper from text input",
                activity_metadata={
                    'subject': subject,
                    'predicted_score': analysis['score_prediction']['expected_score']
                },
                duration=30
            )
            db.session.add(activity)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'analysis_id': paper_analysis.id,
            'analysis': analysis,
            'message': 'Paper analyzed successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/papers/sample-analysis', methods=['GET'])
def get_sample_analysis() -> Response | tuple[Response, Literal[500]]:
    """Get sample analysis for demo purposes"""
    try:
        analysis = {
            'metadata': {
                'subject': 'Physics',
                'total_questions_estimated': 50,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'paper_difficulty_overall': 'Medium'
            },
            'topic_distribution': {
                'Physics_Thermodynamics': 30.0,
                'Physics_Optics': 25.0,
                'Physics_Mechanics': 25.0,
                'Physics_Modern_Physics': 20.0
            },
            'difficulty_analysis': {
                'easy': 40.0,
                'medium': 40.0,
                'hard': 20.0,
                'unknown': 0.0
            },
            'score_prediction': {
                'expected_score': 75.0,
                'score_range': [68.0, 82.0],
                'confidence': 0.85
            },
            'recommendations': [
                {
                    'topic': 'Thermodynamics',
                    'subject': 'Physics',
                    'weight_in_paper': 30.0,
                    'current_mastery': 65.0,
                    'priority': 'high',
                    'recommended_time': '2 hours',
                    'resources': [
                        'Video: Thermodynamics concepts explained',
                        'Notes: Thermodynamics formula sheet'
                    ],
                    'action_items': [
                        'Watch 20-minute video on Thermodynamics',
                        'Solve 5 basic problems on Thermodynamics'
                    ]
                }
            ],
            'note': 'This is sample analysis data for demonstration'
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/papers/history/<student_id>', methods=['GET'])
def get_paper_history(student_id) -> Response | tuple[Response, Literal[500]]:
    """Get paper analysis history for student"""
    try:
        analyses = PaperAnalysis.query.filter_by(student_id=student_id)\
            .order_by(PaperAnalysis.created_at.desc())\
            .limit(10).all()
        
        return jsonify({
            'success': True,
            'analyses': [{
                'id': a.id,
                'filename': a.original_filename,
                'subject': a.subject,
                'created_at': a.created_at.isoformat() if a.created_at else None,
                'predicted_score': a.analysis_data.get('score_prediction', {}).get('expected_score')
            } for a in analyses]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ LEARNING RECOMMENDATIONS ROUTES ============
@app.route('/api/recommendations/<student_id>', methods=['GET'])
def get_recommendations(student_id) -> Response | tuple[Response, Literal[500]]:
    """Get personalized learning recommendations"""
    try:
        # Get weak topics
        performances = StudentPerformance.query.filter_by(student_id=student_id).all()
        weak_topics: list[Any] = sorted(performances, key=lambda x: x.mastery_score)[:3] if performances else []
        
        recommendations = []
        
        for performance in weak_topics:
            if performance.topic:
                recommendations.append({
                    'type': 'video',
                    'title': f'Master {performance.topic.topic_name} in 15 minutes',
                    'description': f'Comprehensive video covering key concepts in {performance.topic.topic_name}',
                    'duration': '15:30',
                    'subject': performance.topic.subject,
                    'topic': performance.topic.topic_name,
                    'priority': 'high' if performance.mastery_score < 50 else 'medium',
                    'url': f'/videos/{performance.topic.id}',
                    'icon': '🎬'
                })
                
                recommendations.append({
                    'type': 'notes',
                    'title': f'Summary notes: {performance.topic.topic_name}',
                    'description': 'Concise notes with formulas and key points',
                    'pages': 3,
                    'subject': performance.topic.subject,
                    'topic': performance.topic.topic_name,
                    'priority': 'medium',
                    'url': f'/notes/{performance.topic.id}',
                    'icon': '📝'
                })
                
                recommendations.append({
                    'type': 'quiz',
                    'title': f'Quick quiz: {performance.topic.topic_name}',
                    'description': '5 questions to test your understanding',
                    'questions': 5,
                    'estimated_time': '10 minutes',
                    'subject': performance.topic.subject,
                    'topic': performance.topic.topic_name,
                    'priority': 'medium',
                    'url': f'/quizzes/{performance.topic.id}',
                    'icon': '❓'
                })
        
        # Add general recommendations
        recommendations.extend([
            {
                'type': 'practice',
                'title': 'Daily Mixed Practice',
                'description': '10 questions from different topics',
                'questions': 10,
                'estimated_time': '20 minutes',
                'subject': 'Mixed',
                'priority': 'medium',
                'url': '/practice/daily',
                'icon': '📚'
            },
            {
                'type': 'mock_test',
                'title': 'Full Length Mock Test',
                'description': 'Complete test with time limit',
                'duration': '60 minutes',
                'questions': 30,
                'subject': 'Physics',
                'priority': 'low',
                'url': '/tests/full',
                'icon': '⏱️'
            }
        ])
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'daily_goal': 'Complete 2 videos and 1 quiz',
            'progress_today': '1/3 activities completed',
            'weekly_progress': '65%'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ TOPICS & QUESTIONS ROUTES ============
@app.route('/api/topics', methods=['GET'])
def get_topics() -> Response | tuple[Response, Literal[500]]:
    """Get all topics with optional filtering"""
    try:
        subject: str | None = request.args.get('subject')
        
        query = Topic.query
        if subject:
            query = query.filter_by(subject=subject)
        
        topics = query.order_by(Topic.subject, Topic.topic_name).all()
        
        return jsonify({
            'success': True,
            'topics': [topic.to_dict() for topic in topics]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/questions', methods=['GET'])
def get_questions() -> Response | tuple[Response, Literal[500]]:
    """Get questions with optional filtering"""
    try:
        subject: str | None = request.args.get('subject')
        topic: str | None = request.args.get('topic')
        difficulty: str | None = request.args.get('difficulty')
        limit = int(request.args.get('limit', 10))
        
        query = Question.query
        if subject:
            query = query.filter_by(subject=subject)
        if topic:
            query = query.filter_by(topic=topic)
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        questions = query.limit(limit).all()
        
        return jsonify({
            'success': True,
            'questions': [q.to_dict() for q in questions],
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ ACTIVITIES ROUTES ============
@app.route('/api/activities/<student_id>', methods=['GET'])
def get_activities(student_id) -> Response | tuple[Response, Literal[500]]:
    """Get student activities"""
    try:
        limit = int(request.args.get('limit', 20))
        activity_type: str | None = request.args.get('type')
        
        query = StudentActivity.query.filter_by(student_id=student_id)
        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        
        activities = query.order_by(StudentActivity.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'activities': [act.to_dict() for act in activities]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ HEALTH & UTILITY ROUTES ============
@app.route('/api/health', methods=['GET'])
def health_check() -> Response:
    """Health check endpoint"""
    print("DEBUG: health_check called")
    # Use a safe command to verify DB connectivity (SQLAlchemy 2.x compatible)
    db_status = 'disconnected'
    try:
        # Attempt a lightweight query
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        print("DEBUG: health_check db exception:", repr(e))
        db_status = 'disconnected'

    return jsonify({
        'status': 'healthy' if db_status == 'connected' else 'degraded',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'service': 'SkillTwin Backend API',
        'database': db_status
    })

@app.route('/api/init', methods=['POST'])
def initialize_database() -> Response | tuple[Response, Literal[500]]:
    """Initialize database with sample data"""
    try:
        with app.app_context():
            db.create_all()
            seed_sample_data()
        
        return jsonify({
            'success': True,
            'message': 'Database initialized successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_database() -> Response | tuple[Response, Literal[500]]:
    """Reset database (for development only)"""
    try:
        with app.app_context():
            # Drop all tables
            db.drop_all()
            # Create fresh tables
            db.create_all()
            # Seed sample data
            seed_sample_data()
        
        return jsonify({
            'success': True,
            'message': 'Database reset successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ STATIC FILES ============
@app.route('/uploads/<filename>')
def uploaded_file(filename) -> Response:
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ============ FRONTEND STATIC SERVE ============
# Absolute build dir used to serve static files
BUILD_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))

@app.route('/static/<path:filename>')
def serve_static(filename) -> Response:
    """Serve static files from build directory"""
    try:
        static_path = os.path.join(BUILD_DIR, 'static', filename)
        if os.path.exists(static_path) and os.path.isfile(static_path):
            return send_from_directory(os.path.join(BUILD_DIR, 'static'), filename)
        else:
            print(f"Static file not found: {static_path}")
            return jsonify({'error': 'Static file not found', 'path': filename}), 404
    except Exception as e:
        print(f"Error serving static file: {e}")
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/')
def serve_root() -> Response:
    """Serve index.html directly"""
    index_path = os.path.join(BUILD_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(BUILD_DIR, 'index.html')
    return jsonify({'error': 'Frontend build not found', 'success': False}), 404

@app.route('/<path:path>')
def serve_frontend(path) -> Response:
    """Serve the React production build files"""
    # First try to serve from build directory
    requested = os.path.join(BUILD_DIR, path)
    if os.path.exists(requested) and os.path.isfile(requested):
        return send_from_directory(BUILD_DIR, path)
    # fallback to index.html for client-side routes
    index_path = os.path.join(BUILD_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(BUILD_DIR, 'index.html')
    return jsonify({'error': 'Resource not found', 'success': False}), 404

# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(error) -> tuple[Response, Literal[404]]:
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error) -> tuple[Response, Literal[500]]:
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.errorhandler(413)
def request_entity_too_large(error) -> tuple[Response, Literal[413]]:
    return jsonify({'success': False, 'error': 'File too large. Maximum size is 16MB'}), 413

# ============ MAIN APPLICATION ============
if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    with app.app_context():
        db.create_all()
        seed_sample_data()
    
    print(f"""
{'='*60}
SkillTwin Backend Server
Python Version: {sys.version.split()[0]}
Database: {app.config['SQLALCHEMY_DATABASE_URI']}
Upload folder: {app.config['UPLOAD_FOLDER']}
Server running on http://localhost:5000
{'='*60}

📚 Available API Endpoints:
  - Health check: GET /api/health
  - Login: POST /api/auth/login
  - Dashboard: GET /api/dashboard/<student_id>
  - Performance prediction: GET /api/performance/predict/<student_id>
  - Paper analysis: POST /api/papers/upload
  - Adaptive test: POST /api/tests/adaptive/start
  - Learning recommendations: GET /api/recommendations/<student_id>

🔐 Demo Credentials:
  - Email: demo@skilltwin.com
  - Password: demo123

📁 Database initialized with sample data.
{'='*60}
""")
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)