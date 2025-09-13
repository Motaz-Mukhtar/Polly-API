import requests

def register_user(username: str, password: str, base_url: str = "http://localhost:8000"):
    """
    Register a new user via the /register endpoint
    
    Args:
        username (str): The username for the new user
        password (str): The password for the new user
        base_url (str): The base URL of the API (default: http://localhost:8000)
        
    Returns:
        dict: The response from the API containing the registered user information
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the username is already registered or other validation errors
    """
    # Prepare the request URL and payload
    url = f"{base_url}/register"
    payload = {
        "username": username,
        "password": password
    }
    
    # Send the POST request to register the user
    response = requests.post(url, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Handle common error cases
        error_data = response.json()
        if response.status_code == 400 and "Username already registered" in error_data.get("detail", ""):
            raise ValueError("Username already registered")
        else:
            raise ValueError(f"Registration failed: {error_data.get('detail', 'Unknown error')}")


# Example usage
if __name__ == "__main__":
    try:
        user = register_user("new_user", "secure_password")
        print(f"User registered successfully: {user}")
    except Exception as e:
        print(f"Error: {e}")