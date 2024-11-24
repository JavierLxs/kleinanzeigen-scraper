from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

def kleinanzeigen_heute(url):
    """
    Fetches titles and URLs from Kleinanzeigen ads published today.

    Parameters:
    url (str): The URL of the page to scrape.

    Returns:
    list of tuples: A list containing tuples of (title, url).
    """
    # Create soup:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    # Initialize an empty list to store the tuples (title, url)
    ads_heute = []

    while True:
        # Create soup:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, 'lxml')

        # Find ads:
        ads = soup.find_all('div', class_='aditem-main')

        # Find all ad items:
        for ad in ads:
            # Find ad publication date:
            date_section = ad.find('div', class_='aditem-main--top--right')
            ad_date = date_section.get_text(strip=True)

            # Check if the date contains "Heute", "Gestern" or is within the last 7 days
            if "Heute" in ad_date:
                # Extract the title and URL:
                title_tag = ad.find('a', class_='ellipsis')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    url = 'https://www.kleinanzeigen.de' + title_tag['href']

                # Append the result as a tuple (title, url)
                ads_heute.append((title, url))

        # Check if there's an additional results page:
        try:
            next_button = soup.find('a', {'data-cy': 'paginator-next'})

            if next_button and 'href' in next_button.attrs:
                next_page_url = 'https://www.jobs.ch' + next_button['href']
                url = next_page_url  #updates URL to the next page
            else:
                #print("No next button found; exiting loop.")
                break  # Exits loop if no next button is found

        except AttributeError:
            # Handles cases where 'soup.find' or 'next_button['href']' causes an error
            print("AttributeError: Problem finding or accessing the next page button.")
            break

        except Exception as e:
            # Catch-all for any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            break

    return ads_heute

def kleinanzeigen_search(url):
    """
    Fetches titles and URLs from Kleinanzeigen ads published in a given time interval.

    Parameters:
    url (str): The URL of the page to scrape.

    Returns:
    list of tuples: A list containing tuples of (title, url).
    """
    # Create soup:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    # Initialize an empty list to store the tuples (title, url)
    ads_heute = []

    while True:
        # Create soup:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, 'lxml')

        # Find ads:
        ads = soup.find_all('div', class_='aditem-main')

        # Find all ad items
        for ad in ads:
            # Find ad publication date:
            date_section = ad.find('div', class_='aditem-main--top--right')
            ad_date = date_section.get_text(strip=True)
            today = datetime.today()

            # Check if the date contains "Heute", "Gestern" or is within the last 7 days:
            if ("Heute" in ad_date or
                "Gestern" in ad_date or
                (":" not in ad_date and  # Ensures it's not a time (e.g., "10:30")
                datetime.strptime(ad_date, "%d.%m.%Y") >= today - timedelta(days=7))):

                # Extract the title and URL
                title_tag = ad.find('a', class_='ellipsis')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    url = 'https://www.kleinanzeigen.de' + title_tag['href']

                # Append the result as a tuple (title, url)
                ads_heute.append((title, url))

        # Check if there's an additional results page:
        try:
            next_button = soup.find('a', {'data-cy': 'paginator-next'})

            if next_button and 'href' in next_button.attrs:
                next_page_url = 'https://www.jobs.ch' + next_button['href']
                url = next_page_url  #updates URL to the next page
            else:
                #print("No next button found; exiting loop.")
                break  # Exits loop if no next button is found

        except AttributeError:
            # Handles cases where 'soup.find' or 'next_button['href']' causes an error
            print("AttributeError: Problem finding or accessing the next page button.")
            break

        except Exception as e:
            # Catch-all for any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            break

    return ads_heute
