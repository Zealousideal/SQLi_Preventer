def view_logs():
    try:
        with open("sql_injection_log.txt") as f:
            for line in f:
                print(line, end="")
    except FileNotFoundError:
        print("No log file found.")

if __name__ == "__main__":
    view_logs() 