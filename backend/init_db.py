"""
Database Initialization Script
Run this once to set up the database with sample data
"""
import json
import os
import sys
from datetime import datetime
from app import app, db, Student, Topic, Question, StudentPerformance

def init_database():
    """Initialize database with sample data"""
    print("Initializing SkillTwin Database...")
    
    # Create tables
    with app.app_context():
        print("1. Creating database tables...")
        db.create_all()
        
        # Load sample data
        sample_file = os.path.join('data', 'sample_data.json')
        if not os.path.exists(sample_file):
            print(f"❌ Error: {sample_file} not found!")
            return
        
        print(f"2. Loading sample data from {sample_file}...")
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample_data = json.load(f)
        
        # Add sample students
        print("3. Adding sample students...")
        for student_data in sample_data.get('students', []):
            # Check if student already exists
            existing = Student.query.filter_by(email=student_data['email']).first()
            if not existing:
                student = Student(
                    id=student_data['id'],
                    email=student_data['email'],
                    name=student_data['name'],
                    class_level=student_data['class_level'],
                    school=student_data.get('school', ''),
                    last_login=datetime.utcnow()
                )
                db.session.add(student)
        
        # Add topics
        print("4. Adding topics...")
        topics_added = set()
        for student_data in sample_data.get('students', []):
            for performance in student_data.get('performance_history', []):
                topic_key = f"{performance['subject']}_{performance['topic']}"
                if topic_key not in topics_added:
                    topic = Topic(
                        subject=performance['subject'],
                        topic_name=performance['topic'],
                        difficulty_level=2
                    )
                    db.session.add(topic)
                    topics_added.add(topic_key)
        
        # Add questions
        print("5. Adding sample questions...")
        for question_data in sample_data.get('questions', []):
            existing = Question.query.filter_by(id=question_data['id']).first()
            if not existing:
                question = Question(
                    id=question_data['id'],
                    subject=question_data['subject'],
                    topic=question_data['topic'],
                    difficulty=question_data['difficulty'],
                    question_text=question_data['question_text'],
                    options=question_data['options'],
                    correct_answer=question_data['correct_answer'],
                    explanation=question_data.get('explanation', ''),
                    marks=question_data.get('marks', 1)
                )
                db.session.add(question)
        
        # Commit all changes
        db.session.commit()
        
        # Add performance data for demo student
        print("6. Adding performance data...")
        demo_student = Student.query.filter_by(email='demo@skilltwin.com').first()
        if demo_student:
            for student_data in sample_data.get('students', []):
                if student_data['email'] == 'demo@skilltwin.com':
                    for performance in student_data.get('performance_history', []):
                        topic = Topic.query.filter_by(
                            subject=performance['subject'],
                            topic_name=performance['topic']
                        ).first()
                        
                        if topic:
                            perf_record = StudentPerformance(
                                student_id=demo_student.id,
                                topic_id=topic.id,
                                mastery_score=performance['mastery'],
                                questions_attempted=len(performance['quiz_scores']) * 5,
                                questions_correct=int(len(performance['quiz_scores']) * 5 * performance['mastery']/100),
                                total_time_spent=performance['engagement_time']
                            )
                            db.session.add(perf_record)
        
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print(f"   Students: {Student.query.count()}")
        print(f"   Topics: {Topic.query.count()}")
        print(f"   Questions: {Question.query.count()}")
        print(f"   Performance records: {StudentPerformance.query.count()}")

if __name__ == '__main__':
    # Add project root to path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        init_database()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()