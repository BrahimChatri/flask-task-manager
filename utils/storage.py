import json, os
from typing import Any
import utils.logger as logger

class Storage:
    """Class to handle saving data to json files. and give each one name to track each user with their own data."""
    @staticmethod
    def load_data(filename: str) -> dict[str, Any]:
        """Load data from JSON file and return it as a dictionary."""
        file_path = os.path.join(os.path.dirname(__file__), "../data", f"{filename}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.Error_logger.error(
                        "The users file is empty or corrupted. Starting with an empty user list."
                    )
                    return {}
        logger.Info_logger.info("No user file found. Starting with an empty user list.")
        return {}

    @staticmethod
    def save_data(user_data: dict, filename: str) -> None:
        """Save the user data to the JSON file."""
        file_path = os.path.join(os.path.dirname(__file__),  "../data", f"{filename}.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=4)
            logger.Info_logger.info("Data saved successfully.")
        except OSError:
            logger.Error_logger.error("Couldn't save the data")

    @staticmethod
    def user_exists(username: str) -> bool:
        return os.path.exists(f"data/{username}.json")
