from pure_recipe import PureRecipe


def test_format_file_name():
    recipe = PureRecipe(
        title="Chocolate Chip Cookies",
        # description="A delicious chocolate chip cookie recipe.",
        ingredients=["1 cup of flour", "1/2 cup of chocolate chips"],
        instructions=["Mix ingredients", "Bake at 350 degrees"],
        total_time=10,
        yield_amount=12,
    )
    assert recipe.filename == "chocolate-chip-cookies"


test_format_file_name()
