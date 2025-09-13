import requests
from typing import Dict, Any, Optional

def vote_on_poll(
    poll_id: int, 
    option_id: int, 
    access_token: str, 
    base_url: str = "http://localhost:8000"
) -> Dict[str, Any]:
    """
    Cast a vote on an existing poll
    
    Args:
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        access_token (str): JWT access token for authentication
        base_url (str): The base URL of the API (default: http://localhost:8000)
        
    Returns:
        Dict[str, Any]: Vote response following VoteOut schema with fields:
            - id (int): Vote ID
            - user_id (int): ID of the user who voted
            - option_id (int): ID of the voted option
            - created_at (str): Timestamp when vote was created
            
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If authentication fails, poll/option not found, or other API errors
    """
    # Prepare the request URL and payload
    url = f"{base_url}/polls/{poll_id}/vote"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "option_id": option_id
    }
    
    try:
        # Send the POST request to vote on the poll
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            vote_data = response.json()
            
            # Validate response structure
            required_fields = ["id", "user_id", "option_id", "created_at"]
            for field in required_fields:
                if field not in vote_data:
                    raise ValueError(f"Invalid response: missing field '{field}'")
            
            return vote_data
        else:
            # Handle error cases
            try:
                error_data = response.json()
                error_message = error_data.get("detail", "Unknown error")
            except:
                error_message = f"HTTP {response.status_code}"
            
            if response.status_code == 401:
                raise ValueError("Unauthorized: Invalid or expired access token")
            elif response.status_code == 404:
                raise ValueError("Poll or option not found")
            else:
                raise ValueError(f"Failed to vote on poll: {error_message}")
                
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


def get_poll_results(
    poll_id: int, 
    base_url: str = "http://localhost:8000"
) -> Dict[str, Any]:
    """
    Retrieve poll results with vote counts for each option
    
    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): The base URL of the API (default: http://localhost:8000)
        
    Returns:
        Dict[str, Any]: Poll results following PollResults schema with fields:
            - poll_id (int): ID of the poll
            - question (str): The poll question
            - results (List[Dict]): List of results for each option containing:
                - option_id (int): ID of the option
                - text (str): Text of the option
                - vote_count (int): Number of votes for this option
                
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If poll not found or other API errors
    """
    # Prepare the request URL
    url = f"{base_url}/polls/{poll_id}/results"
    
    try:
        # Send the GET request to fetch poll results
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            results_data = response.json()
            
            # Validate response structure
            required_fields = ["poll_id", "question", "results"]
            for field in required_fields:
                if field not in results_data:
                    raise ValueError(f"Invalid response: missing field '{field}'")
            
            # Validate results array structure
            if not isinstance(results_data["results"], list):
                raise ValueError("Invalid response: 'results' must be a list")
            
            for i, result in enumerate(results_data["results"]):
                result_required_fields = ["option_id", "text", "vote_count"]
                for field in result_required_fields:
                    if field not in result:
                        raise ValueError(f"Invalid response: result {i} missing field '{field}'")
                
                # Validate field types
                if not isinstance(result["option_id"], int):
                    raise ValueError(f"Invalid response: result {i} 'option_id' must be integer")
                if not isinstance(result["text"], str):
                    raise ValueError(f"Invalid response: result {i} 'text' must be string")
                if not isinstance(result["vote_count"], int):
                    raise ValueError(f"Invalid response: result {i} 'vote_count' must be integer")
            
            return results_data
        else:
            # Handle error cases
            try:
                error_data = response.json()
                error_message = error_data.get("detail", "Unknown error")
            except:
                error_message = f"HTTP {response.status_code}"
            
            if response.status_code == 404:
                raise ValueError("Poll not found")
            else:
                raise ValueError(f"Failed to get poll results: {error_message}")
                
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Example: Vote on a poll
    try:
        # You would get this token from the login function
        access_token = "your_jwt_token_here"
        
        vote_result = vote_on_poll(
            poll_id=1, 
            option_id=2, 
            access_token=access_token
        )
        print(f"Vote cast successfully: {vote_result}")
        
    except Exception as e:
        print(f"Error voting: {e}")
    
    # Example: Get poll results
    try:
        results = get_poll_results(poll_id=1)
        print(f"\nPoll Results for: {results['question']}")
        for result in results['results']:
            print(f"- {result['text']}: {result['vote_count']} votes")
            
    except Exception as e:
        print(f"Error getting results: {e}")