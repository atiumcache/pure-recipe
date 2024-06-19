import shutil

import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me
from rich.console import Console
from rich.markdown import Markdown
import argparse
import yaml
import os
import platformdirs
import inquirer


console = Console()


def main():
    settings = load_yaml()
    args = parse_arguments()

    try: 
        if args.operations == "view":
            view_recipe(args.url, settings, prompt_save=True)
        elif args.operations == "save":
            save_recipe_to_markdown(args.url, settings)
        elif args.operations == "list":
            save_list_of_recipes(args.url, settings)
        elif args.operations == "browse":
            browse_recipes()
        elif args.operations == "search":
            search()
        else: 
            console.print("Invalid operation. See documentation.",
                          style="bright_red")
    except Exception as e:
        console.print(f"\nAn error occurred: {str(e)}", style="bright_red bold")


def search():
    query = input("Enter a recipe search term: ")
    recipe_url = choose_recipe_from_search(query)
    if recipe_url:
        view_recipe_online(recipe_url)


def search_recipes(query):
    """
    Search for recipes online.

    Args:
        query (str): Search query.

    Returns:
        list of tuples: List of (recipe title, recipe URL).
    """
    url = f"https://www.allrecipes.com/search/results/?search={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    recipes = []
    for item in soup.select('.fixed-recipe-card'):
        title = item.select_one('.fixed-recipe-card__title-link').text.strip()
        link = item.select_one('.fixed-recipe-card__title-link')['href']
        recipes.append((title, link))

    return recipes


def choose_recipe_from_search(query):
    """
    Search for recipes and choose one from the results.

    Args:
        query (str): Search query.

    Returns:
        str: URL of the chosen recipe.
    """
    recipes = search_recipes(query)
    choices = [f"{title} ({url})" for title, url in recipes] + ["Quit"]

    questions = [
        inquirer.List(
            "recipe",
            message="Select a recipe to view",
            choices=choices
        )
    ]

    answers = inquirer.prompt(questions)
    if answers["recipe"] == "Quit":
        return None

    selected_recipe = answers["recipe"]
    selected_url = selected_recipe.split('(')[-1][:-1]

    return selected_url


