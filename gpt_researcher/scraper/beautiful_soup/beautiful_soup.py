import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from ..utils import get_relevant_images, extract_title, get_text_from_soup, clean_soup

class BeautifulSoupScraper:

    def __init__(self, link, session=None):
        self.link = link
        self.session = session

    def scrape(self):
        """
        This function scrapes content from a webpage by making a GET request, parsing the HTML using
        BeautifulSoup, and extracting script and style elements before returning the cleaned content.
        
        Returns:
          The `scrape` method is returning the cleaned and extracted content from the webpage specified
        by the `self.link` attribute. The method fetches the webpage content, removes script and style
        tags, extracts the text content, and returns the cleaned content as a string. If any exception
        occurs during the process, an error message is printed and an empty string is returned.
        """
        try:
            response = self.session.get(self.link, timeout=4)
            
            # Create a directory to store scraped sites if it doesn't exist
            output_dir = "outputs/scraped_sites"
            os.makedirs(output_dir, exist_ok=True)

            # Sanitize the URL to create a valid filename
            parsed_url = urlparse(self.link)
            filename = f"{parsed_url.netloc.replace('.', '_')}_{parsed_url.path.replace('/', '_')}.html"
            filename = re.sub(r'_+', '_', filename).strip('_')

            # Save the raw HTML content
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(response.content)

            soup = BeautifulSoup(
                response.content, "lxml", from_encoding=response.encoding
            )

            soup = clean_soup(soup)

            content = get_text_from_soup(soup)

            image_urls = get_relevant_images(soup, self.link)
            
            # Extract the title using the utility function
            title = extract_title(soup)

            return content, image_urls, title

        except Exception as e:
            print("Error! : " + str(e))
            return "", [], ""