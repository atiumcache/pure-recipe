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

## Installation

Download `pure_recipe.py` and `requirements.txt` from this repository.

Then, install the dependencies from `pip`:

	pip install -r requirements.txt

Alternatively, you can install each dependency manually:

	pip install rich
	pip install recipe_scrapers
	pip install pyyaml

## Usage

There are four options: `view`, `save`, `list`, or `browse`. 

### View in Terminal

To view the recipe in the terminal:

	python pure_recipe.py view https://www.seriouseats.com/potato-wedges-recipe-5217319

Example of viewing:

![terminal demonstration](pure-recipe.gif)

### Save to Markdown

To save the recipe to a markdown file: 

	python pure_recipe.py save https://www.seriouseats.com/potato-wedges-recipe-5217319

The default location is `/home/user/Documents/recipes/`. Change this path in the `config.yaml` file, as described below. 

You can turn other settings on/off in the yaml file. 

### Save a List of URLs

Have a whole bunch of recipes that you want to save? Just create a `.txt` file with one recipe on each line. Make sure the file is located in your `recipe` directory denoted in your `config` file. Default location is `/home/user/Documents/recipes/`.

Example file called `recipes_list.txt`:

	https://www.seriouseats.com/beef-braciole-recipe-7561806
	https://www.seriouseats.com/basque-cheesecake
	https://www.seriouseats.com/omelette-souffle-with-cheese

Then, run the program as follows:

	python pure_recipe.py list recipes_list.txt

You should see all recipes on the list saved in markdown format.

The default location is `/home/user/Documents/recipes/`. Change this path in the `config.yaml` file, as described below. 

### Browse

Browse previously saved recipes with:

	python pure_recipe.py browse

## Configuration

The program will create a `config.yaml` file upon its first run. The program should create default settings, placing a `recipe` directory in the user's `Documents` directory.

If needed, copy and paste the following template into the config file, changing the path to a folder where you want your recipes saved. 

### Config Template

	---
	directory: '/home/user/Documents/recipes/'
	time: true
	yield: true

Change `time` or `yield` to false if you don't want these options to populate when you save a recipe.

More settings are planned for the future.

## Supported Websites

See this link for supported websites: https://github.com/hhursev/recipe-scrapers#scrapers-available-for

## Why Create Pure Recipe?

There does exist other solutions for bypassing ad-filled recipes --- namely, Paprika. However, you are locked into their ecosystem and exporting the recipes can be troublesome. Plus, there is a subscription fee to use the app on multiple ecosystems/devices. 

With Pure Recipe, you can be in charge of your own digital recipe book. By saving the files in Markdown format, you can quickly transfer recipes to a new device. Or, share your well-formatted recipes with family and friends without forcing them to download a propietary app. 

## Future Work

- More error catching for invalid inputs.
- Unit tests.
- Different color themes.
- ~~Ability to pass in a list of URLs to save, all at once.~~
- Search for recipes from the terminal.
- ~~Browse your saved-recipes folder in the terminal.~~

## License

Distributed under the MIT License. See LICENSE.txt for more information.
