# Database Guide - HR Help Desk

## Where is the Database Stored?

The application supports two database types:

### 1. SQLite (Default for Development)
- **Location**: `backend/instance/hr_helpdesk.db`
- **Type**: Single file database
- **When configured**: When `.env` has `DATABASE_TYPE=sqlite`

### 2. PostgreSQL (Recommended for Production)
- **Location**: PostgreSQL server (not a file)
- **Type**: Client-server database
- **When configured**: When `.env` has `DATABASE_TYPE=postgresql`

## How to View the Database

### Option 1: Using SQLite Browser (Recommended for Beginners)

**DB Browser for SQLite** is a free, open-source visual tool:

1. **Download and Install**:
   - Website: https://sqlitebrowser.org/
   - Available for Windows, Mac, and Linux

2. **Open the Database**:
   - Launch DB Browser for SQLite
   - Click "Open Database"
   - Navigate to: `backend/instance/hr_helpdesk.db`
   - Browse tables: `tickets` and `comments`

### Option 2: Using Command Line (SQLite)

```bash
# Navigate to backend directory
cd backend/instance

# Open SQLite shell
sqlite3 hr_helpdesk.db

# SQLite commands:
.tables                    # List all tables
.schema tickets           # Show tickets table structure
.schema comments          # Show comments table structure

SELECT * FROM tickets;    # View all tickets
SELECT * FROM comments;   # View all comments

# Exit
.quit
```

### Option 3: Using Python Script

Create a simple Python script to view data:

```python
# view_db.py
import sqlite3
import json

# Connect to database
conn = sqlite3.connect('backend/instance/hr_helpdesk.db')
cursor = conn.cursor()

# View all tickets
print("=== TICKETS ===")
cursor.execute("SELECT * FROM tickets")
tickets = cursor.fetchall()
for ticket in tickets:
    print(ticket)

print("\n=== COMMENTS ===")
cursor.execute("SELECT * FROM comments")
comments = cursor.fetchall()
for comment in comments:
    print(comment)

conn.close()
```

Run it:
```bash
python view_db.py
```

### Option 4: Using DBeaver (Universal Database Tool)

DBeaver works with both SQLite and PostgreSQL:

1. **Download**: https://dbeaver.io/download/
2. **For SQLite**:
   - New Connection → SQLite
   - Path: `backend/instance/hr_helpdesk.db`
3. **For PostgreSQL**:
   - New Connection → PostgreSQL
   - Enter your connection details from `.env`

### Option 5: Using pgAdmin (PostgreSQL Only)

If you're using PostgreSQL:

1. **Download**: https://www.pgadmin.org/download/
2. **Connect** using credentials from `.env`:
   - Host: localhost (or from DATABASE_HOST)
   - Port: 5432 (or from DATABASE_PORT)
   - Database: hr_helpdesk (or from DATABASE_NAME)
   - Username/Password: from `.env`

## Quick Database Queries

### View Recent Tickets
```sql
SELECT id, employee_name, subject, status, created_at 
FROM tickets 
ORDER BY created_at DESC 
LIMIT 10;
```

### View Tickets by Status
```sql
SELECT status, COUNT(*) as count 
FROM tickets 
GROUP BY status;
```

### View Tickets with Comments
```sql
SELECT t.id, t.subject, COUNT(c.id) as comment_count
FROM tickets t
LEFT JOIN comments c ON t.id = c.ticket_id
GROUP BY t.id, t.subject;
```

### View All Data for a Specific Ticket
```sql
SELECT * FROM tickets WHERE id = 1;
SELECT * FROM comments WHERE ticket_id = 1;
```

## Database Schema

### Tickets Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| employee_name | VARCHAR(255) | Name of employee |
| employee_email | VARCHAR(255) | Email address |
| category | VARCHAR(50) | Ticket category |
| priority | VARCHAR(20) | Priority level |
| subject | VARCHAR(255) | Ticket subject/title |
| description | TEXT | Detailed description |
| status | VARCHAR(20) | Current status (default: 'Open') |
| assigned_to | VARCHAR(255) | Assigned HR staff (nullable) |
| created_at | TIMESTAMP | When ticket was created |
| updated_at | TIMESTAMP | Last update time |

### Comments Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| ticket_id | INTEGER | Foreign key to tickets table |
| author | VARCHAR(255) | Comment author name |
| comment_text | TEXT | Comment content |
| created_at | TIMESTAMP | When comment was created |

## Backup and Export

### Backup SQLite Database
```bash
# Simple copy
cp backend/instance/hr_helpdesk.db backend/instance/hr_helpdesk_backup.db

# Or export to SQL
sqlite3 backend/instance/hr_helpdesk.db .dump > backup.sql
```

### Export to CSV
```bash
sqlite3 backend/instance/hr_helpdesk.db << EOF
.headers on
.mode csv
.output tickets.csv
SELECT * FROM tickets;
.output comments.csv
SELECT * FROM comments;
.quit
EOF
```

### Restore from Backup
```bash
# From .db file
cp backend/instance/hr_helpdesk_backup.db backend/instance/hr_helpdesk.db

# From SQL dump
sqlite3 backend/instance/hr_helpdesk.db < backup.sql
```

## Switching Between SQLite and PostgreSQL

Edit your `.env` file:

**For SQLite (Development):**
```
DATABASE_TYPE=sqlite
DATABASE_NAME=hr_helpdesk
```

**For PostgreSQL (Production):**
```
DATABASE_TYPE=postgresql
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=hr_helpdesk
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
```

Then restart the backend server.

## Troubleshooting

### Can't Find Database File
- Make sure you've run the application at least once
- Check `backend/instance/hr_helpdesk.db`
- If missing, run: `cd backend && python populate_db.py`

### Permission Denied
```bash
# Fix permissions (Linux/Mac)
chmod 644 backend/instance/hr_helpdesk.db
```

### Database is Locked
- Close all connections to the database
- Stop the Flask backend server
- Try again

### Want to Reset Database
```bash
# Delete the database file
rm backend/instance/hr_helpdesk.db

# Recreate with sample data
cd backend
python populate_db.py
```
