import os
import re
import json
import PyPDF2
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple, Any
from datetime import datetime

class PaperAnalyzer:
    def __init__(self, student_performance_data: Dict = None):
        """
        Initialize Paper Analyzer with student performance data
        
        Args:
            student_performance_data: Dictionary containing student's performance metrics
        """
        self.student_data = student_performance_data or {}
        
        # Topic keywords database (can be expanded)
        self.topic_keywords = {
            'Physics': {
                'thermodynamics': [
                    'heat', 'temperature', 'entropy', 'carnot', 'adiabatic', 
                    'isothermal', 'enthalpy', 'internal energy', 'work done',
                    'first law', 'second law', 'heat engine', 'refrigerator',
                    'specific heat', 'thermal expansion', 'heat transfer',
                    'boyle\'s law', 'charles\' law', 'ideal gas', 'PV diagram'
                ],
                'optics': [
                    'lens', 'mirror', 'refraction', 'reflection', 'focal length',
                    'image formation', 'magnification', 'snell\'s law',
                    'critical angle', 'total internal reflection', 'dispersion',
                    'prism', 'optical instruments', 'microscope', 'telescope',
                    'interference', 'diffraction', 'polarization', 'wave optics'
                ],
                'mechanics': [
                    'force', 'velocity', 'acceleration', 'newton', 'friction',
                    'momentum', 'work', 'energy', 'power', 'kinetic energy',
                    'potential energy', 'conservation', 'projectile', 'circular motion',
                    'gravity', 'gravitation', 'kepler', 'simple harmonic motion',
                    'elasticity', 'viscosity', 'surface tension', 'fluid mechanics'
                ],
                'electromagnetism': [
                    'electric field', 'magnetic field', 'coulomb', 'gauss',
                    'capacitor', 'resistor', 'inductor', 'circuit', 'ohm\'s law',
                    'kirchhoff', 'faraday', 'lenz', 'electromagnetic induction',
                    'ac current', 'transformer', 'motor', 'generator', 'solenoid'
                ],
                'modern_physics': [
                    'quantum', 'photon', 'electron', 'photoelectric', 'de broglie',
                    'heisenberg', 'schrodinger', 'atomic model', 'bohr',
                    'radioactivity', 'nuclear', 'fission', 'fusion', 'semiconductor',
                    'diode', 'transistor', 'logic gates', 'communication system'
                ]
            },
            'Mathematics': {
                'calculus': [
                    'derivative', 'differentiation', 'integration', 'limit',
                    'continuity', 'differentiability', 'maxima', 'minima',
                    'tangent', 'normal', 'area under curve', 'definite integral',
                    'indefinite integral', 'partial derivative', 'differential equation'
                ],
                'algebra': [
                    'matrix', 'determinant', 'vector', 'linear equation',
                    'quadratic', 'polynomial', 'complex number', 'sequence',
                    'series', 'permutation', 'combination', 'probability',
                    'inequality', 'binomial theorem', 'mathematical induction'
                ],
                'geometry': [
                    'coordinate', 'straight line', 'circle', 'parabola',
                    'ellipse', 'hyperbola', '3d geometry', 'distance',
                    'section formula', 'triangle', 'quadrilateral', 'polygon'
                ],
                'trigonometry': [
                    'trigonometric', 'sine', 'cosine', 'tangent', 'cotangent',
                    'secant', 'cosecant', 'identity', 'equation', 'inverse',
                    'height and distance', 'triangle solution'
                ]
            },
            'Chemistry': {
                'physical_chemistry': [
                    'mole concept', 'stoichiometry', 'atomic structure',
                    'chemical bonding', 'thermodynamics', 'equilibrium',
                    'redox', 'electrochemistry', 'chemical kinetics',
                    'surface chemistry', 'solid state', 'solutions'
                ],
                'organic_chemistry': [
                    'hydrocarbon', 'alkyl', 'aryl', 'functional group',
                    'isomerism', 'reaction mechanism', 'named reaction',
                    'polymer', 'biomolecule', 'chemistry in everyday life'
                ],
                'inorganic_chemistry': [
                    'periodic table', 's block', 'p block', 'd block',
                    'f block', 'coordination compound', 'metallurgy',
                    'qualitative analysis', 'environmental chemistry'
                ]
            }
        }
        
        # Difficulty indicators
        self.difficulty_indicators = {
            'easy': ['define', 'state', 'what is', 'name', 'list', 'identify'],
            'medium': ['explain', 'describe', 'calculate', 'derive', 'show', 'prove'],
            'hard': ['analyze', 'evaluate', 'compare', 'contrast', 'justify', 'critically examine']
        }
        
        # Question types
        self.question_types = {
            'mcq': ['option', 'choose', 'correct', 'incorrect', 'a)', 'b)', 'c)', 'd)'],
            'numerical': ['calculate', 'find', 'solve', 'value', 'answer', 'numerical'],
            'derivation': ['derive', 'prove', 'show that', 'expression', 'formula'],
            'explanation': ['explain', 'describe', 'discuss', 'why', 'how']
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from uploaded PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string
        """
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"
                    
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            # For demo purposes, return sample text
            text = self._get_sample_paper_text()
            
        return text
    
    def _get_sample_paper_text(self) -> str:
        """Return sample paper text for demo purposes"""
        return """
        PHYSICS - MID TERM EXAMINATION
        Time: 3 Hours | Maximum Marks: 70
        
        SECTION A
        1. Define entropy. (2 marks)
        2. State First Law of Thermodynamics. (2 marks)
        3. Calculate the work done in isothermal expansion of an ideal gas. (3 marks)
        4. Derive Carnot's theorem. (5 marks)
        
        SECTION B
        5. Explain the working of a heat engine with PV diagram. (5 marks)
        6. Two lenses of focal length 10cm and -15cm are placed in contact. 
           Find the focal length of combination. (4 marks)
        7. Derive lens maker's formula. (5 marks)
        
        SECTION C
        8. Compare isothermal and adiabatic processes. (6 marks)
        9. A carnot engine works between temperatures 400K and 300K. 
           Calculate its efficiency. (4 marks)
        10. Explain photoelectric effect with Einstein's equation. (6 marks)
        
        SECTION D
        11. Derive expression for pressure of ideal gas using kinetic theory. (8 marks)
        12. Solve the differential equation for damped harmonic oscillator. (10 marks)
        """
    
    def identify_topics(self, text: str, subject: str = None) -> Dict[str, float]:
        """
        Identify topics from paper text
        
        Args:
            text: Extracted text from paper
            subject: Subject name (Physics, Mathematics, Chemistry)
            
        Returns:
            Dictionary with topics and their weights
        """
        text_lower = text.lower()
        topic_scores = {}
        
        # If subject is provided, only check topics from that subject
        subjects_to_check = [subject] if subject else self.topic_keywords.keys()
        
        for subj in subjects_to_check:
            if subj in self.topic_keywords:
                for topic, keywords in self.topic_keywords[subj].items():
                    score = 0
                    for keyword in keywords:
                        # Use regex for whole word matching
                        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                        matches = re.findall(pattern, text_lower)
                        score += len(matches)
                    
                    if score > 0:
                        topic_key = f"{subj}_{topic}" if not subject else topic
                        topic_scores[topic_key] = score
        
        # Normalize scores to percentage
        total_score = sum(topic_scores.values())
        if total_score > 0:
            topic_scores = {k: (v/total_score)*100 for k, v in topic_scores.items()}
        
        return topic_scores
    
    def analyze_difficulty(self, text: str) -> Dict[str, float]:
        """
        Analyze difficulty level of questions
        
        Args:
            text: Extracted text from paper
            
        Returns:
            Dictionary with difficulty distribution
        """
        text_lower = text.lower()
        difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0, 'unknown': 0}
        
        # Split into individual questions
        questions = self._extract_questions(text)
        
        for question in questions:
            q_text = question.lower()
            difficulty = self._classify_question_difficulty(q_text)
            difficulty_counts[difficulty] += 1
        
        # Calculate percentages
        total_questions = sum(difficulty_counts.values())
        if total_questions > 0:
            difficulty_percentages = {
                k: round((v/total_questions)*100, 1) 
                for k, v in difficulty_counts.items()
            }
        else:
            difficulty_percentages = {'easy': 0, 'medium': 0, 'hard': 0, 'unknown': 100}
        
        return difficulty_percentages
    
    def _extract_questions(self, text: str) -> List[str]:
        """
        Extract individual questions from paper text
        
        Args:
            text: Full paper text
            
        Returns:
            List of individual questions
        """
        # Split by question numbers (1., 2., Q1, etc.)
        pattern = r'\n\s*(?:\d+[\.\)]|Q\d+\s*[\.\)]?|\([a-z]\))\s*'
        questions = re.split(pattern, text)
        
        # Remove empty strings and clean
        questions = [q.strip() for q in questions if q.strip()]
        
        # If no questions found with pattern, split by newlines
        if len(questions) <= 1:
            questions = [q.strip() for q in text.split('\n') if q.strip() and len(q.strip()) > 10]
        
        return questions[:20]  # Limit to first 20 questions
    
    def _classify_question_difficulty(self, question_text: str) -> str:
        """
        Classify question difficulty based on keywords
        
        Args:
            question_text: Text of a single question
            
        Returns:
            Difficulty level (easy, medium, hard, unknown)
        """
        # Check for hard keywords first
        for keyword in self.difficulty_indicators['hard']:
            if keyword in question_text:
                return 'hard'
        
        # Check for medium keywords
        for keyword in self.difficulty_indicators['medium']:
            if keyword in question_text:
                return 'medium'
        
        # Check for easy keywords
        for keyword in self.difficulty_indicators['easy']:
            if keyword in question_text:
                return 'easy'
        
        # Check for marks indicator
        marks_pattern = r'\((\d+)\s*marks?\)'
        marks_match = re.search(marks_pattern, question_text)
        if marks_match:
            marks = int(marks_match.group(1))
            if marks >= 8:
                return 'hard'
            elif marks >= 5:
                return 'medium'
            else:
                return 'easy'
        
        return 'unknown'
    
    def analyze_question_types(self, text: str) -> Dict[str, float]:
        """
        Analyze distribution of question types
        
        Args:
            text: Extracted text from paper
            
        Returns:
            Dictionary with question type distribution
        """
        text_lower = text.lower()
        type_counts = {'mcq': 0, 'numerical': 0, 'derivation': 0, 'explanation': 0, 'other': 0}
        
        questions = self._extract_questions(text)
        
        for question in questions:
            q_text = question.lower()
            detected_types = []
            
            # Check for MCQ indicators
            for indicator in self.question_types['mcq']:
                if indicator in q_text:
                    detected_types.append('mcq')
                    break
            
            # Check for numerical indicators
            for indicator in self.question_types['numerical']:
                if indicator in q_text:
                    detected_types.append('numerical')
                    break
            
            # Check for derivation indicators
            for indicator in self.question_types['derivation']:
                if indicator in q_text:
                    detected_types.append('derivation')
                    break
            
            # Check for explanation indicators
            for indicator in self.question_types['explanation']:
                if indicator in q_text:
                    detected_types.append('explanation')
                    break
            
            if detected_types:
                # Assign the first detected type
                type_counts[detected_types[0]] += 1
            else:
                type_counts['other'] += 1
        
        # Calculate percentages
        total_questions = sum(type_counts.values())
        if total_questions > 0:
            type_percentages = {
                k: round((v/total_questions)*100, 1) 
                for k, v in type_counts.items()
            }
        else:
            type_percentages = {k: 0 for k in type_counts.keys()}
        
        return type_percentages
    
    def calculate_expected_score(self, topic_distribution: Dict[str, float], 
                               student_mastery: Dict[str, float]) -> Tuple[float, float, float]:
        """
        Calculate expected score based on student's mastery
        
        Args:
            topic_distribution: Topic distribution from paper
            student_mastery: Student's mastery scores for topics
            
        Returns:
            Tuple of (expected_score, min_score, max_score)
        """
        expected_score = 50  # Default base score
        min_score = 30
        max_score = 70
        
        if not topic_distribution or not student_mastery:
            return expected_score, min_score, max_score
        
        # Normalize topic distribution
        total_weight = sum(topic_distribution.values())
        if total_weight == 0:
            return expected_score, min_score, max_score
        
        normalized_distribution = {
            k: v/total_weight for k, v in topic_distribution.items()
        }
        
        # Calculate weighted mastery
        weighted_mastery = 0
        matched_topics = 0
        
        for topic, weight in normalized_distribution.items():
            # Try to find matching topic in student mastery
            matching_keys = [k for k in student_mastery.keys() if topic in k.lower() or k.lower() in topic]
            
            if matching_keys:
                # Use the first matching topic
                student_score = student_mastery[matching_keys[0]]
                weighted_mastery += student_score * weight
                matched_topics += weight
        
        if matched_topics > 0:
            # Adjust expected score based on weighted mastery
            base_score = weighted_mastery / matched_topics
            expected_score = base_score
            
            # Add some randomness and adjustment factors
            consistency = self.student_data.get('consistency_score', 0.7)
            time_factor = self.student_data.get('time_management', 0.8)
            
            adjusted_score = expected_score * consistency * time_factor
            
            # Add bonus for preparation time
            preparation_days = self.student_data.get('preparation_days', 7)
            if preparation_days >= 14:
                adjusted_score += 10
            elif preparation_days >= 7:
                adjusted_score += 5
            
            expected_score = min(95, max(5, adjusted_score))
            
            # Calculate min and max scores
            confidence = self.student_data.get('confidence_level', 0.8)
            variation = 20 * (1 - confidence)
            
            min_score = max(0, expected_score - variation)
            max_score = min(100, expected_score + variation)
        
        return round(expected_score, 1), round(min_score, 1), round(max_score, 1)
    
    def generate_study_recommendations(self, topic_distribution: Dict[str, float],
                                      student_mastery: Dict[str, float],
                                      paper_difficulty: Dict[str, float]) -> List[Dict]:
        """
        Generate personalized study recommendations
        
        Args:
            topic_distribution: Topic distribution from paper
            student_mastery: Student's mastery scores
            paper_difficulty: Difficulty analysis of paper
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        if not topic_distribution:
            return recommendations
        
        # Sort topics by weight in paper
        sorted_topics = sorted(topic_distribution.items(), key=lambda x: x[1], reverse=True)
        
        for topic, weight in sorted_topics[:5]:  # Top 5 topics
            # Extract subject and topic name
            parts = topic.split('_')
            if len(parts) >= 2:
                subject = parts[0]
                topic_name = ' '.join(parts[1:]).title()
            else:
                subject = 'General'
                topic_name = topic.title()
            
            # Find student's mastery for this topic
            student_score = 50  # Default
            for mastery_topic, score in student_mastery.items():
                if topic in mastery_topic.lower() or mastery_topic.lower() in topic:
                    student_score = score
                    break
            
            # Determine priority
            if student_score < 40:
                priority = 'high'
            elif student_score < 60:
                priority = 'medium'
            else:
                priority = 'low'
            
            # Generate recommendation
            recommendation = {
                'topic': topic_name,
                'subject': subject,
                'weight_in_paper': round(weight, 1),
                'current_mastery': round(student_score, 1),
                'priority': priority,
                'recommended_time': self._calculate_study_time(weight, student_score),
                'resources': self._suggest_resources(topic_name, subject, student_score),
                'action_items': self._generate_action_items(topic_name, student_score)
            }
            
            recommendations.append(recommendation)
        
        # Add general recommendations based on paper difficulty
        hard_percentage = paper_difficulty.get('hard', 0)
        if hard_percentage > 30:
            recommendations.append({
                'topic': 'Exam Strategy',
                'subject': 'General',
                'weight_in_paper': 0,
                'current_mastery': 0,
                'priority': 'medium',
                'recommended_time': '2 hours',
                'resources': ['Time management techniques', 'Question selection strategy'],
                'action_items': ['Practice time-bound tests', 'Learn to identify easy questions first']
            })
        
        return recommendations
    
    def _calculate_study_time(self, weight: float, mastery: float) -> str:
        """Calculate recommended study time for a topic"""
        base_time = weight * 2  # 2 hours per 100% weight
        
        # Adjust based on mastery
        if mastery < 40:
            adjustment = 1.5  # Need more time
        elif mastery < 60:
            adjustment = 1.2
        else:
            adjustment = 0.8  # Need less time
        
        total_hours = base_time * adjustment
        total_minutes = int(total_hours * 60)
        
        if total_minutes >= 120:
            return f"{total_minutes//60} hours"
        else:
            return f"{total_minutes} minutes"
    
    def _suggest_resources(self, topic: str, subject: str, mastery: float) -> List[str]:
        """Suggest learning resources based on topic and mastery"""
        resources = []
        
        # Base resources
        resources.append(f"Video: {topic} concepts explained")
        resources.append(f"Notes: {topic} formula sheet")
        
        # Additional resources based on mastery
        if mastery < 40:
            resources.append(f"Basic practice: 10 simple problems on {topic}")
            resources.append(f"Concept revision: Fundamentals of {topic}")
        elif mastery < 60:
            resources.append(f"Intermediate practice: 15 problems on {topic}")
            resources.append(f"Previous year questions on {topic}")
        else:
            resources.append(f"Advanced practice: Challenging problems on {topic}")
            resources.append(f"Mock test focusing on {topic}")
        
        return resources
    
    def _generate_action_items(self, topic: str, mastery: float) -> List[str]:
        """Generate specific action items for studying"""
        actions = []
        
        if mastery < 40:
            actions.append(f"Watch 20-minute video on {topic}")
            actions.append(f"Solve 5 basic problems on {topic}")
            actions.append(f"Create summary notes for {topic}")
        elif mastery < 60:
            actions.append(f"Review key concepts of {topic}")
            actions.append(f"Solve 10 mixed difficulty problems")
            actions.append(f"Analyze common mistakes in {topic}")
        else:
            actions.append(f"Solve 5 challenging problems on {topic}")
            actions.append(f"Teach {topic} to a peer")
            actions.append(f"Create mind map for {topic}")
        
        return actions
    
    def analyze_complete_paper(self, pdf_path: str, student_id: str = None, 
                             student_mastery: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Complete analysis of uploaded question paper
        
        Args:
            pdf_path: Path to PDF file
            student_id: Optional student ID for personalized analysis
            student_mastery: Optional student mastery data
            
        Returns:
            Comprehensive analysis dictionary
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        # Identify subject (try to detect from text)
        subject = self._detect_subject(text)
        
        # Perform analyses
        topic_distribution = self.identify_topics(text, subject)
        difficulty_analysis = self.analyze_difficulty(text)
        question_type_analysis = self.analyze_question_types(text)
        
        # Calculate expected score if student data is available
        expected_score = None
        min_score = None
        max_score = None
        
        if student_mastery:
            expected_score, min_score, max_score = self.calculate_expected_score(
                topic_distribution, student_mastery
            )
        
        # Generate recommendations
        recommendations = self.generate_study_recommendations(
            topic_distribution, student_mastery or {}, difficulty_analysis
        )
        
        # Compile analysis
        analysis = {
            'metadata': {
                'subject': subject,
                'total_questions_estimated': len(self._extract_questions(text)),
                'analysis_timestamp': datetime.now().isoformat(),
                'paper_difficulty_overall': self._calculate_overall_difficulty(difficulty_analysis)
            },
            'topic_distribution': topic_distribution,
            'difficulty_analysis': difficulty_analysis,
            'question_type_analysis': question_type_analysis,
            'score_prediction': {
                'expected_score': expected_score,
                'score_range': [min_score, max_score] if min_score and max_score else None,
                'confidence': self._calculate_confidence(topic_distribution, student_mastery)
            },
            'recommendations': recommendations,
            'key_insights': self._generate_key_insights(
                topic_distribution, difficulty_analysis, recommendations
            ),
            'study_plan': self._generate_study_plan(recommendations)
        }
        
        return analysis
    
    def _detect_subject(self, text: str) -> str:
        """Detect subject from paper text"""
        text_lower = text.lower()
        
        for subject in self.topic_keywords.keys():
            if subject.lower() in text_lower:
                return subject
        
        # Check for common subject indicators
        if any(word in text_lower for word in ['physics', 'thermodynamics', 'optics', 'mechanics']):
            return 'Physics'
        elif any(word in text_lower for word in ['mathematics', 'calculus', 'algebra', 'geometry']):
            return 'Mathematics'
        elif any(word in text_lower for word in ['chemistry', 'organic', 'inorganic', 'physical']):
            return 'Chemistry'
        
        return 'General'
    
    def _calculate_overall_difficulty(self, difficulty_analysis: Dict[str, float]) -> str:
        """Calculate overall difficulty level"""
        hard_weight = difficulty_analysis.get('hard', 0)
        medium_weight = difficulty_analysis.get('medium', 0)
        
        if hard_weight > 40:
            return 'Hard'
        elif hard_weight > 20 or medium_weight > 50:
            return 'Medium'
        else:
            return 'Easy'
    
    def _calculate_confidence(self, topic_distribution: Dict, student_mastery: Dict) -> float:
        """Calculate confidence score for predictions"""
        if not student_mastery:
            return 0.5  # Default confidence
        
        # Calculate topic coverage
        total_topics = len(topic_distribution)
        if total_topics == 0:
            return 0.5
        
        matched_topics = 0
        for paper_topic in topic_distribution.keys():
            for student_topic in student_mastery.keys():
                if paper_topic in student_topic.lower() or student_topic.lower() in paper_topic:
                    matched_topics += 1
                    break
        
        coverage = matched_topics / total_topics
        
        # Calculate data completeness
        completeness = min(1.0, len(student_mastery) / 10)  # Assume 10 topics is good coverage
        
        confidence = (coverage * 0.6) + (completeness * 0.4)
        
        return round(confidence, 2)
    
    def _generate_key_insights(self, topic_distribution: Dict, 
                              difficulty_analysis: Dict, 
                              recommendations: List) -> List[str]:
        """Generate key insights from analysis"""
        insights = []
        
        # Topic distribution insights
        if topic_distribution:
            top_topic = max(topic_distribution.items(), key=lambda x: x[1])[0]
            insights.append(f"Most important topic: {top_topic.replace('_', ' ').title()} "
                          f"({topic_distribution[top_topic]:.1f}% weightage)")
        
        # Difficulty insights
        hard_percent = difficulty_analysis.get('hard', 0)
        if hard_percent > 30:
            insights.append(f"Paper is challenging with {hard_percent:.1f}% difficult questions")
        elif hard_percent < 10:
            insights.append("Paper has mostly easy to moderate difficulty questions")
        
        # Recommendation insights
        high_priority = [r for r in recommendations if r['priority'] == 'high']
        if high_priority:
            insights.append(f"Focus on {len(high_priority)} high-priority topics for maximum improvement")
        
        return insights
    
    def _generate_study_plan(self, recommendations: List) -> Dict:
        """Generate a 7-day study plan"""
        study_plan = {
            'total_days': 7,
            'daily_target': '2-3 hours',
            'schedule': []
        }
        
        # Group recommendations by priority
        high_priority = [r for r in recommendations if r['priority'] == 'high']
        medium_priority = [r for r in recommendations if r['priority'] == 'medium']
        low_priority = [r for r in recommendations if r['priority'] == 'low']
        
        # Day 1-2: High priority topics
        if high_priority:
            study_plan['schedule'].append({
                'day': 'Day 1-2',
                'focus': 'High Priority Topics',
                'topics': [r['topic'] for r in high_priority[:2]],
                'activities': ['Concept learning', 'Basic practice', 'Note making']
            })
        
        # Day 3-4: Medium priority topics
        if medium_priority:
            study_plan['schedule'].append({
                'day': 'Day 3-4',
                'focus': 'Medium Priority Topics',
                'topics': [r['topic'] for r in medium_priority[:2]],
                'activities': ['Problem solving', 'Previous year questions', 'Revision']
            })
        
        # Day 5: Mixed practice
        study_plan['schedule'].append({
            'day': 'Day 5',
            'focus': 'Mixed Practice',
            'topics': ['All weak topics'],
            'activities': ['Mock test', 'Time-bound practice', 'Error analysis']
        })
        
        # Day 6: Low priority topics
        if low_priority:
            study_plan['schedule'].append({
                'day': 'Day 6',
                'focus': 'Low Priority Topics',
                'topics': [r['topic'] for r in low_priority[:2]],
                'activities': ['Quick revision', 'Formula review', 'Important questions']
            })
        
        # Day 7: Final revision
        study_plan['schedule'].append({
            'day': 'Day 7',
            'focus': 'Final Revision',
            'topics': ['All important topics'],
            'activities': ['Complete paper solving', 'Time management practice', 'Relaxation']
        })
        
        return study_plan


# Example usage and testing
if __name__ == "__main__":
    # Create analyzer instance
    analyzer = PaperAnalyzer()
    
    # Sample student data (for personalized analysis)
    sample_student_mastery = {
        'physics_thermodynamics': 65,
        'physics_optics': 45,
        'physics_mechanics': 80,
        'mathematics_calculus': 70,
        'mathematics_algebra': 85
    }
    
    # Test with sample paper
    analysis = analyzer.analyze_complete_paper(
        pdf_path="sample_paper.pdf",
        student_mastery=sample_student_mastery
    )
    
    # Print results
    print("=" * 60)
    print("PAPER ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"\nSubject: {analysis['metadata']['subject']}")
    print(f"Overall Difficulty: {analysis['metadata']['paper_difficulty_overall']}")
    
    print("\n📊 TOPIC DISTRIBUTION:")
    for topic, weight in sorted(analysis['topic_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {topic.replace('_', ' ').title():30} {weight:5.1f}%")
    
    print("\n🎯 DIFFICULTY ANALYSIS:")
    for level, percent in analysis['difficulty_analysis'].items():
        print(f"  {level.title():15} {percent:5.1f}%")
    
    if analysis['score_prediction']['expected_score']:
        print("\n📈 SCORE PREDICTION:")
        print(f"  Expected Score: {analysis['score_prediction']['expected_score']}/100")
        print(f"  Score Range: {analysis['score_prediction']['score_range'][0]} - {analysis['score_prediction']['score_range'][1]}")
        print(f"  Confidence: {analysis['score_prediction']['confidence']*100:.0f}%")
    
    print("\n💡 KEY INSIGHTS:")
    for insight in analysis['key_insights'][:3]:
        print(f"  • {insight}")
    
    print("\n📚 STUDY RECOMMENDATIONS (Top 3):")
    for rec in analysis['recommendations'][:3]:
        print(f"\n  Topic: {rec['topic']}")
        print(f"  Priority: {rec['priority'].upper()}")
        print(f"  Current Mastery: {rec['current_mastery']}%")
        print(f"  Recommended Time: {rec['recommended_time']}")
        print(f"  Actions: {', '.join(rec['action_items'][:2])}")
    
    print("\n📅 7-DAY STUDY PLAN:")
    for day in analysis['study_plan']['schedule']:
        print(f"\n  {day['day']}: {day['focus']}")
        print(f"  Topics: {', '.join(day['topics'])}")
        print(f"  Activities: {', '.join(day['activities'])}")