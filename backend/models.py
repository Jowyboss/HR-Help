from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Ticket(db.Model):
    """Ticket model for help desk tickets"""
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(255), nullable=False)
    employee_email = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')
    assigned_to = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with comments
    comments = db.relationship('Comment', backref='ticket', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert ticket object to dictionary"""
        return {
            'id': self.id,
            'employee_name': self.employee_name,
            'employee_email': self.employee_email,
            'category': self.category,
            'priority': self.priority,
            'subject': self.subject,
            'description': self.description,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'comments_count': len(self.comments) if self.comments else 0
        }

class Comment(db.Model):
    """Comment model for ticket comments"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert comment object to dictionary"""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'author': self.author,
            'comment_text': self.comment_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
