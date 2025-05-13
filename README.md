# SecureDBGuard

A simple, robust demonstration of SQL Injection prevention in Python using SQLite.

## Features
- Enforces parameterized queries only
- Detects and blocks risky SQL patterns
- Logs all suspicious activity
- CLI to view logs

## Project Structure
```
SecureDBGuard/
├── users.sql                # Sample DB schema and data
├── test.db                  # SQLite DB file
├── securedb.py              # Secure wrapper module
├── test_safe.py             # Test script with safe queries
├── test_unsafe.py           # Test script with unsafe queries
├── sql_injection_log.txt    # Log file for SQLi attempts
├── view_logs.py             # CLI to view logs
└── README.md                # Project documentation
```

## Setup
1. **Create the database:**
   ```sh
   sqlite3 test.db < users.sql
   ```
2. **Run safe queries:**
   ```sh
   python3 test_safe.py
   ```
3. **Run unsafe queries (should be blocked and logged):**
   ```sh
   python3 test_unsafe.py
   ```
4. **View logs:**
   ```sh
   python3 view_logs.py
   ```

## How it Works
- All queries go through `SecureDB.execute()`
- Only parameterized queries are allowed
- If a query matches a risky pattern, it is blocked and logged
- All logs are written to `sql_injection_log.txt`

## Example
**Safe:**
```python
from securedb import SecureDB
db = SecureDB()
print(db.execute("SELECT * FROM users WHERE username = ?", ("admin",)))
db.close()
```

**Unsafe:**
```python
from securedb import SecureDB
db = SecureDB()
db.execute("SELECT * FROM users WHERE username = 'admin' OR 1=1 --'")  # Blocked!
db.close()
```

## License
MIT 