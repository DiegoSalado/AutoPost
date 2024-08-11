import requests
from bs4 import BeautifulSoup

def fetch_spaceflight_articles() -> dict:
    """
    Fetches the latest spaceflight news articles from the Spaceflight News API.

    Returns:
        dict: A dictionary containing the response JSON data, which includes the spaceflight articles.
    """
    headers = {
        "accept": "application/json",
        "accept-language": "es-ES,es;q=0.9",
        "referer": "https://api.spaceflightnewsapi.net/v4/docs/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    response = requests.get("https://api.spaceflightnewsapi.net/v4/articles/", headers=headers)
    response.raise_for_status()  # Raise an error for bad responses

    return response.json()


def extract_text_from_url(url: str) -> str:
    """
    Extracts all the text content from a given URL.

    Args:
        url (str): The URL of the webpage to extract text from.

    Returns:
        str: The text content of the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
