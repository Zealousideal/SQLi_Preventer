import sys
from securedb import SecureDB
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama
init()

class SecureDBMonitorCLI:
    def __init__(self):
        self.menu = '''\nSecureDBGuard CLI
==================
1. Run a safe query
2. Attempt an unsafe query
3. View SQL injection log
4. Exit\n'''

    def run_safe_query(self):
        db = SecureDB()
        try:
            query = input("Enter a parameterized SQL query (use ? for parameters):\n> ")
            params = input("Enter parameters as a comma-separated list (or leave blank):\n> ")
            params_tuple = tuple(p.strip() for p in params.split(",")) if params.strip() else ()
            try:
                result = db.execute(query, params_tuple)
                print(f"{Fore.GREEN}✓ Query executed successfully{Style.RESET_ALL}")
                print(f"Result: {result}")
            except Exception as e:
                print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        finally:
            db.close()

    def run_unsafe_query(self):
        db = SecureDB()
        try:
            query = input("Enter a raw SQL query (unsafe, for demo):\n> ")
            try:
                result = db.execute(query)
                print(f"{Fore.GREEN}✓ Query executed successfully{Style.RESET_ALL}")
                print(f"Result: {result}")
            except Exception as e:
                print(f"{Fore.RED}✗ Blocked: {e}{Style.RESET_ALL}")
        finally:
            db.close()

    def colorize_log_line(self, line):
        # Add timestamp if not present
        if not line.startswith('['):
            timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            line = f"{timestamp} {line}"

        # Colorize based on content
        if '[SAFE]' in line:
            return f"{Fore.GREEN}✓ {line}{Style.RESET_ALL}"
        elif '[UNSAFE]' in line:
            return f"{Fore.RED}✗ {line}{Style.RESET_ALL}"
        elif '[BLOCKED]' in line:
            return f"{Fore.RED}⚠ {line}{Style.RESET_ALL}"
        elif '[ERROR]' in line:
            return f"{Fore.RED}✗ {line}{Style.RESET_ALL}"
        elif '[ALERT]' in line:
            return f"{Fore.RED}⚠ {line}{Style.RESET_ALL}"
        elif '[INFO]' in line:
            return f"{Fore.GREEN}ℹ {line}{Style.RESET_ALL}"
        elif '[WARNING]' in line:
            return f"{Fore.YELLOW}⚠ {line}{Style.RESET_ALL}"
        else:
            return line

    def view_logs(self):
        print(f"\n{Fore.CYAN}=== SQL Injection Log ==={Style.RESET_ALL}")
        try:
            with open("sql_injection_log.txt") as f:
                for line in f:
                    print(self.colorize_log_line(line), end="")
        except FileNotFoundError:
            print(f"{Fore.RED}No log file found.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}======================={Style.RESET_ALL}\n")

    def menu_loop(self):
        while True:
            print(self.menu)
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.run_safe_query()
            elif choice == "2":
                self.run_unsafe_query()
            elif choice == "3":
                self.view_logs()
            elif choice == "4":
                print("Goodbye!")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

def main():
    cli = SecureDBMonitorCLI()
    cli.menu_loop()

if __name__ == "__main__":
    main() 