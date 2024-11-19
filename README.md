# kleinanzeigen-scraper
This project contains scripts to scrape titles and URLs from kleinanzeigen.de for ads meeting a given criteria.
It uses Python libraries like `requests` and `BeautifulSoup` to extract and process data.
Ideally we would create a DAG in Apache Airflow so that this script automatically looks for search results daily.

## Features
- Scrapes data based on user-defined parameters (e.g. category, location, price, search terms, etc.).
- Outputs data as a list of tuples (title,url).
- Sends the list of results per e-mail as clickable links.

## File Descriptions
- `functions.py`: Contains the function `kleinanzeigen_heute()` that collects ads published today for the given search parameters. The ad publication date is stored in a variable named `date_section`; to search for ads published yesterday we should replace the word `Heute` by `Gestern`, and for longer time intervals we can simply transform the publication dates from string (e.g. 31.12.2024) into datetime format.
- `script.py`: Contains some examples of URLs of different searches we may want to perform. Uses `kleinanzeigen_heute()` to collect the data and sends the output as an e-mail message.
- `search_template_auto.txt`: Contains a template with the components of a typical URL for a search in the Auto category of kleinanzeigen.de. A similar template could be created for any other type of search (Immobilien, Elektronik, etc.); we would then simply manually perform a search on the website with all the possible filters, copy-paste the URL on a text file and split the components of the address.
- `search_template_immobilien.txt`: Similarly, contains a template with the components of a typical URL for a search in the Immobilien category of kleinanzeigen.de.
- `requirements.txt`: Lists the Python libraries needed for the project.

## Requirements
- beautifulsoup4==4.9.0
- pandas==1.0.3
- redmail==0.6.0
- Requests==2.32.3
- Install dependencies using `pip install -r requirements.txt`.

## Usage
1. Clone the repository:
   ```
   git clone https://github.com/JavierLxs/kleinanzeigen-scraper
   cd kleinanzeigen-scraper
   ```
2. Configure the `script.py` file with your search parameters and e-mail credentials. To define your search URLs you can use any of the provided search templates or create your own.
3. Run the script:
   ```
   python script.py
   ```
