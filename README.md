# Pure Recipe
### A web-to-markdown recipe viewer.

We're tired of the ads. We're tired of the blog posts. We just want the recipe!

This is a terminal application that allows you to quickly bypass the junk that plagues most recipe websites. Just run the program and _voilà_, a pretty-printed recipe is outputted to your terminal. 

- [Usage](#usage)
	- [View in Terminal](#view-in-terminal)
	- [Save to Markdown](#save-to-markdown)
- [Configuration](#configuration)
	- [Config Template](#config-template)
- [Supported Websites](#supported-websites)
- [Why Create Pure Recipe?](#why-create-pure-recipe)
- [Future Work](#future-work)
- [License](#license)

## Usage

There are two options: view or save. 

### View in Terminal

To view the recipe in the terminal:

	python pure-recipe.py view https://www.seriouseats.com/potato-wedges-recipe-5217319

Example of viewing:

![terminal demonstration](pure-recipe.gif)

### Save to Markdown

To save the recipe to a markdown file: 

	python pure-recipe.py save https://www.seriouseats.com/potato-wedges-recipe-5217319

The default location is `/home/user/Documents/recipes/`. Change this path in the `config.yaml` file, as described below. 

You can turn other settings on/off in the yaml file. 

## Configuration

The program will create a `config.yaml` file upon its first run. Copy and paste the following template into the config file, adding the path to a folder where you want your recipes saved.

### Config Template

	---
	directory: '/home/user/Documents/recipes/'
	time: true 
	yield: true


## Supported Websites

See this link for supported websites: https://github.com/hhursev/recipe-scrapers#scrapers-available-for

## Why Create Pure Recipe?

There does exist other solutions for bypassing ad-filled recipes --- namely, Paprika. However, you are locked into their ecosystem and exporting the recipes can be troublesome. Plus, there is a subscription fee to use the app on multiple ecosystems/devices. 

With Pure Recipe, you can be in charge of your own digital recipe book. By saving the files in Markdown format, you can quickly transfer recipes to a new device. Or, share your well-formatted recipes with family and friends without forcing them to download a propietary app. 

## Future Work

- Error catching for invalid inputs.
- Different color themes.
- Ability to pass in a list of URLs to save, all at once.
- Search for recipes from the terminal.

## License

Distributed under the MIT License. See LICENSE.txt for more information.
