from recipe_scrapers import scrape_me
from rich.console import Console 
import sys

recipe_url = sys.argv[1]

console = Console()

def save_to_markdown():
    pass


def view_in_terminal(url):
    """
    
    :param url: a url string from a recipe website
    :return: 
    :rtype:
    """
    scraper = scrape_me(url)
    console.print('\n\n', scraper.title(), style="bold white", justify='center')
    console.print('\nINGREDIENTS', style="bold white")
    for index, ingredient in enumerate(scraper.ingredients()):
        console.print('-', ingredient, style='gold3')
    console.print('\nINSTRUCTIONS', style="bold white")
    for index, instruction in enumerate(scraper.instructions_list()):
        console.print(index+1, ') ', style='white', sep='', end='', highlight=False)
        console.print(instruction, style='gold3')


def main(url):

    
    view_in_terminal(url)
    

main(recipe_url)

