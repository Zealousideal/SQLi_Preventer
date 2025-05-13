import sqlite3
import re
import logging

class SecureDB:
    def __init__(self, db_path="test.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        logging.basicConfig(filename="sql_injection_log.txt", level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')

    def execute(self, query, params=None):
        if self._is_safe_query(query):
            try:
                self.cursor.execute(query, params or [])
                self.conn.commit()
                return self.cursor.fetchall()
            except Exception as e:
                logging.warning(f"DB Error: {e}")
                raise
        else:
            logging.warning(f"[ALERT] SQL Injection attempt detected: {query}")
            raise Exception("Blocked potentially unsafe query")

    def _is_safe_query(self, query):
        # Basic SQLi pattern matching
        sqli_patterns = [
            r"(--|\bOR\b|\bAND\b\s+\d+=\d+)",    # Classic injections
            r"(?i)union\s+select",               # UNION attacks
            r"(?i)drop\s+table",                 # Drop commands
            r"(?i)insert\s+into",                # Unwanted inserts
            r"(?i)exec(\s|\+)+(s|x)p\w+"         # Exec/sp stored procedures
        ]
        for pattern in sqli_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return False
        return True

    def close(self):
        self.conn.close() 