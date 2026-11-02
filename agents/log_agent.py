
from pathlib import Path
from datetime import datetime


# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Log file location
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "customer_support_history.txt"


def save_customer_interaction(
    customer_query: str,
    agent_response: str,
    answered_by: str,
    status: str = "Answered"
) -> str:

    """
    Save customer question and final response
    with local date and time.

    Every interaction is appended to the TXT file.
    Previous records are never overwritten.
    """

    try:

        # Create logs folder if it does not exist
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Get local date and time
        current_time = datetime.now().astimezone()

        date = current_time.strftime("%d-%m-%Y")
        time = current_time.strftime("%I:%M:%S %p %Z")

        # Prepare log entry
        log_entry = f"""
========================================
CUSTOMER SUPPORT INTERACTION
========================================

Date       : {date}
Time       : {time}
Customer   : {customer_query}

Answered By: {answered_by}

Response:
{agent_response}

Status     : {status}

========================================

"""

        # Append entry to file
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_entry)

        print("Customer interaction saved successfully.")

        return str(LOG_FILE)

    except Exception as error:

        print(f"Error saving customer interaction: {error}")

        raise


print("Agent 03: Customer Support Log Agent is ready.")
