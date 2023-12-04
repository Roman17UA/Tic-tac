import requests
from bs4 import BeautifulSoup
import os


def get_cache_filename(url):
    # Create a filename based on the URL
    return f"cache/{url.replace('/', '_').replace(':', '_').replace('.', '_')}.html"


def download_url(url):
    # Check if the cache directory exists, create it if not
    if not os.path.exists('cache'):
        os.makedirs('cache')

    # Check if the response is already cached
    cache_filename = get_cache_filename(url)
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r', encoding='utf-8') as file:
            content = file.read()
        print("Using cached content.")
        return content

    # If not cached, download the content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        content = response.content.decode('utf-8')

        # Save the content to the cache
        with open(cache_filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print("Downloaded and cached content.")
        return content
    else:
        print(f"Failed to download the page. Status code: {response.status_code}")
        return None


if __name__ == '__main__':
    # Example usage
    url = "https://prom.ua/ua/"
    content = download_url(url)
    if content is None:
        print("ERROR: CONTENT_IS_NONE")
        exit()
    # Now you can use the downloaded_content as needed

    soup = BeautifulSoup(content, 'html.parser')

    # Find all items on the page with the updated selector
    items = soup.select('div[data-testid="listing-grid"] > div[data-testid="l-card"]')

    # Print the details of each item
    for item in items:
        # Extract the title and price if available
        print(item.select_one("h6").text)
        print(item.select_one('[data-testid="location-date"]').text.split("-"))
        print(item.select_one('[data-testid="ad-price"]').text)
        print("https://www.prom.ua" + item.select_one('a')['href'])
        print(item.select_one('[title="Нове"]'))
        print(item.select_one('[title="Вживане"]'))
        print(item.select_one('[data-testid="param-value"]'))
        print()
