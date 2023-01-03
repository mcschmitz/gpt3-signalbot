from typing import Dict, List

import requests


def get_groups(phone_number: str, service: str) -> List[Dict[str, str]]:
    """Returns the name, id, and internal id of a users groups.

    Args:
        phone_number: The users phone number
        service: The IP adress of the local signal service
    """
    resp = requests.get(f"http://{service}/v1/groups/{phone_number}")
    groups_list = resp.json()
    return [
        {
            "name": group["name"],
            "id": group["id"],
            "internal_id": group["internal_id"],
        }
        for group in groups_list
    ]
