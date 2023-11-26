from recipe_scrapers import scrape_me
from rich.console import Console 
import sys

recipe_url = sys.argv[1]

console = Console()

def main(url):
    """
    
    :param url: a url string from a recipe website
    :return: 
    :rtype:
    """
    scraper = scrape_me(url)
    console.print('\n\n', scraper.title(), style="bold white")
    for ingredient in scraper.ingredients():
        console.print('-', ingredient, style='green')

main(recipe_url)