from recipe_scrapers import scrape_me
from rich.console import Console
from rich.markdown import Markdown
import argparse
import yaml
import os
import platformdirs

console = Console()


"""
Load settings from yaml config file.
Prints message if no config file.
"""
try:
    with open("config.yaml", "r") as file:
        settings = yaml.safe_load(file)
except:
    # Config file automatically created in try block.
    print("A config.yaml file has been created in ~/.config/pure-recipe.")
    print("Please add a path to the config file to save your recipes.")
    print("No directory needed if viewing recipes in the terminal.")
    quit()


def main():
    """
    Flow for the application.

    Depending on the arguments, we either view or save the corresponding recipe.

    Or, we can browse previously saved recipes.
    """

    parser = argparse.ArgumentParser(
        prog="Pure Recipe", description="Make recipes pretty again."
    )

    parser.add_argument("operations", choices=["view", "save", "list", "browse"])
    parser.add_argument("url", default="foo", nargs="?")

    args = parser.parse_args()
    url = args.url

    if args.operations == "view":
        try:
            view_in_terminal(url)
        except:
            console.print("\nUh oh! There was an error.", style="bright_red bold")
            print("\nUsage:")
            print("python pure-recipe.py view https://recipes.com/sample-recipe")
            console.print("\nTry again, or see documentation for more info.\n")

    if args.operations == "save":
        try:
            save_to_markdown(url)
        except:
            console.print("\nUh oh! There was an error.", style="bright_red bold")
            print("\nUsage:")
            print("python pure-recipe.py save https://recipes.com/sample-recipe")
            console.print("\nTry again, or see documentation for more info.\n")

    if args.operations == "list":
        f = open(url, "r")
        for line in f:
            try:
                single_url = line.strip().rstrip("\n")
                save_to_markdown(single_url)
            except:
                console.print(
                    "\nFile error. Try again using proper file format. See documentation.\n",
                    style="bright_red",
                )

    if args.operations == "browse":
        browse_recipes()


def format_file_name(recipe_title):
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


def save_to_markdown(recipe_url):
    """
    Scrapes recipe URL and saves to markdown file.

    :param url: a url string from a recipe website

    :rtype: string
    :return: path to file
    """
    load_config()

    scraper = scrape_me(recipe_url)
    directory = settings.get("directory")
    if not os.path.exists(directory):
        os.makedirs(directory, mode="0o777")
    title = scraper.title()
    recipe_file = directory + format_file_name(title) + ".md"

    with open(recipe_file, "w+") as text_file:
        print(f"# {title}", file=text_file)
        print(f"**Serves:** {scraper.yields()}", file=text_file)
        print(f"**Total Time:** {scraper.total_time()} mins", file=text_file)
        print(f"\n## Ingredients", file=text_file)
        for ingredient in scraper.ingredients():
            print(f"-", ingredient, file=text_file)
        print(f"\n## Instructions", file=text_file)
        for index, instruction in enumerate(scraper.instructions_list()):
            print(f"{index+1}.", instruction, file=text_file)

    return recipe_file


def print_markdown(md):
    console.print("\n")
    console.print(md)
    console.print("\n")
    return True


def view_in_terminal(recipe_url):
    """
    Scrapes recipe url and returns markdown-formatted recipe to terminal output.


    :param url: a url string from a recipe website
    :rtype: bool
    :return: True if successful, False otherwise.
    """
    try:
        file_path = save_to_markdown(recipe_url)
        f = open(file_path, "r")
        md = Markdown(f.read())
        print_markdown(md)
        os.remove(file_path)
    except:
        console.print("\nError in view_in_terminal function.\n", style="bright_red")
        return False

    return True


def browse_recipes():
    """
    Provides user with previously-saved recipe options.
    User can choose 1 to view in terminal.
    """
    with open("config.yaml", "r") as file:
        settings = yaml.safe_load(file)

    directory = settings.get("directory")

    print(directory)

    files_to_paths = {}

    def print_titles(recipe_path):
        with open(recipe_path, "r") as f:
            title = f.readline().lstrip("#")
            console.print((index + 1), title, style="green")

    # Add files to file_to_paths dictionary
    # And print each filename for selection
    for index, file in enumerate(os.listdir(directory)):
        filename = os.fsdecode(file)
        file_path = directory + filename
        if filename.endswith(".md") or filename.endswith(".txt"):
            files_to_paths.update({filename: file_path})
            print_titles(file_path)

    def choose_recipe():
        file_path = ""

        inp = input("Enter a number to choose a recipe. Or, enter 'q' to quit.\n")

        if inp == "q":
            exit()

        try:
            choice = int(inp) - 1
            file_path = list(files_to_paths.values())[choice]
        except:
            console.print("\nInput error. Try again.\n", style="bright_red")
            choose_recipe()

        if file:
            f = open(file_path, "r")
            md = Markdown(f.read())
            print_markdown(md)

    choose_recipe()


def load_config():
    """
    Loads the config settings for saving recipe files.
    """
    config_path = platformdirs.user_config_path(appname="pure-recipe")

    try:
        os.chdir(config_path)
    except:
        os.mkdir(config_path)
        os.chdir(config_path)

    directory = settings.get("directory")

    if directory == "":
        print("Please add a path to the config file to save your recipes.")
        print("Then, try again.")
        quit()


if __name__ == "__main__":
    main()
