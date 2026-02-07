# Frequently Asked Questions (FAQ)

## Database Setup

### Q: Do I need to run schema.sql when using SQLite?

**A: No! You do NOT need to run schema.sql for SQLite.**

The `schema.sql` file is **only for PostgreSQL**. When using SQLite:
- Tables are created automatically by Flask-SQLAlchemy
- Just run `python populate_db.py` and you're done!
- The database file will be created at `backend/instance/hr_helpdesk.db`

### Q: When do I need to use schema.sql?

**A: Only when setting up PostgreSQL.**

PostgreSQL requires you to:
1. Create the database: `CREATE DATABASE hr_helpdesk;`
2. Run the schema file: `psql -U postgres -d hr_helpdesk -f backend/database/schema.sql`
3. Then optionally populate data: `python populate_db.py`

### Q: What's the difference between SQLite and PostgreSQL?

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Setup** | Automatic - no installation | Requires PostgreSQL server |
| **Use Case** | Development, testing, small apps | Production, large-scale apps |
| **Location** | Single file: `backend/instance/hr_helpdesk.db` | Database server |
| **Performance** | Good for single user | Better for multiple concurrent users |
| **Schema File** | ❌ Not needed | ✅ Required (`schema.sql`) |

### Q: How do I switch from SQLite to PostgreSQL?

Edit your `.env` file:

**From SQLite:**
```env
DATABASE_TYPE=sqlite
DATABASE_NAME=hr_helpdesk
```

**To PostgreSQL:**
```env
DATABASE_TYPE=postgresql
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=hr_helpdesk
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
```

Then restart the backend server.

### Q: Where is my data stored?

- **SQLite**: `backend/instance/hr_helpdesk.db` (single file)
- **PostgreSQL**: On your PostgreSQL server (check with your DBA or connection settings)

### Q: How do I reset my database?

**SQLite:**
```bash
rm backend/instance/hr_helpdesk.db
cd backend
python populate_db.py
```

**PostgreSQL:**
```bash
psql -U postgres -d hr_helpdesk -f backend/database/schema.sql
cd backend
python populate_db.py
```

## Running the Application

### Q: What do I run to start the application?

**Quick Start (Automated):**
- Linux/Mac: `./start.sh`
- Windows: Double-click `start.bat`

**Manual Start:**

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
python -m http.server 8080
```

Then visit: http://localhost:8080/dashboard.html

### Q: I get "Failed to fetch" error when submitting tickets

This means the backend server is not running. Make sure:
1. The backend is running: `cd backend && python app.py`
2. You can access http://localhost:5000/
3. Both backend (port 5000) and frontend (port 8080) are running

See the error message on the page for detailed instructions.

### Q: How do I view my tickets and data?

**Option 1: Web Interface**
- Visit http://localhost:8080/dashboard.html

**Option 2: Database Viewer**
- For SQLite: Use [DB Browser for SQLite](https://sqlitebrowser.org/)
- For PostgreSQL: Use [pgAdmin](https://www.pgadmin.org/)

**Option 3: Command Line**
```bash
python view_database.py stats
python view_database.py tickets
python view_database.py ticket 1
```

See [DATABASE.md](DATABASE.md) for more options.

## Development

### Q: Can I use this in production?

Yes, but:
- Use PostgreSQL instead of SQLite
- Set `FLASK_ENV=production` in `.env`
- Use a production WSGI server (not `python app.py`)
- Set a strong `SECRET_KEY`
- Configure proper database backups

### Q: How do I add more sample tickets?

Edit `backend/populate_db.py` and add more entries to the `tickets_data` list, then run:
```bash
cd backend
python populate_db.py
```

### Q: The ports 5000 or 8080 are already in use

**Find what's using the port:**
- Linux/Mac: `lsof -ti:5000` or `lsof -ti:8080`
- Windows: `netstat -ano | findstr :5000`

**Stop the process or change ports:**
- Backend: Edit `backend/app.py` (change port 5000)
- Frontend: Use `python -m http.server 8081` (different port)
- Update `frontend/js/app.js` API_BASE_URL if you change backend port

## Troubleshooting

### Q: "ModuleNotFoundError: No module named 'flask'"

Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Q: Can't find the database file

For SQLite, the database is created in `backend/instance/hr_helpdesk.db` when you:
1. Run `python app.py` (creates empty tables)
2. Or run `python populate_db.py` (creates tables with sample data)

If the directory doesn't exist, Flask creates it automatically.

### Q: Database is locked

SQLite locks the database when it's being accessed. To fix:
1. Stop the backend server (`Ctrl+C`)
2. Close any database browser tools
3. Try again

### Q: I want to contribute

Great! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) if available.

## Support

For more help:
- Read [README.md](README.md) - Main documentation
- Read [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- Read [DATABASE.md](DATABASE.md) - Database details
- Check existing [GitHub Issues](https://github.com/Jowyboss/HR-Help/issues)
- Open a new issue if you find a bug
