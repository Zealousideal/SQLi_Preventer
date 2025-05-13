from securedb import SecureDB

def main():
    db = SecureDB()
    try:
        queries = [
            # Classic tautologies
            "SELECT * FROM users WHERE username = 'admin' OR 1=1 --",
            "SELECT * FROM users WHERE username = '' OR '1'='1' --",
            "SELECT * FROM users WHERE username = 'admin' OR '1'='1'",
            "SELECT * FROM users WHERE username = 'admin' OR TRUE --",
            # Union-based
            "SELECT * FROM users UNION SELECT * FROM sqlite_master --",
            "SELECT * FROM users WHERE id = 1 UNION SELECT name, sql, 1 FROM sqlite_master --",
            # Piggy-backed queries
            "SELECT * FROM users; DROP TABLE users; --",
            "SELECT * FROM users WHERE username = 'admin'; DROP TABLE users; --",
            # Comments
            "SELECT * FROM users WHERE username = 'admin' -- and password = 'foo'",
            "SELECT * FROM users WHERE username = 'admin' #",
            # Blind SQLi
            "SELECT * FROM users WHERE username = 'admin' AND SUBSTR(password,1,1) = 'a' --",
            # Time-based
            "SELECT * FROM users WHERE username = 'admin' OR 1=1; SELECT sleep(5); --",
            # Sub-selects
            "SELECT * FROM users WHERE id = (SELECT MAX(id) FROM users); DROP TABLE users; --",
            # Encoded attacks
            "SELECT * FROM users WHERE username = CHAR(97,100,109,105,110) --",
            # Known bypasses
            "SELECT * FROM users WHERE username = 'admin'/**/OR/**/1=1 --",
            "SELECT * FROM users WHERE username = 'admin' OR 1=1#",
            "SELECT * FROM users WHERE username = 'admin' OR 1=1/*",
            # Hex encoding
            "SELECT * FROM users WHERE username = 0x61646d696e --",
            # Stacked queries
            "SELECT * FROM users; SELECT * FROM sqlite_master; --",
            # Insert/Update/Delete
            "INSERT INTO users (username, password) VALUES ('evil', 'pw'); --",
            "UPDATE users SET password = 'pw' WHERE username = 'admin' OR 1=1 --",
            "DELETE FROM users WHERE username = 'admin' OR 1=1 --",
            # Exec/Stored procedures
            "EXEC xp_cmdshell('dir'); --",
            # Obfuscated
            "SELECT * FROM users WHERE username = 'admin' OR\n'1'='1' --",
            "SELECT * FROM users WHERE username = 'admin' OR '1' = '1' --",
            # Double query
            "SELECT * FROM users WHERE username = 'admin'; SELECT * FROM users; --",
            # Attempt to bypass filters
            "SELECT * FROM users WHERE username = 'admin' OR 'a'='a' --",
            "SELECT * FROM users WHERE username = 'admin' OR 1=1; --",
            # Using semicolons
            "SELECT * FROM users WHERE username = 'admin';--",
            # Using sleep for time-based
            "SELECT * FROM users WHERE username = 'admin' OR SLEEP(5) --",
        ]
        for i, query in enumerate(queries, 1):
            print(f"[UNSAFE {i}] Attempting: {query}")
            try:
                db.execute(query)
            except Exception as e:
                print(f"Blocked: {e}\n")
    finally:
        db.close()

if __name__ == "__main__":
    main() 