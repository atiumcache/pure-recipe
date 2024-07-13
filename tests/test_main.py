import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import tempfile
import yaml
from pure_recipe import *

from recipe_scrapers import scrape_me

class TestRecipeApp(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="http://example.com/recipe")
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('recipe_scrapers.scrape_me')
    def test_save_recipe_to_markdown(self, mock_scrape_me, mock_exists, mock_makedirs, mock_open):
        mock_scraper = MagicMock()
        mock_scraper.title.return_value = "Test Recipe"
        mock_scraper.yields.return_value = "4 servings"
        mock_scraper.total_time.return_value = 30
        mock_scraper.ingredients.return_value = ["1 cup flour", "2 eggs"]
        mock_scraper.instructions_list.return_value = ["Mix ingredients", "Bake for 20 minutes"]
        mock_scrape_me.return_value = mock_scraper

        settings = {"directory": tempfile.gettempdir(), "yield": True, "time": True}
        recipe_url = "http://example.com/recipe"
        file_path = save_recipe_to_markdown(recipe_url, settings)

        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r") as f:
            content = f.read()
            self.assertIn("# Test-Recipe", content)
            self.assertIn("**Serves:** 4 servings", content)
            self.assertIn("**Total Time:** 30 mins", content)
            self.assertIn("- 1 cup flour", content)
            self.assertIn("1. Mix ingredients", content)

    @patch('builtins.open', new_callable=mock_open, read_data="# Test Recipe\n**Serves:** 4 servings\n**Total Time:** 30 mins\n\n## Ingredients\n- 1 cup flour\n- 2 eggs\n\n## Instructions\n1. Mix ingredients\n2. Bake for 20 minutes")
    @patch('os.path.exists', return_value=True)
    def test_view_recipe(self, mock_exists, mock_open):
        settings = {"directory": tempfile.gettempdir(), "yield": True, "time": True}
        recipe_url = "http://example.com/recipe"
        with patch('inquirer.prompt', return_value={"after_view": "Quit"}):
            view_recipe(recipe_url, settings, prompt_save=False)

    @patch('builtins.open', new_callable=mock_open, read_data="http://example.com/recipe1\nhttp://example.com/recipe2")
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('recipe_scrapers.scrape_me')
    def test_save_list_of_recipes(self, mock_scrape_me, mock_exists, mock_makedirs, mock_open):
        mock_scraper = MagicMock()
        mock_scraper.title.return_value = "Test Recipe"
        mock_scraper.yields.return_value = "4 servings"
        mock_scraper.total_time.return_value = 30
        mock_scraper.ingredients.return_value = ["1 cup flour", "2 eggs"]
        mock_scraper.instructions_list.return_value = ["Mix ingredients", "Bake for 20 minutes"]
        mock_scrape_me.return_value = mock_scraper

        settings = {"directory": tempfile.gettempdir(), "yield": True, "time": True}
        url_file = tempfile.mktemp()
        with open(url_file, "w") as f:
            f.write("http://example.com/recipe1\nhttp://example.com/recipe2")

        save_list_of_recipes(url_file, settings)

        for i in range(1, 3):
            file_path = os.path.join(tempfile.gettempdir(), f"test-recipe{i}.md")
            self.assertTrue(os.path.exists(file_path))
            with open(file_path, "r") as f:
                content = f.read()
                self.assertIn("# Test-Recipe", content)
                self.assertIn("**Serves:** 4 servings", content)
                self.assertIn("**Total Time:** 30 mins", content)
                self.assertIn("- 1 cup flour", content)
                self.assertIn("1. Mix ingredients", content)

    @patch('os.listdir', return_value=["test-recipe.md"])
    @patch('builtins.open', new_callable=mock_open, read_data="# Test Recipe\n**Serves:** 4 servings\n**Total Time:** 30 mins\n\n## Ingredients\n- 1 cup flour\n- 2 eggs\n\n## Instructions\n1. Mix ingredients\n2. Bake for 20 minutes")
    @patch('os.path.exists', return_value=True)
    def test_browse_recipes(self, mock_exists, mock_open, mock_listdir):
        settings = {"directory": tempfile.gettempdir()}
        with patch('inquirer.prompt', side_effect=[{"recipe": "Test Recipe"}, {"back_to_menu": "Quit"}]):
            browse_recipes(settings)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('yaml.safe_load', return_value={"directory": tempfile.gettempdir(), "time": True, "yield": True})
    def test_load_yaml(self, mock_safe_load, mock_exists, mock_makedirs):
        settings = load_yaml()
        self.assertIn("directory", settings)
        self.assertIn("time", settings)
        self.assertIn("yield", settings)

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(operations="view", url="http://example.com/recipe"))
    def test_parse_arguments(self, mock_parse_args):
        args = parse_arguments()
        self.assertEqual(args.operations, "view")
        self.assertEqual(args.url, "http://example.com/recipe")

if __name__ == "__main__":
    unittest.main()
