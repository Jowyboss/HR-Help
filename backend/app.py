from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from config import Config
from models import db, Ticket, Comment

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'HR Help Desk API',
        'version': '1.0.0',
        'endpoints': {
            'tickets': '/api/tickets',
            'ticket_detail': '/api/tickets/<id>',
            'comments': '/api/tickets/<id>/comments',
            'stats': '/api/stats'
        }
    })

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets with optional filters"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        category = request.args.get('category')
        priority = request.args.get('priority')
        assigned_to = request.args.get('assigned_to')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = Ticket.query
        
        # Apply filters
        if status:
            query = query.filter(Ticket.status == status)
        if category:
            query = query.filter(Ticket.category == category)
        if priority:
            query = query.filter(Ticket.priority == priority)
        if assigned_to:
            query = query.filter(Ticket.assigned_to == assigned_to)
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    Ticket.subject.ilike(search_pattern),
                    Ticket.description.ilike(search_pattern),
                    Ticket.employee_name.ilike(search_pattern)
                )
            )
        
        # Apply sorting
        if sort_order == 'desc':
            query = query.order_by(db.desc(getattr(Ticket, sort_by, Ticket.created_at)))
        else:
            query = query.order_by(db.asc(getattr(Ticket, sort_by, Ticket.created_at)))
        
        tickets = query.all()
        
        return jsonify({
            'success': True,
            'count': len(tickets),
            'tickets': [ticket.to_dict() for ticket in tickets]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket by ID"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        ticket_dict = ticket.to_dict()
        ticket_dict['comments'] = [comment.to_dict() for comment in ticket.comments]
        
        return jsonify({
            'success': True,
            'ticket': ticket_dict
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Create a new ticket"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['employee_name', 'employee_email', 'category', 'priority', 'subject', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create new ticket
        ticket = Ticket(
            employee_name=data['employee_name'],
            employee_email=data['employee_email'],
            category=data['category'],
            priority=data['priority'],
            subject=data['subject'],
            description=data['description'],
            status=data.get('status', 'Open'),
            assigned_to=data.get('assigned_to')
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ticket created successfully',
            'ticket': ticket.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """Update an existing ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['status', 'assigned_to', 'category', 'priority', 'subject', 'description']
        for field in allowed_fields:
            if field in data:
                setattr(ticket, field, data[field])
        
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ticket updated successfully',
            'ticket': ticket.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """Delete a ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ticket deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tickets/<int:ticket_id>/comments', methods=['GET'])
def get_comments(ticket_id):
    """Get all comments for a ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        comments = Comment.query.filter_by(ticket_id=ticket_id).order_by(Comment.created_at.asc()).all()
        
        return jsonify({
            'success': True,
            'count': len(comments),
            'comments': [comment.to_dict() for comment in comments]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tickets/<int:ticket_id>/comments', methods=['POST'])
def add_comment(ticket_id):
    """Add a comment to a ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.get_json()
        
        # Validate required fields
        if 'author' not in data or 'comment_text' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: author and comment_text'
            }), 400
        
        # Create new comment
        comment = Comment(
            ticket_id=ticket_id,
            author=data['author'],
            comment_text=data['comment_text']
        )
        
        # Update ticket's updated_at timestamp
        ticket.updated_at = datetime.utcnow()
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment added successfully',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about tickets"""
    try:
        stats = {
            'total_tickets': Ticket.query.count(),
            'by_status': {
                'open': Ticket.query.filter_by(status='Open').count(),
                'in_progress': Ticket.query.filter_by(status='In Progress').count(),
                'resolved': Ticket.query.filter_by(status='Resolved').count(),
                'closed': Ticket.query.filter_by(status='Closed').count()
            },
            'by_priority': {
                'low': Ticket.query.filter_by(priority='Low').count(),
                'medium': Ticket.query.filter_by(priority='Medium').count(),
                'high': Ticket.query.filter_by(priority='High').count(),
                'urgent': Ticket.query.filter_by(priority='Urgent').count()
            },
            'by_category': {
                'benefits': Ticket.query.filter_by(category='Benefits').count(),
                'payroll': Ticket.query.filter_by(category='Payroll').count(),
                'time_off': Ticket.query.filter_by(category='Time Off').count(),
                'onboarding': Ticket.query.filter_by(category='Onboarding').count(),
                'general': Ticket.query.filter_by(category='General').count()
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
