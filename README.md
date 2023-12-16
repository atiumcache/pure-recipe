# Pure Recipe
### A web-to-markdown recipe viewer.

We're tired of the ads. We're tired of the blog posts. We just want the recipe!

This is a terminal application that allows you to quickly bypass the junk that plagues most recipe websites. Just run the program and _voilà_, a pretty-printed recipe is outputted to your terminal. 

## Usage

### View in Terminal

To view the recipe in the terminal:

	python recipe-to-markdown.py view https://www.seriouseats.com/potato-wedges-recipe-5217319

Example of viewing:

[![asciicast](https://asciinema.org/a/IHjK7v8F3TEVVBMFJoxKcbOuB.svg)](https://asciinema.org/a/IHjK7v8F3TEVVBMFJoxKcbOuB)

### Save to Markdown

To save the recipe to a markdown file: 

	python recipe-to-markdown.py save https://www.seriouseats.com/potato-wedges-recipe-5217319

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


