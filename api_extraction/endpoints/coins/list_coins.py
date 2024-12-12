from typing import Optional
from api_extraction.utils.api_utils import APIUtils
from urllib.parse import urlencode
import pandas as pd

class ListCoins:
    """
    A class to fetch a list of cryptocurrency coins from a given base API URL.

    Attributes:
        base_url (str): The base URL of the API endpoint.
        include_platform (Optional[bool]): Indicates whether to include platform information in the response.
        status (Optional[str]): The status of the coins to filter, either 'active' or 'inactive'.
    """

    def __init__(self, base_url: str, include_platform: Optional[bool] = None, status: Optional[str] = None):
        """
        Initializes the ListCoins object with API configuration.

        Args:
            base_url (str): The base URL of the API endpoint.
            include_platform (Optional[bool]): Whether to include platform data in the response.
            status (Optional[str]): Filter for coin status ('active' or 'inactive').
        """
        self.base_url = base_url.rstrip("/")
        self.include_platform = include_platform
        self.status = status

    def get_coins_list(self) -> dict:
        """
        Fetches the list of coins from the API.

        Returns:
            dict: The API response containing the list of coins.

        Raises:
            Exception: If the API request fails.
        """
        headers = APIUtils.setup_api_headers()
        url = self.get_full_url()
        response = APIUtils.make_api_request(url=url, headers=headers)

        return response.json()

    def get_full_url(self) -> str:
        """
        Constructs the full API URL with query parameters.

        Returns:
            str: The full URL with encoded query parameters.
        """
        main_url = f"{self.base_url}/coins/list"
        params: dict[str, str] = {}

        if self.include_platform is not None:
            params["include_platform"] = str(self.include_platform).lower()

        if self.status is not None:
            valid_status = {"active", "inactive"}
            if self.status.lower() in valid_status:
                params["status"] = self.status.lower()
            else:
                raise ValueError(f"Invalid status: {self.status}. Must be 'active' or 'inactive'.")

        query_string = urlencode(params)
        return f"{main_url}?{query_string}" if query_string else main_url


coins = ListCoins(base_url="https://api.coingecko.com/api/v3", include_platform=False)

data = coins.get_coins_list()
list_coins = ["bitcoin", "ethereum", "solana", "cardano", "bitcoin-cash"]
df = pd.DataFrame(data)
filtered_df = df[df['id'].isin(list_coins)]
print(filtered_df)