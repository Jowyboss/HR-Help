#!/usr/bin/env python
"""Script to populate the database with sample data"""
from app import app, db
from models import Ticket, Comment
from datetime import datetime, timedelta

def populate_database():
    """Populate database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Clear existing data
        Comment.query.delete()
        Ticket.query.delete()
        db.session.commit()
        
        # Create sample tickets
        tickets_data = [
            {
                'employee_name': 'John Doe',
                'employee_email': 'john.doe@company.com',
                'category': 'Benefits',
                'priority': 'High',
                'subject': 'Health Insurance Question',
                'description': 'I need help understanding my health insurance coverage options.',
                'status': 'Open',
                'assigned_to': None,
                'created_at': datetime.utcnow() - timedelta(days=2)
            },
            {
                'employee_name': 'Jane Smith',
                'employee_email': 'jane.smith@company.com',
                'category': 'Payroll',
                'priority': 'Urgent',
                'subject': 'Missing Paycheck',
                'description': 'I did not receive my paycheck for this month.',
                'status': 'In Progress',
                'assigned_to': 'Sarah Johnson',
                'created_at': datetime.utcnow() - timedelta(days=1)
            },
            {
                'employee_name': 'Bob Wilson',
                'employee_email': 'bob.wilson@company.com',
                'category': 'Time Off',
                'priority': 'Medium',
                'subject': 'Vacation Request',
                'description': 'I would like to request time off for next month.',
                'status': 'Open',
                'assigned_to': None,
                'created_at': datetime.utcnow() - timedelta(hours=12)
            },
            {
                'employee_name': 'Alice Brown',
                'employee_email': 'alice.brown@company.com',
                'category': 'Onboarding',
                'priority': 'Low',
                'subject': 'New Hire Documentation',
                'description': 'What documents do I need to submit as a new hire?',
                'status': 'Resolved',
                'assigned_to': 'Mike Davis',
                'created_at': datetime.utcnow() - timedelta(days=5)
            },
            {
                'employee_name': 'Charlie Davis',
                'employee_email': 'charlie.davis@company.com',
                'category': 'General',
                'priority': 'Medium',
                'subject': 'Office Access Card',
                'description': 'My access card is not working properly.',
                'status': 'Open',
                'assigned_to': None,
                'created_at': datetime.utcnow() - timedelta(hours=3)
            }
        ]
        
        tickets = []
        for ticket_data in tickets_data:
            ticket = Ticket(**ticket_data)
            db.session.add(ticket)
            tickets.append(ticket)
        
        db.session.commit()
        
        # Create sample comments
        comments_data = [
            {
                'ticket_id': 2,
                'author': 'Sarah Johnson',
                'comment_text': 'I am investigating this issue with the payroll department.',
                'created_at': datetime.utcnow() - timedelta(hours=20)
            },
            {
                'ticket_id': 2,
                'author': 'Sarah Johnson',
                'comment_text': 'The issue has been identified. Your paycheck will be processed today.',
                'created_at': datetime.utcnow() - timedelta(hours=10)
            },
            {
                'ticket_id': 4,
                'author': 'Mike Davis',
                'comment_text': 'Please submit your ID, social security card, and direct deposit form.',
                'created_at': datetime.utcnow() - timedelta(days=4)
            },
            {
                'ticket_id': 4,
                'author': 'Alice Brown',
                'comment_text': 'Thank you! I have submitted all the documents.',
                'created_at': datetime.utcnow() - timedelta(days=4)
            }
        ]
        
        for comment_data in comments_data:
            comment = Comment(**comment_data)
            db.session.add(comment)
        
        db.session.commit()
        
        print(f"Database populated successfully!")
        print(f"Created {len(tickets)} tickets")
        print(f"Created {len(comments_data)} comments")

if __name__ == '__main__':
    populate_database()
