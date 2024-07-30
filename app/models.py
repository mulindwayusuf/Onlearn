import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# define user role enum
class UserRole(enum.Enum):
    PARENT = 'parent'
    STUDENT = 'student'
    ADMIN = 'admin'

# MODELS
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default= 'static/Yus.jpg')
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    submissions = db.relationship('Submission', backref='student', lazy=True)
    progress = db.relationship('Progress', backref='student', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.role})"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(30), nullable=False)
    topics = db.relationship('Topic', backref='subject', lazy=True)
    
    def __repr__(self):
        return f"Subject('{self.subject_name}', '{self.description}', '{self.level}')"
    
class Topic(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    quizzes = db.relationship('Quiz', backref='topic', lazy=True)
    assignments = db.relationship('Assignment', backref='topic', lazy=True)
    progress = db.relationship('Progress', backref='topic', lazy=True)
    
    def __repr__(self):
        return f"Topic('{self.title}', '{self.content}')"        

class Quiz(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    
    def __repr__(self):
        return f"Quiz('{self.title}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question_text = db.Column(db.Text(), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    options = db.Column(db.JSON)
    correct_answer = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Question('{self.question_text}', '{self.question_type}')"

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    submissions = db.relationship('Submission', backref='assignment', lazy=True)
    
    def __repr__(self):
        return f"Assignment('{self.title}', '{self.description}', '{self.due_date}')"

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.now)
    grade = db.Column(db.String(20))
    feedback = db.Column(db.Text)
    
    def __repr__(self):
        return f"Submission('{self.submitted_at}', '{self.grade}', '{self.feedback}')"

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    criteria = db.Column(db.Text)
    
    def __repr__(self):
        return f"Badge('{self.name}', '{self.description}', '{self.criteria}')"

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    status = db.Column(db.String(29), nullable=False)
    
    def __repr__(self):
        return f"Progress('{self.status}')"
    
    
    
    
    