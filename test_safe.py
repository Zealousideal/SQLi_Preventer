from securedb import SecureDB

def main():
    db = SecureDB()
    try:
        # Create test table if it doesn't exist
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT,
                age INTEGER,
                is_active BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Safe queries with different parameter types and operations
        safe_queries = [
            # Basic SELECT with single parameter
            ("SELECT * FROM users WHERE username = ?", ("admin",)),
            
            # SELECT with multiple parameters
            ("SELECT * FROM users WHERE username = ? AND is_active = ?", ("admin", True)),
            
            # SELECT with numeric parameters
            ("SELECT * FROM users WHERE age > ? AND age < ?", (18, 65)),
            
            # SELECT with LIKE and wildcards
            ("SELECT * FROM users WHERE username LIKE ?", ("%admin%",)),
            
            # SELECT with IN clause
            ("SELECT * FROM users WHERE username IN (?, ?, ?)", ("admin", "user1", "user2")),
            
            # SELECT with ORDER BY and LIMIT
            ("SELECT * FROM users ORDER BY created_at DESC LIMIT ?", (10,)),
            
            # SELECT with JOIN
            ("SELECT u.username, p.title FROM users u JOIN posts p ON u.id = p.user_id WHERE u.id = ?", (1,)),
            
            # INSERT with multiple columns
            ("INSERT INTO users (username, email, age, is_active) VALUES (?, ?, ?, ?)", 
             ("newuser", "user@example.com", 25, True)),
            
            # UPDATE with multiple parameters
            ("UPDATE users SET email = ?, age = ? WHERE username = ?", 
             ("newemail@example.com", 26, "newuser")),
            
            # DELETE with parameter
            ("DELETE FROM users WHERE username = ?", ("newuser",)),
            
            # Complex WHERE clause
            ("SELECT * FROM users WHERE (age > ? OR is_active = ?) AND username LIKE ?", 
             (18, True, "%user%")),
            
            # Date comparison
            ("SELECT * FROM users WHERE created_at > datetime(?)", ("2024-01-01",)),
            
            # Aggregate functions
            ("SELECT COUNT(*) as user_count, AVG(age) as avg_age FROM users WHERE age > ?", (18,)),
            
            # Subquery
            ("SELECT * FROM users WHERE id IN (SELECT user_id FROM posts WHERE created_at > ?)", 
             ("2024-01-01",)),
            
            # CASE statement
            ("SELECT username, CASE WHEN age >= ? THEN 'Adult' ELSE 'Minor' END as age_group FROM users", 
             (18,)),
            
            # Multiple conditions
            ("SELECT * FROM users WHERE username = ? OR (age > ? AND is_active = ?)", 
             ("admin", 18, True)),
            
            # Pattern matching
            ("SELECT * FROM users WHERE email LIKE ? AND username LIKE ?", 
             ("%@gmail.com", "user%")),
            
            # NULL handling
            ("SELECT * FROM users WHERE email IS NULL OR email = ?", ("",)),
            
            # Boolean operations
            ("SELECT * FROM users WHERE is_active = ? AND (age > ? OR email IS NOT NULL)", 
             (True, 18)),
            
            # Complex JOIN with parameters
            ("""
            SELECT u.username, p.title, c.content 
            FROM users u 
            JOIN posts p ON u.id = p.user_id 
            JOIN comments c ON p.id = c.post_id 
            WHERE u.id = ? AND p.created_at > ?
            """, (1, "2024-01-01")),
            
            # Window functions
            ("""
            SELECT username, age,
            ROW_NUMBER() OVER (ORDER BY age) as age_rank
            FROM users
            WHERE age > ?
            """, (18,))
        ]

        print(f"{'='*80}\nTesting Safe Queries\n{'='*80}")
        
        for i, (query, params) in enumerate(safe_queries, 1):
            print(f"\n[SAFE {i}] Testing: {query}")
            print(f"Parameters: {params}")
            try:
                result = db.execute(query, params)
                print(f"Success! Result: {result}")
            except Exception as e:
                print(f"Error: {e}")
            print("-"*80)

    finally:
        db.close()

if __name__ == "__main__":
    main() 