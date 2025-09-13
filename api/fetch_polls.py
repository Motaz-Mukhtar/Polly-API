import requests
from typing import List, Dict, Any, Optional

def fetch_polls(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> List[Dict[str, Any]]:
    """
    Fetch paginated poll data from the /polls endpoint
    
    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: http://localhost:8000)
        
    Returns:
        List[Dict[str, Any]]: List of poll objects following the PollOut schema
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the response format is invalid
    """
    # Prepare the request URL with query parameters
    url = f"{base_url}/polls"
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        # Send the GET request to fetch polls
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            polls_data = response.json()
            
            # Validate that the response is a list
            if not isinstance(polls_data, list):
                raise ValueError("Expected a list of polls in the response")
            
            return polls_data
        else:
            # Handle error cases
            try:
                error_data = response.json()
                error_message = error_data.get("detail", "Unknown error")
            except:
                error_message = f"HTTP {response.status_code}"
            
            raise ValueError(f"Failed to fetch polls: {error_message}")
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


def fetch_polls_with_validation(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> List[Dict[str, Any]]:
    """
    Fetch paginated poll data with additional validation of the response schema
    
    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: http://localhost:8000)
        
    Returns:
        List[Dict[str, Any]]: List of validated poll objects
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the response format doesn't match the expected schema
    """
    polls = fetch_polls(skip, limit, base_url)
    
    # Validate each poll object against the expected schema
    required_fields = ["id", "question", "created_at", "owner_id", "options"]
    
    for i, poll in enumerate(polls):
        # Check if all required fields are present
        for field in required_fields:
            if field not in poll:
                raise ValueError(f"Poll at index {i} is missing required field: {field}")
        
        # Validate field types
        if not isinstance(poll["id"], int):
            raise ValueError(f"Poll at index {i}: 'id' must be an integer")
        if not isinstance(poll["question"], str):
            raise ValueError(f"Poll at index {i}: 'question' must be a string")
        if not isinstance(poll["owner_id"], int):
            raise ValueError(f"Poll at index {i}: 'owner_id' must be an integer")
        if not isinstance(poll["options"], list):
            raise ValueError(f"Poll at index {i}: 'options' must be a list")
        
        # Validate options structure
        for j, option in enumerate(poll["options"]):
            option_required_fields = ["id", "text", "poll_id"]
            for field in option_required_fields:
                if field not in option:
                    raise ValueError(f"Poll {i}, option {j} is missing required field: {field}")
    
    return polls


# Example usage
if __name__ == "__main__":
    try:
        # Fetch first 5 polls
        polls = fetch_polls(skip=0, limit=5)
        print(f"Fetched {len(polls)} polls:")
        for poll in polls:
            print(f"- Poll {poll['id']}: {poll['question']} (Options: {len(poll['options'])})")
        
        # Fetch with validation
        validated_polls = fetch_polls_with_validation(skip=0, limit=10)
        print(f"\nValidated {len(validated_polls)} polls successfully")
        
    except Exception as e:
        print(f"Error: {e}")