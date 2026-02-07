# 🚀 Quick Start Guide - HR Help Desk

## The Absolute Easiest Way to Run This App

### For Linux/Mac Users:

Open a terminal and run:

```bash
./start.sh
```

That's it! The script will:
- ✅ Install all dependencies
- ✅ Set up the database with sample data
- ✅ Start the backend server
- ✅ Start the frontend server
- ✅ Open your browser automatically

### For Windows Users:

Just double-click on:

```
start.bat
```

The script will do everything for you!

---

## What URLs Should I Visit?

After the servers start, open these in your browser:

- **📝 Submit a New Ticket**: http://localhost:8080/index.html
- **📊 View Dashboard**: http://localhost:8080/dashboard.html
- **🔧 API Endpoint**: http://localhost:5000/api/tickets

---

## Manual Setup (If Scripts Don't Work)

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Set Up Database
```bash
# Create .env file
cat > ../.env << 'EOF'
SECRET_KEY=dev-secret-key
DATABASE_TYPE=sqlite
DATABASE_NAME=hr_helpdesk
FLASK_ENV=development
EOF

# Populate with sample data
python populate_db.py
```

### Step 3: Start Backend Server
Open one terminal:
```bash
cd backend
python app.py
```
Leave this running!

### Step 4: Start Frontend Server
Open a SECOND terminal:
```bash
cd frontend
python -m http.server 8080
```
Leave this running too!

### Step 5: Open Your Browser
Visit: http://localhost:8080/dashboard.html

---

## Having Issues?

### "Connection refused" or can't connect?
- Make sure BOTH servers are running (backend AND frontend)
- Check you're using `http://localhost:8080/` not opening files directly

### Not seeing any tickets?
```bash
cd backend
python populate_db.py
```

### Ports already in use?
Close any other programs using port 5000 or 8080, or change the ports in the code.

### Still stuck?
See the full [README.md](README.md) for detailed troubleshooting.

---

## What's Running?

When everything is working, you have:

1. **Backend API Server** (Flask) - Port 5000
   - Handles all data operations
   - Manages tickets, comments, statistics
   
2. **Frontend Web Server** (Python HTTP) - Port 8080
   - Serves the HTML/CSS/JavaScript files
   - Provides the user interface

3. **Database** (SQLite file: `backend/instance/hr_helpdesk.db`)
   - Stores all tickets and comments
   - Pre-loaded with sample data

---

## How to View the Database?

Your data is stored in: `backend/instance/hr_helpdesk.db`

**Option 1: Visual Tool (Easiest)**
- Download [DB Browser for SQLite](https://sqlitebrowser.org/)
- Open the file: `backend/instance/hr_helpdesk.db`
- Browse the `tickets` and `comments` tables

**Option 2: Command Line**
```bash
cd backend/instance
sqlite3 hr_helpdesk.db
SELECT * FROM tickets;
.quit
```

**Option 3: See [DATABASE.md](DATABASE.md)** for complete guide including:
- Different database viewers
- SQL queries to run
- How to export/backup data
- Switching to PostgreSQL

---

## Next Steps

Once you have it running:

1. **Explore the Dashboard** - View all tickets, use filters, and search
2. **Create a Ticket** - Try submitting a new help desk request
3. **View Ticket Details** - Click on any ticket to see details and comments
4. **Update Status** - Change ticket status and assignments
5. **Add Comments** - Add updates and comments to tickets

Enjoy your HR Help Desk system! 🎉
