#!/usr/bin/env python3
"""
Simple script to view HR Help Desk database contents
Works with both SQLite and PostgreSQL
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

try:
    from app import app, db
    from models import Ticket, Comment
except ImportError as e:
    print(f"Error: {e}")
    print("\nPlease make sure you're in the HR-Help directory and have installed dependencies:")
    print("  cd backend && pip install -r requirements.txt")
    sys.exit(1)


def print_separator(title=""):
    """Print a nice separator"""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}")
    else:
        print(f"{'='*70}")


def view_tickets():
    """Display all tickets"""
    print_separator("TICKETS")
    
    with app.app_context():
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
        
        if not tickets:
            print("No tickets found in database.")
            return
        
        print(f"\nTotal tickets: {len(tickets)}\n")
        
        for ticket in tickets:
            print(f"ID: {ticket.id}")
            print(f"  Employee: {ticket.employee_name} ({ticket.employee_email})")
            print(f"  Subject: {ticket.subject}")
            print(f"  Category: {ticket.category} | Priority: {ticket.priority} | Status: {ticket.status}")
            print(f"  Assigned to: {ticket.assigned_to or 'Unassigned'}")
            print(f"  Created: {ticket.created_at}")
            print(f"  Description: {ticket.description[:100]}{'...' if len(ticket.description) > 100 else ''}")
            
            # Count comments
            comment_count = Comment.query.filter_by(ticket_id=ticket.id).count()
            print(f"  Comments: {comment_count}")
            print()


def view_comments():
    """Display all comments"""
    print_separator("COMMENTS")
    
    with app.app_context():
        comments = Comment.query.order_by(Comment.created_at.desc()).all()
        
        if not comments:
            print("No comments found in database.")
            return
        
        print(f"\nTotal comments: {len(comments)}\n")
        
        for comment in comments:
            # Get ticket subject
            ticket = Ticket.query.get(comment.ticket_id)
            ticket_subject = ticket.subject if ticket else "Unknown"
            
            print(f"ID: {comment.id} | Ticket #{comment.ticket_id}: {ticket_subject}")
            print(f"  Author: {comment.author}")
            print(f"  Date: {comment.created_at}")
            print(f"  Comment: {comment.comment_text}")
            print()


def view_stats():
    """Display database statistics"""
    print_separator("STATISTICS")
    
    with app.app_context():
        total_tickets = Ticket.query.count()
        total_comments = Comment.query.count()
        
        print(f"\nTotal Tickets: {total_tickets}")
        print(f"Total Comments: {total_comments}")
        
        # Tickets by status
        print("\nTickets by Status:")
        for status in ['Open', 'In Progress', 'Resolved', 'Closed']:
            count = Ticket.query.filter_by(status=status).count()
            print(f"  {status}: {count}")
        
        # Tickets by priority
        print("\nTickets by Priority:")
        for priority in ['Low', 'Medium', 'High', 'Urgent']:
            count = Ticket.query.filter_by(priority=priority).count()
            print(f"  {priority}: {count}")
        
        # Tickets by category
        print("\nTickets by Category:")
        for category in ['Benefits', 'Payroll', 'Time Off', 'Onboarding', 'General']:
            count = Ticket.query.filter_by(category=category).count()
            print(f"  {category}: {count}")
        
        print()


def view_ticket_detail(ticket_id):
    """Display detailed information about a specific ticket"""
    print_separator(f"TICKET DETAIL - #{ticket_id}")
    
    with app.app_context():
        ticket = Ticket.query.get(ticket_id)
        
        if not ticket:
            print(f"Ticket #{ticket_id} not found.")
            return
        
        print(f"\nID: {ticket.id}")
        print(f"Employee: {ticket.employee_name}")
        print(f"Email: {ticket.employee_email}")
        print(f"Category: {ticket.category}")
        print(f"Priority: {ticket.priority}")
        print(f"Status: {ticket.status}")
        print(f"Subject: {ticket.subject}")
        print(f"Description: {ticket.description}")
        print(f"Assigned to: {ticket.assigned_to or 'Unassigned'}")
        print(f"Created: {ticket.created_at}")
        print(f"Updated: {ticket.updated_at}")
        
        # Show comments
        comments = Comment.query.filter_by(ticket_id=ticket_id).order_by(Comment.created_at.asc()).all()
        print(f"\nComments ({len(comments)}):")
        
        if comments:
            for i, comment in enumerate(comments, 1):
                print(f"\n  Comment #{i}:")
                print(f"    Author: {comment.author}")
                print(f"    Date: {comment.created_at}")
                print(f"    Text: {comment.comment_text}")
        else:
            print("  No comments yet.")
        
        print()


def main():
    """Main function"""
    print_separator("HR HELP DESK - DATABASE VIEWER")
    
    # Check database connection
    with app.app_context():
        db_type = "SQLite" if "sqlite" in app.config['SQLALCHEMY_DATABASE_URI'] else "PostgreSQL"
        print(f"\nDatabase Type: {db_type}")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'tickets':
            view_tickets()
        elif command == 'comments':
            view_comments()
        elif command == 'stats':
            view_stats()
        elif command == 'ticket' and len(sys.argv) > 2:
            try:
                ticket_id = int(sys.argv[2])
                view_ticket_detail(ticket_id)
            except ValueError:
                print("Error: Ticket ID must be a number")
        else:
            print(f"\nUnknown command: {command}")
            show_help()
    else:
        # Default: show everything
        view_stats()
        view_tickets()
        view_comments()
    
    print_separator()


def show_help():
    """Show help message"""
    print("\nUsage:")
    print("  python view_database.py              # Show everything")
    print("  python view_database.py stats        # Show statistics only")
    print("  python view_database.py tickets      # Show all tickets")
    print("  python view_database.py comments     # Show all comments")
    print("  python view_database.py ticket <id>  # Show specific ticket with comments")
    print("\nExamples:")
    print("  python view_database.py stats")
    print("  python view_database.py ticket 1")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
