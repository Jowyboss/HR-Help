# HR Help Desk Web Application

A complete HR help desk web application for HR employees to manage employee requests and tickets.

## 🚀 Quick Start (SQLite - Easiest Setup)

Want to run the app quickly without PostgreSQL? Use the automated startup scripts:

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

The script will automatically:
1. Install Python dependencies
2. Configure SQLite database
3. Create sample tickets
4. Start both backend and frontend servers

### Option 2: Manual Setup

```bash
# 1. Install Python dependencies
cd backend
pip install -r requirements.txt

# 2. Set up environment for SQLite
cat > ../.env << 'EOF'
SECRET_KEY=dev-secret-key
DATABASE_TYPE=sqlite
DATABASE_NAME=hr_helpdesk
FLASK_ENV=development
EOF

# 3. Create sample data
python populate_db.py

# 4. Start the backend server (in one terminal)
python app.py

# 5. In a NEW terminal, start the frontend server
cd ../frontend
python -m http.server 8080
```

**Open your browser:**
- 📝 Submit tickets: http://localhost:8080/index.html
- 📊 View dashboard: http://localhost:8080/dashboard.html

That's it! You now have a fully functional HR Help Desk system running locally.

---

## Features

- 📝 **Ticket Management**: Submit, view, update, and manage help desk tickets
- 📊 **Dashboard**: View all tickets with filtering, sorting, and search capabilities
- 💬 **Comments**: Add comments and updates to tickets
- 🏷️ **Categories**: Organize tickets by Benefits, Payroll, Time Off, Onboarding, and General
- ⚡ **Priority Levels**: Track tickets by Low, Medium, High, and Urgent priorities
- 📈 **Statistics**: View ticket counts by status, priority, and category
- 👥 **Assignment**: Assign tickets to HR staff members

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask framework
- **Database**: PostgreSQL (production) or SQLite (development)
- **API**: RESTful API with JSON responses

## Project Structure

```
hr-helpdesk/
├── backend/
│   ├── app.py              # Flask application and API endpoints
│   ├── models.py           # Database models (Ticket, Comment)
│   ├── config.py           # Application configuration
│   ├── requirements.txt    # Python dependencies
│   └── database/
│       └── schema.sql      # Database schema and sample data
├── frontend/
│   ├── index.html          # Submit ticket page
│   ├── dashboard.html      # Dashboard page
│   ├── ticket-detail.html  # Ticket detail page
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       └── app.js          # JavaScript API client
├── .gitignore
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Jowyboss/HR-Help.git
cd HR-Help
```

### 2. Set Up PostgreSQL Database

Create a new PostgreSQL database:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE hr_helpdesk;

# Exit psql
\q
```

Initialize the database schema:

```bash
psql -U postgres -d hr_helpdesk -f backend/database/schema.sql
```

### 3. Configure Environment Variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit `.env` and set your database credentials:

```
SECRET_KEY=your-secret-key-here
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=hr_helpdesk
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
```

### 4. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Run the Application

Start the Flask backend server:

```bash
python app.py
```

The API server will start at `http://localhost:5000`

### 6. Access the Frontend

Open the frontend in your browser:

1. Submit Ticket: `frontend/index.html`
2. Dashboard: `frontend/dashboard.html`

**Note**: For local development, you may need to serve the frontend files through a local web server to avoid CORS issues. You can use Python's built-in HTTP server:

```bash
cd frontend
python -m http.server 8080
```

Then access:
- Submit Ticket: `http://localhost:8080/index.html`
- Dashboard: `http://localhost:8080/dashboard.html`

## API Endpoints

### Tickets

- `GET /api/tickets` - Get all tickets (with optional filters)
  - Query parameters: `status`, `category`, `priority`, `assigned_to`, `search`, `sort_by`, `sort_order`
- `GET /api/tickets/<id>` - Get a specific ticket by ID
- `POST /api/tickets` - Create a new ticket
- `PUT /api/tickets/<id>` - Update a ticket
- `DELETE /api/tickets/<id>` - Delete a ticket

### Comments

- `GET /api/tickets/<id>/comments` - Get all comments for a ticket
- `POST /api/tickets/<id>/comments` - Add a comment to a ticket

### Statistics

- `GET /api/stats` - Get ticket statistics

## Usage

### Submit a New Ticket

1. Navigate to the Submit Ticket page
2. Fill in the required information:
   - Name and email
   - Category (Benefits, Payroll, Time Off, Onboarding, General)
   - Priority (Low, Medium, High, Urgent)
   - Subject and description
3. Click "Submit Ticket"

### View and Manage Tickets

1. Navigate to the Dashboard page
2. Use filters to narrow down tickets:
   - Filter by status, category, priority
   - Search by keywords
   - Sort by date, priority, or status
3. Click "View" to see ticket details

### Update Ticket Status

1. Open a ticket from the dashboard
2. Update the status or assign to an HR staff member
3. Click "Update Ticket"

### Add Comments

1. Open a ticket from the dashboard
2. Scroll to the Comments section
3. Enter your name and comment
4. Click "Add Comment"

## Database Schema

### Tickets Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| employee_name | VARCHAR(255) | Employee name |
| employee_email | VARCHAR(255) | Employee email |
| category | VARCHAR(50) | Ticket category |
| priority | VARCHAR(20) | Priority level |
| subject | VARCHAR(255) | Ticket subject |
| description | TEXT | Ticket description |
| status | VARCHAR(20) | Current status (default: 'Open') |
| assigned_to | VARCHAR(255) | Assigned HR staff (nullable) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Comments Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| ticket_id | INTEGER | Foreign key to tickets |
| author | VARCHAR(255) | Comment author |
| comment_text | TEXT | Comment content |
| created_at | TIMESTAMP | Creation timestamp |

## Development

### Adding New Features

1. **Backend**: Add new endpoints in `backend/app.py`
2. **Frontend**: Update HTML templates and JavaScript in `frontend/`
3. **Database**: Modify schema in `backend/database/schema.sql`
4. **Models**: Update data models in `backend/models.py`

### Running Tests

```bash
# Coming soon: Add test suite
```

## Troubleshooting

### CORS Issues

If you encounter CORS issues when accessing the API from the frontend, ensure:
1. Flask-CORS is properly installed
2. The backend is running on `http://localhost:5000`
3. The frontend is served from a web server (not opened directly as a file)

### Database Connection Issues

If you can't connect to the database:
1. Verify PostgreSQL is running
2. Check your `.env` file has correct credentials
3. Ensure the database exists and schema is loaded

### Port Already in Use

If port 5000 or 8080 is already in use:
1. Stop the process using that port
2. Or modify the port in `backend/app.py` and `frontend/js/app.js`

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.