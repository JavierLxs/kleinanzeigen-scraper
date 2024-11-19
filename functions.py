import requests
from bs4 import BeautifulSoup

def kleinanzeigen_heute(url):
    """
    Fetches ad titles and URLs from ads published today in Kleinanzeigen.de.

    Parameters:
    url (str): The URL of the search page to scrape.

    Returns:
    list of tuples: A list containing tuples of (title, url).
    """
    # Create soup:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find all ad items:
    ad_items = soup.find_all('div', class_='aditem-main')

    # Initialize an empty list to store the tuples (title, url):
    ads_heute = []

    for ad in ad_items:
        # Check if the ad publication date containins "Heute":
        date_section = ad.find('div', class_='aditem-main--top--right')

        if date_section and "Heute" in date_section.get_text():

            # Extract the title and URL:
            title_tag = ad.find('a', class_='ellipsis')

            if title_tag:
                title = title_tag.get_text(strip=True)
                url = 'https://www.kleinanzeigen.de' + title_tag['href']

                # Append the result as a tuple (title, url):
                ads_heute.append((title, url))

    return ads_heute
