"""
Database utility functions
"""
import json
import os
from datetime import datetime, timedelta
import random
from app import db, Student, Topic, Question, StudentPerformance, MockTest, StudentActivity

def load_sample_data_from_json():
    """Load data from sample_data.json"""
    data_path = os.path.join('data', 'sample_data.json')
    if not os.path.exists(data_path):
        print(f"Sample data file not found: {data_path}")
        return None
    
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_student_by_email(email):
    """Get student by email"""
    return Student.query.filter_by(email=email).first()

def create_demo_data():
    """Create comprehensive demo data"""
    with db.session.no_autoflush:
        # Check if demo student exists
        demo_student = get_student_by_email('demo@skilltwin.com')
        if not demo_student:
            print("Creating demo student...")
            demo_student = Student(
                email='demo@skilltwin.com',
                name='Demo Student',
                class_level='10th Grade',
                school='SkillTwin Academy'
            )
            db.session.add(demo_student)
            db.session.flush()
        
        # Create sample topics if they don't exist
        topics = [
            ('Physics', 'Thermodynamics'),
            ('Physics', 'Optics'),
            ('Physics', 'Mechanics'),
            ('Mathematics', 'Calculus'),
            ('Mathematics', 'Algebra'),
            ('Chemistry', 'Organic Chemistry')
        ]
        
        topic_objects = {}
        for subject, topic_name in topics:
            topic = Topic.query.filter_by(subject=subject, topic_name=topic_name).first()
            if not topic:
                topic = Topic(subject=subject, topic_name=topic_name, difficulty_level=random.randint(1, 5))
                db.session.add(topic)
                db.session.flush()
            topic_objects[f"{subject}_{topic_name}"] = topic
        
        # Create performance records
        for key, topic in topic_objects.items():
            performance = StudentPerformance.query.filter_by(
                student_id=demo_student.id,
                topic_id=topic.id
            ).first()
            
            if not performance:
                mastery = random.randint(40, 90)
                questions = random.randint(20, 100)
                correct = int(questions * mastery / 100)
                
                performance = StudentPerformance(
                    student_id=demo_student.id,
                    topic_id=topic.id,
                    mastery_score=mastery,
                    questions_attempted=questions,
                    questions_correct=correct,
                    total_time_spent=random.randint(60, 300)
                )
                db.session.add(performance)
        
        # Create sample activities
        activity_types = ['test_completed', 'video_watched', 'paper_analyzed', 'question_answered']
        for i in range(10):
            activity_date = datetime.utcnow() - timedelta(days=random.randint(0, 30))
            activity = StudentActivity(
                student_id=demo_student.id,
                activity_type=random.choice(activity_types),
                description=f"Demo activity {i+1}",
                activity_metadata={'score': random.randint(60, 95)},
                duration=random.randint(300, 1800),
                created_at=activity_date
            )
            db.session.add(activity)
        
        db.session.commit()
        print("Demo data created successfully!")
        return demo_student