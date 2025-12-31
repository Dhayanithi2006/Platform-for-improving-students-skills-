from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    performances = db.relationship('StudentPerformance', backref='student', lazy=True)
    tests = db.relationship('MockTest', backref='student', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'class_level': self.class_level,
            'created_at': self.created_at.isoformat()
        }

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    topic_name = db.Column(db.String(200), nullable=False)
    difficulty_level = db.Column(db.Integer, default=2)  # 1-5 scale
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'topic_name': self.topic_name,
            'difficulty_level': self.difficulty_level
        }

class StudentPerformance(db.Model):
    __tablename__ = 'student_performance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    mastery_score = db.Column(db.Float, default=0.0)  # 0-100
    questions_attempted = db.Column(db.Integer, default=0)
    questions_correct = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    topic = db.relationship('Topic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'topic': self.topic.to_dict(),
            'mastery_score': self.mastery_score,
            'questions_attempted': self.questions_attempted,
            'questions_correct': self.questions_correct,
            'last_updated': self.last_updated.isoformat()
        }

class MockTest(db.Model):
    __tablename__ = 'mock_tests'
    
    id = db.Column(db.String(36), primary_key=True)
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    questions = db.Column(db.JSON)  # Store question IDs and answers
    scores = db.Column(db.JSON)     # Per topic scores
    ability_estimate = db.Column(db.Float, default=0.5)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'questions': self.questions,
            'scores': self.scores,
            'ability_estimate': self.ability_estimate,
            'started_at': self.started_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.String(36), primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # List of options
    correct_answer = db.Column(db.String(10), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'topic': self.topic,
            'difficulty': self.difficulty,
            'question_text': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation
        }