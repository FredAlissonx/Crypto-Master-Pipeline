import os
from dotenv import load_dotenv
import requests
from requests.models import Response


class APIUtils:
    """
    Utility class for interacting with APIs, including setting up headers and making requests.
    """

    @staticmethod
    def setup_api_headers() -> dict:
        """
        Set up API headers for CoinGecko requests.

        Returns:
            dict: A dictionary of headers for API requests.

        Raises:
            ValueError: If the API_KEY is missing from environment variables.
        """
        load_dotenv()
        api_key = os.getenv("API_KEY")

        if not api_key:
            raise ValueError("API_KEY is missing. Please check your environment variables.")

        return {
            "accept": "application/json",
            "x-cg-api-key": api_key
        }

    @staticmethod
    def make_api_request(url: str, headers: dict) -> Response:
        """
        Make a GET request to the specified API URL.

        Args:
            url (str): The API endpoint URL.
            headers (dict): The headers to include in the request.

        Returns:
            Response: The response object from the API call.

        Raises:
            requests.exceptions.Timeout: For HTTP timeout related errors during the request.
            requests.exceptions.RequestException: For any HTTP-related errors during the request.
        """
        
        if not url:
            raise ValueError("URL can not be empty!")
        if not headers:
            raise ValueError("Headers can not be empty!")
        
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print("API request timed out.")
            raise
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}.")
            raise
