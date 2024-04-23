#reminder_agent.py

from dateutil import parser
import datetime

def set_reminder(text):
    try:
        # Parse the time from the text
        reminder_time = parser.parse(text, fuzzy=True)
        if reminder_time < datetime.datetime.now():
            print("Reminder time has already passed.")
        else:
            print(f"Reminder set for {reminder_time}")
            # In a real application, you would store this reminder
    except ValueError:
        print("Could not understand the time.")

if __name__ == "__main__":
    # Example usage
    set_reminder("Remind me to call John on June 25 at 5 pm")

