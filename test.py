from pure_recipe import main, format_file_name, save_to_markdown, view_in_terminal, load_config


def test_format_file_name():
    recipe_title = "Chocolate Chip Cookies"
    assert format_file_name(recipe_title) == "chocolate-chip-cookies"


