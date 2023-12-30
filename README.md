# Pure Recipe
### A web-to-markdown recipe viewer.

We're tired of the ads. We're tired of the blog posts. We just want the recipe!

This is a terminal application that allows you to quickly bypass the junk that plagues most recipe websites. Just run the program and _voilà_, a pretty-printed recipe is outputted to your terminal. Alternatively, you can save the recipe to a markdown file for later use.

- [Installation](#installation)
- [Usage](#usage)
	- [View in Terminal](#view-in-terminal)
	- [Save to Markdown](#save-to-markdown)
	- [Save a List of URLs](#save-a-list-of-urls)
	- [Browse](#browse)
- [Configuration](#configuration)
	- [Config Template](#config-template)
- [Supported Websites](#supported-websites)
- [Why Create Pure Recipe?](#why-create-pure-recipe)
- [Future Work](#future-work)
- [License](#license)

## Features

- View recipes directly in your terminal.
- Save recipes to markdown for easy access and sharing.
- Support for a wide range of cooking sites.
- Easy-to-use command-line interface.

## Installation

**Prerequisites:**

- Python 3.6 or higher.

**Steps:**

1. Clone the repository or download `pure_recipe.py` and `requirements.txt`.
2. Install the required Python dependencies:
	
 		pip install -r requirements.txt


## Usage

There are four options: `view`, `save`, `list`, or `browse`. 

### View in Terminal

**Command:**

	python pure_recipe.py view [RECIPE_URL]

**Example:**

	python pure_recipe.py view https://www.seriouseats.com/potato-wedges-recipe-5217319

Viewing example:

![terminal demonstration](pure-recipe.gif)

### Save to Markdown

**Command:**

	python pure_recipe.py save [RECIPE_URL]

**Example:**

	python pure_recipe.py save https://www.seriouseats.com/potato-wedges-recipe-5217319

Saves multiple recipes from a list of URLs in a text file. The default location is `/home/user/Documents/recipes/`. Change this path in the `config.yaml` file, as described below. 

### Save a List of URLs

**Command:**

	python pure_recipe.py list [FILE_PATH]

Have a whole bunch of recipes that you want to save? Just create a `.txt` file with one recipe on each line. Make sure the file is located in your `recipe` directory denoted in your `config` file. Default location is `/home/user/Documents/recipes/`.

Consider an example file called `recipes_list.txt`:

	https://www.seriouseats.com/beef-braciole-recipe-7561806
	https://www.seriouseats.com/basque-cheesecake
	https://www.seriouseats.com/omelette-souffle-with-cheese

Then, run the program as follows:

	python pure_recipe.py list recipes_list.txt

You should see all recipes on the list saved in markdown format.

The default location is `/home/user/Documents/recipes/`. Change this path in the `config.yaml` file, as described below. 

### Browse

**Command:**

	python pure_recipe.py browse
 
Browse and view your saved recipes.

## Configuration

The program will create a `config.yaml` file upon its first run. The program should create default settings, placing a `recipe` directory in the user's `Documents` directory.

If needed, copy and paste the following template into the config file, changing the path to a folder where you want your recipes saved. 

### Config Template

	---
	directory: '/path/to/your/recipes/'
	time: true
	yield: true

- `directory`: Path where your recipes are saved.
- `time`: Include preparation and cooking time in the output.
- `yield`: Include the number of servings.

More settings are planned for the future.

## Supported Websites

Check out the [list of supported websites](https://github.com/hhursev/recipe-scrapers#scrapers-available-for) for recipe scraping.

## Troubleshooting

- Dependency Issues: Ensure all dependencies are correctly installed.
- Invalid URLs: Check the URL format and website support.
- File Permissions: Ensure you have write permissions to the specified recipe directory.

## Why Create Pure Recipe?

There does exist other solutions for bypassing ad-filled recipes --- namely, Paprika. However, you are locked into their ecosystem and exporting the recipes can be troublesome. Plus, there is a subscription fee to use the app on multiple ecosystems/devices. 

With Pure Recipe, you can be in charge of your own digital recipe book. By saving the files in Markdown format, you can quickly transfer recipes to a new device. Or, share your well-formatted recipes with family and friends without forcing them to download a propietary app. 

## Future Work

- Adding more robust error handling.
- Implementing unit tests for reliability.
- Introducing different color themes.
- ~~Ability to pass in a list of URLs to save, all at once.~~
- Searching for recipes directly from the terminal.
- ~~Browse your saved-recipes folder in the terminal.~~

## Contributing

Contributions are welcome! If you have a suggestion or want to contribute code, please feel free to make a pull request or open an issue.

## License

Distributed under the MIT License. See LICENSE.txt for more information.
