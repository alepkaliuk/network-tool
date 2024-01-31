import time
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen

# Variables for Telegram bot
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
LOG_FILE_PATH = "/flash/guest-share/log_20231130-222053"
PROGRAM_LOG_FILE = "/flash/guest-share/program_log.txt"

# Variables to store the time of the last sent message and the last sent log
last_sent_time = 0
last_sent_log = ""

def get_severity_level(log_line):
    try:
        # We divide the line by the "-" sign and choose the part containing the level of importance
        severity_level = int(log_line.split('-')[1].split('-')[0])
        return severity_level
    except (IndexError, ValueError) as e:
        log_message = f"Error in get_severity_level: {e}\nProblematic log line: {log_line}\n"
        write_to_log(log_message)
        return -1

def write_to_log(message):
    with open(PROGRAM_LOG_FILE, "a") as log_file:
        log_file.write(message)

def format_time(timestamp):
    # We format the time conveniently
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

while True:
    try:
        # Read the content of the log file
        with open(LOG_FILE_PATH, "r") as log_file:
            # Read all lines and get the last one
            logs = log_file.readlines()[-1]

        severity_level = get_severity_level(logs)

        # Get the current time in seconds
        current_time = time.time()

        # Output values for debugging and write to log file
        log_message = f"Logs: {logs}\nSeverity Level: {severity_level}\nCurrent Time: {format_time(current_time)}\nLast Sent Time: {format_time(last_sent_time)}\nLast Sent Log: {last_sent_log}\n"
        print(log_message)
        write_to_log(log_message)

        # Check if there are new logs, if the last log is different, and if severity is in range 0 to 4
        if current_time > last_sent_time and logs != last_sent_log and 0 <= severity_level <= 4:
            # Check if the logs are not empty
            if logs.strip():
                # Message to send
                message = f"Important log from Cisco IOS:\n{logs}"

                # Send the message using the Telegram API
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
                response = urlopen(url, data=urlencode(data).encode())

                # Check the response status
                if response.status == 200:
                    # Update the time and log of the last sent message
                    last_sent_time = current_time
                    last_sent_log = logs

                    # Print a message about the logs being sent
                    success_message = "Logs sent to Telegram\n"
                    print(success_message)
                    write_to_log(success_message)
                else:
                    error_message = f"Failed to send logs. HTTP Status Code: {response.status}\n"
                    print(error_message)
                    write_to_log(error_message)

            else:
                empty_logs_message = "Logs are empty. No logs sent to Telegram.\n"
                print(empty_logs_message)
                write_to_log(empty_logs_message)

        else:
            # Print a message if no new logs or if the last log was already sent or severity is not in the specified range
            no_new_logs_message = "No new logs, log already sent, or severity not in the specified range.\n"
            print(no_new_logs_message)
            write_to_log(no_new_logs_message)

        # Delay before the next check
        time.sleep(60)  # You can adjust the delay as needed

    except Exception as e:
        # Handle any other exceptions
        error_message = f"An error occurred: {e}\n"
        print(error_message)
        write_to_log(error_message)
