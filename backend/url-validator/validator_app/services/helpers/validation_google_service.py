import httpx
from pydantic import HttpUrl

from validator_app.core.logger import logger


class GoogleUrlChecker:
    """
    Service for checking if a URL is safe using Google Safe Browsing API.
    """

    def __init__(self, api_key: str):
        # Save the API key
        self.api_key = api_key

        # Full endpoint URL with embedded API key
        self.url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.api_key}"

        # Required metadata for the client identity (defined by Google)
        self.client_id = "url-validator"
        self.client_version = "1.0"

    async def is_url_safe(self, url: str | HttpUrl) -> tuple[bool | None, list[dict]]:
        """
        Checks the given URL using Google Safe Browsing API.

        Returns:
            - (False, matches): if the URL is considered unsafe
            - (True, []): if the URL is considered safe
            - (None, []): if the check failed (e.g., network error)
        """

        # Prepare the request payload based on Google API requirements
        payload = {
            "client": {
                "clientId": self.client_id,
                "clientVersion": self.client_version
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": str(url)}]
            }
        }

        try:
            # Make the request asynchronously using httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(self.url, json=payload, timeout=5)

            # Raise an exception if status code is 4xx or 5xx
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # If Google detected any threats, return False and the threat details
            if data.get("matches"):
                logger.warning(f"URL flagged as unsafe by Google: {url}")
                return False, data["matches"]

            # If no threats found, return True (safe)
            return True, []

        except httpx.RequestError as e:
            # Network or connection error occurred during the request
            logger.error(f"Request to Google Safe Browsing failed: {e}")
            return None, []

        except Exception as e:
            # Any other unexpected error (e.g., parsing, runtime issues)
            logger.error(f"Unexpected error in GoogleUrlChecker: {e}")
            return None, []