def view_recipe_online(recipe_url: str) -> None:
    """
    Fetches and displays a recipe from a given URL.

    Args:
        recipe_url (str): URL of the recipe to display.
    """
    response = requests.get(recipe_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('.recipe-summary__h1').text.strip()
    ingredients = [li.text.strip() for li in soup.select('.recipe-ingred_txt') if li.text.strip()]
    instructions = [step.text.strip() for step in soup.select('.recipe-directions__list--item') if step.text.strip()]

    md_content = f"# {title}\n\n## Ingredients\n" + "\n".join(
        [f"- {ing}" for ing in ingredients]) + "\n\n## Instructions\n" + "\n".join(
        [f"{i + 1}. {inst}" for i, inst in enumerate(instructions)])

    print_markdown(md_content)


def get_console_width() -> int:
    """Get the current width of the console, with a maximum limit."""
    return min(shutil.get_terminal_size().columns, 80)


def clear_console() -> None:
    """Clear the console."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux, macOS)
        os.system('clear')


def format_file_name(recipe_title: str) -> str:
    """
    Converts the recipe title to a nice format.

    :param recipe_title: a string containing a recipe title.
    :return: formatted title
    :rtype: string
    """
    s = list(recipe_title.lower())

    for i, char in enumerate(s):
        if char.isspace():
            s[i] = "-"
    return "".join(s)


def save_recipe_to_markdown(recipe_url: str, yaml_settings):
    """
    Scrapes recipe URL and saves to markdown file.

    :param recipe_url: a url string from a recipe website
    :param yaml_settings: a dictionary containing settings for a recipe

    :rtype: string
    :return: path to file
    """
    try:
        scraper = scrape_me(recipe_url)
    except Exception as e:
        console.print(f"\nCould not scrape recipe, error: {str(e)}", style="bright_cyan bold")
    directory = yaml_settings.get("directory")
    # if not os.path.exists(directory):
    #   os.makedirs(directory, mode="0o777")
    title = scraper.title().replace(" ", "-")
    recipe_file = directory + "/" + format_file_name(title) + ".md"

    with open(recipe_file, "w+") as text_file:
        print(f"# {title}", file=text_file)

        if yaml_settings["yield"] != False:
            print(f"**Serves:** {scraper.yields()}", file=text_file)
        if yaml_settings["time"] != False:
            print(f"**Total Time:** {scraper.total_time()} mins", file=text_file)

        print(f"\n## Ingredients", file=text_file)

        for ingredient in scraper.ingredients():
            print(f"-", ingredient, file=text_file)

        print(f"\n## Instructions", file=text_file)

        for index, instruction in enumerate(scraper.instructions_list()):
            print(f"{index+1}.", instruction, file=text_file)

    return recipe_file


def print_markdown(md_content: str) -> None:
    """Prints markdown content with a dynamically limited width."""
    clear_console()
    console_width = get_console_width()
    console = Console(width=console_width)
    md = Markdown(md_content)
    console.print('\n', md, '\n')


def view_recipe(recipe_url: str, yaml_settings: dict, prompt_save=True) -> None:
    """
    Scrapes a recipe URL and prints a markdown-formatted recipe to terminal output.

    Args:
        recipe_url (str): A URL string from a recipe website.
        yaml_settings (dict): Settings loaded from a YAML configuration file.
        prompt_save (bool): Whether to prompt the user to save the recipe.
    """
    try:
        file_path = save_recipe_to_markdown(recipe_url, yaml_settings)
        if not file_path:
            return

        with open(file_path, "r") as f:
            md_content = f.read()

        print_markdown(md_content)

        if prompt_save:
            after_view_question = [
                inquirer.List(
                    "after_view",
                    message="What would you like to do next?",
                    choices=["Save this recipe", "Quit"]
                )
            ]

            after_view_answer = inquirer.prompt(after_view_question)
            if after_view_answer["after_view"] == "Save this recipe":
                try:
                    save_recipe_to_markdown(recipe_url, yaml_settings)
                    console.print("\nRecipe saved successfully.\n", style="bright_green")
                except Exception as e:
                    console.print(f"\nError saving the recipe: {str(e)}\n", style="bright_red")
            elif after_view_answer["after_view"] == "Quit":
                return
    except FileNotFoundError:
        console.print("\nMarkdown file not found.\n", style="bright_red")
    except IOError as e:
        console.print(f"\nI/O error({e.errno}): {e.strerror}\n", style="bright_red")
    except Exception as e:
        console.print(f"\nAn error occurred: {str(e)}\n", style="bright_red")


def save_list_of_recipes(url: str, settings: dict) -> None:
    """
    Reads a file containing a list of recipe URLs and saves each recipe to markdown.

    Args:
        url (str): Path to the file containing the list of URLs.
        settings (dict): Settings loaded from a YAML configuration file.

    Raises:
        FileNotFoundError: If the URL file or directory specified in settings is not found.
        IOError: If there is an I/O error when reading the file.
        Exception: For any other errors that occur.
    """
    try:
        os.chdir(settings["directory"])
    except FileNotFoundError:
        console.print("\nDirectory not found. Please check the settings.\n", style="bright_red")
        raise
    except Exception as e:
        console.print(f"\nAn error occurred while changing directory: {str(e)}\n", style="bright_red")
        raise

    try:
        with open(url, "r") as f:
            for line in f:
                single_url = line.strip().rstrip("\n")
                try:
                    save_recipe_to_markdown(single_url, settings)
                except Exception as e:
                    console.print(
                        f"\nError saving recipe from URL: {single_url}. Error: {str(e)}\n",
                        style="bright_red",
                    )
    except FileNotFoundError:
        console.print("\nURL file not found. Please provide a valid file path.\n", style="bright_red")
        raise
    except IOError as e:
        console.print(f"\nI/O error({e.errno}): {e.strerror}\n", style="bright_red")
        raise
    except Exception as e:
        console.print(f"\nAn error occurred: {str(e)}\n", style="bright_red")
        raise


def browse_recipes():
    """
    Allow user to browse previously-saved recipes.
    User can choose 1 to view in terminal.
    """
    while True:
        # Load settings from YAML file
        with open("config.yaml", "r") as file:
            settings = yaml.safe_load(file)

        directory = settings.get("directory")
        if not directory:
            console.print("\nDirectory not specified in the settings.\n", style="bright_red")
            return

        files_to_paths = {}
        titles = []

        # Gather markdown files and their paths
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            file_path = os.path.join(directory, filename)
            if filename.endswith(".md"):
                files_to_paths[filename] = file_path
                with open(file_path, "r") as f:
                    title = f.readline().lstrip("#").strip()
                    titles.append(f"{title} ({filename})")

        if not titles:
            console.print("\nNo markdown files found in the specified directory.\n", style="bright_red")
            return

        # Prompt user to select a recipe
        questions = [
            inquirer.List(
                "recipe",
                message="Select a recipe to view",
                choices=titles + ["Quit"]
            )
        ]

        answers = inquirer.prompt(questions)
        if answers["recipe"] == "Quit":
            break

        selected_title = answers["recipe"]
        selected_filename = selected_title.split(" (")[-1][:-1]
        file_path = files_to_paths[selected_filename]

        # Display the selected recipe
        try:
            with open(file_path, "r") as f:
                md_content = f.read()
            print_markdown(md_content)
        except Exception as e:
            console.print(f"\nError reading the file: {str(e)}\n", style="bright_red")

        # Offer to go back to the menu
        back_to_menu_question = [
            inquirer.List(
                "back_to_menu",
                message="What would you like to do next?",
                choices=["Back to menu", "Quit"]
            )
        ]

        back_to_menu_answer = inquirer.prompt(back_to_menu_question)
        if back_to_menu_answer["back_to_menu"] == "Quit":
            break


def load_yaml() -> dict:
    """
    Loads yaml settings. Searches for a config file, creating one if not present.

    :rtype: dictionary
    :return: mappings for each setting. ex: {time: 'true'}
    """

    config_dir = os.path.join(platformdirs.user_config_dir(), "pure_recipe")
    config_path = "config.yaml"

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    os.chdir(config_dir)

    # Create the file if it doesn't exist
    if not os.path.exists(config_path):
        with open(config_path, "a"):
            os.utime(config_path)

    # Open the file since we can be sure it exists now
    with open(config_path, "r") as file:
        settings = yaml.safe_load(file)

    # Catch an empty file, even if it wasn't just created
    if settings is None:
        settings = dict()
        settings["directory"] = None

    # Generate and update the recipe directory if it doesn't exist
    recipe_directory = settings.get("directory")
    if not os.path.exists(recipe_directory):
        os.makedirs(recipe_directory)
        print('Created new folder for saving recipes at:' + recipe_directory)

    # Generate and update the time and yield options if they don't exist
    if settings.get("time") is None or "":
        settings["time"] = "true"
    if settings.get("yield") is None or "":
        settings["yield"] = "true"

    # Update the settings file with the changed field(s)
    return settings


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the Pure Recipe program.

    This function sets up an argument parser for the Pure Recipe program,
    which is designed to make recipes pretty again. It defines two arguments:
    - `operations`: A required positional argument that specifies the operation
      to be performed. It must be one of "view", "save", "list", or "browse".
    - `url`: An optional positional argument that specifies a URL. If not provided,
      it defaults to "foo".

    Returns:
        Namespace: An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="Pure Recipe", description="Make recipes pretty again."
    )

    parser.add_argument("operations", choices=["view", "save", "list", "browse", "search"])
    parser.add_argument("url", default="foo", nargs="?")

    return parser.parse_args()


if __name__ == "__main__":
    main()
