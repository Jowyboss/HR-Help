# 📊 How to View Your Database Information

## Quick Answer to Your Question

**"How do I view the information added to the database? Do I do it through PostgreSQL, SQLite, or Workbench?"**

### The Answer Depends on Which Database You're Using!

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Check Which Database Type You're Using             │
└─────────────────────────────────────────────────────────────┘

Look at your .env file:
  • DATABASE_TYPE=sqlite      → Use SQLite tools (see below)
  • DATABASE_TYPE=postgresql  → Use PostgreSQL tools (see below)

If you don't have a .env file or used the startup scripts,
you're probably using SQLite (the default).
```

---

## 🔍 Decision Tree: Which Tool Should I Use?

```
Are you using SQLite or PostgreSQL?
│
├─ SQLite (Default for development)
│  │
│  ├─ EASIEST: Python Script (Already included!)
│  │  └─ Run: python view_database.py
│  │     └─ Shows: All tickets, comments, stats
│  │
│  ├─ VISUAL: DB Browser for SQLite ⭐ RECOMMENDED
│  │  └─ Download: https://sqlitebrowser.org/
│  │     └─ Open: backend/instance/hr_helpdesk.db
│  │
│  ├─ COMMAND LINE: sqlite3
│  │  └─ Run: sqlite3 backend/instance/hr_helpdesk.db
│  │
│  └─ UNIVERSAL: DBeaver (works with any database)
│     └─ Download: https://dbeaver.io/
│
└─ PostgreSQL (Production setup)
   │
   ├─ VISUAL: pgAdmin ⭐ RECOMMENDED
   │  └─ Download: https://www.pgadmin.org/
   │
   ├─ COMMAND LINE: psql
   │  └─ Run: psql -U postgres -d hr_helpdesk
   │
   ├─ UNIVERSAL: DBeaver (works with any database)
   │  └─ Download: https://dbeaver.io/
   │
   └─ WORKBENCH: MySQL Workbench (NOT COMPATIBLE)
      └─ ❌ Don't use this - it's for MySQL, not PostgreSQL
```

---

## 🚀 Quickest Way to View Your Data (3 Options)

### Option 1: Use the Built-in Python Script (EASIEST!)

This works for both SQLite AND PostgreSQL!

```bash
# View everything
python view_database.py

# View just statistics
python view_database.py stats

# View all tickets
python view_database.py tickets

# View specific ticket with comments
python view_database.py ticket 5
```

**Example output:**
```
======================================================================
  STATISTICS
======================================================================

Total Tickets: 6
Total Comments: 4

Tickets by Status:
  Open: 4
  In Progress: 1
  Resolved: 1
```

### Option 2: Use Your Web Browser (ALREADY RUNNING!)

If your application is running, you can view tickets at:
- **Dashboard**: http://localhost:8080/dashboard.html
- **Ticket Details**: Click any ticket to see details and comments

### Option 3: Use a Database Viewer Tool

Choose based on your database type:

#### For SQLite (Most Common):

**DB Browser for SQLite** - Free visual tool
1. Download from https://sqlitebrowser.org/
2. Install and open
3. Click "Open Database"
4. Navigate to: `backend/instance/hr_helpdesk.db`
5. Browse the `tickets` and `comments` tables

#### For PostgreSQL:

**pgAdmin** - Official PostgreSQL tool
1. Download from https://www.pgadmin.org/
2. Install and open
3. Add server with your `.env` credentials:
   - Host: localhost (or your DATABASE_HOST)
   - Port: 5432 (or your DATABASE_PORT)
   - Database: hr_helpdesk (or your DATABASE_NAME)
   - Username/Password: from your `.env` file

---

## 📋 Quick Reference Commands

### If Using SQLite:

```bash
# Method 1: Python script (recommended)
python view_database.py

# Method 2: SQLite command line
cd backend/instance
sqlite3 hr_helpdesk.db
.tables
SELECT * FROM tickets;
.quit

# Method 3: Check file location
ls -l backend/instance/hr_helpdesk.db
```

### If Using PostgreSQL:

```bash
# Method 1: Python script (recommended)
python view_database.py

# Method 2: PostgreSQL command line
psql -U postgres -d hr_helpdesk
\dt                    # List tables
SELECT * FROM tickets;
\q                     # Quit
```

---

## ❓ Still Not Sure Which Database You're Using?

Run this command to check:

```bash
cat .env | grep DATABASE_TYPE
```

**Result:**
- `DATABASE_TYPE=sqlite` → You're using SQLite
- `DATABASE_TYPE=postgresql` → You're using PostgreSQL
- No result or file not found → You're likely using SQLite (default)

---

## 🎯 Most Common Scenarios

### Scenario 1: "I just ran start.sh or start.bat"
✅ You're using **SQLite**
- Use: `python view_database.py` or DB Browser for SQLite
- Database file: `backend/instance/hr_helpdesk.db`

### Scenario 2: "I set up PostgreSQL and ran schema.sql"
✅ You're using **PostgreSQL**
- Use: `python view_database.py` or pgAdmin
- Database: PostgreSQL server

### Scenario 3: "I have no idea what I'm using"
✅ You're probably using **SQLite** (the default)
- Try: `python view_database.py`
- If it works, you're using SQLite
- If it fails with connection error, check your `.env` file

---

## 🛠️ Tool Comparison

| Tool | Database Type | Difficulty | Best For |
|------|---------------|------------|----------|
| **view_database.py** | Both | ⭐ Easy | Quick checks, automation |
| **Web Dashboard** | Both | ⭐ Easy | End users, viewing tickets |
| **DB Browser for SQLite** | SQLite only | ⭐⭐ Medium | Visual browsing, SQLite |
| **sqlite3 (command)** | SQLite only | ⭐⭐⭐ Hard | Advanced users, scripts |
| **pgAdmin** | PostgreSQL only | ⭐⭐ Medium | Visual browsing, PostgreSQL |
| **psql (command)** | PostgreSQL only | ⭐⭐⭐ Hard | Advanced users, scripts |
| **DBeaver** | Both | ⭐⭐ Medium | Universal tool, any database |
| **MySQL Workbench** | ❌ None | N/A | Wrong tool (for MySQL only!) |

---

## 📖 Need More Help?

- **Complete database guide**: See [DATABASE.md](DATABASE.md)
- **Frequently asked questions**: See [FAQ.md](FAQ.md)
- **Quick start guide**: See [QUICKSTART.md](QUICKSTART.md)

---

## 💡 Pro Tips

1. **Start simple**: Use `python view_database.py` first
2. **For regular use**: Install DB Browser (SQLite) or pgAdmin (PostgreSQL)
3. **Don't use MySQL Workbench**: It's incompatible with this application
4. **Check your database type**: Look in `.env` file for DATABASE_TYPE
5. **The web dashboard**: Works regardless of database type!
