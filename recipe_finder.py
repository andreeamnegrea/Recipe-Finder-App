import requests
import os

# Function to fetch recipes from API based on ingredient
def recipe_search(ingredient):
    recipe_app_id = '3423be68'
    recipe_app_key = 'c1008d04e643b0385dbea8ee789bce92'
    result = requests.get(
'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient, recipe_app_id,
recipe_app_key)
)
    data = result.json()
    return data['hits']

# Function to display recipes
def display_recipes(results):
    for index, result in enumerate(results, start=1):
        recipe = result['recipe']
        print(f"{index}. Recipe: {recipe['label']}")
        print("Ingredients:")
        ingredients_list = "\n - ".join(recipe['ingredientLines'])
        print(f" - {ingredients_list}")
        print(f"Link: {recipe['uri']}\n")
    return results

# Function to display detailed recipe information
def display_recipe_details(recipe):
    print(f"\nRecipe: {recipe['label']}")
    print("Ingredients:")
    ingredients_list = "\n - ".join(recipe['ingredientLines'])
    print(f" - {ingredients_list}")
    print(f"Link: {recipe['uri']}")
    print(f"Source: {recipe.get('source', 'N/A')}")

    try:
        calories = float(recipe.get('calories', 0))
        totalWeight = float(recipe.get('totalWeight', 0))
    except ValueError:
        calories = 0
        totalWeight = 0
    print(f"Calories: {calories:.2f}")
    print(f"Total Weight: {totalWeight:.2f} grams")
    print(f"Total Time: {recipe.get('totalTime', 'N/A')} minutes\n")
    return recipe

# Function to save a single recipe to a file
def save_single_recipe(recipe, filename='recipes.txt'):
    recipe_to_save = f"Recipe: {recipe['label']}\n"
    recipe_to_save += "Ingredients:\n"
    for ingredient in recipe['ingredientLines']:
        formatted_ingredient = ingredient.lstrip("- ")
        recipe_to_save += f"- {formatted_ingredient}\n"
    recipe_to_save += f"Link: {recipe['uri']}\n"
    recipe_to_save += f"Source: {recipe.get('source', 'N/A')}\n"
    recipe_to_save += f"Calories: {recipe.get('calories', 'N/A'):.2f}\n"
    recipe_to_save += f"Total Weight: {recipe.get('totalWeight', 'N/A'):.2f} grams\n"
    recipe_to_save += f"Total Time: {recipe.get('totalTime', 'N/A')} minutes\n\n"

    with open(filename, 'r') as file:
        if recipe_to_save in file.read():
            print("\nRecipe already saved.")
            return

    with open(filename, 'a') as file:
        file.write(recipe_to_save)
        print("\nRecipe saved successfully!")


# Function to load recipes from a file
def load_recipes_from_file(filename='recipes.txt'):
    recipes = []
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            recipe = {}
            for line in file:
                line = line.strip()
                
                if line.startswith("Recipe:"):
                    if recipe:
                        recipes.append({"recipe": recipe})
                    recipe = {"label": line[len("Recipe: "):], "ingredientLines": [], "uri": "", "source": "", "calories": 0, "totalWeight": 0, "totalTime": 0}
                
                elif line.startswith("- "):  # Ingredient lines
                    # Ensure to strip only one leading dash and space
                    cleaned_line = line.lstrip("- ")
                    recipe["ingredientLines"].append(cleaned_line)
                
                elif line.startswith("Link:"):
                    recipe["uri"] = line[len("Link: "):]
                
                elif line.startswith("Source:"):
                    recipe["source"] = line[len("Source: "):]
                
                elif line.startswith("Calories:"):
                    recipe["calories"] = float(line[len("Calories: "):])
                
                elif line.startswith("Total Weight:"):
                    recipe["totalWeight"] = float(line[len("Total Weight: "):].split()[0])
                
                elif line.startswith("Total Time:"):
                    recipe["totalTime"] = float(line[len("Total Time: "):].split()[0])
            
            if recipe:
                recipes.append({"recipe": recipe})

    return recipes

# Function to order recipes by total calories or total weight
def order_recipes(recipes):
    # build dictionary from returned items
    my_dict = {"Name": [], "URL": [], "Calories": [], "TotalWeight": []}
    for recipe in recipes:
        recipe = recipe['recipe']

        my_dict["Name"].append(recipe['label'])
        my_dict["URL"].append(recipe['url'])
        my_dict["Calories"].append(recipe['calories'])
        my_dict["TotalWeight"].append(recipe['totalWeight'])

# Sorted list of Calories
    sorted_calorie_items = sorted(enumerate(my_dict['Calories']), key=lambda x: x[1])

# Sorted list of Total Weight
    sorted_weight_items = sorted(enumerate(my_dict['TotalWeight']),key=lambda x: x[1])

    exit_loop=True
    while exit_loop==True:
        recipe_menu = input("""Please select one of the following options:
            1 - Order Recipes by Total Calories
            2 - Order Recipes by Total Weight
            e - Exit         
        """)

        if recipe_menu == "1":
            print("Recipes Sorted by Total Calories")
            sorted_recipes = [recipes[i] for i, _ in sorted_calorie_items]
            for index, (i, _) in enumerate(sorted_calorie_items):
                print(f"{index + 1}. {my_dict['Name'][i]} - Calories: {my_dict['Calories'][i]:.2f}")
            return sorted_recipes

        elif recipe_menu == "2":
            print("Recipes Sorted by Total Weight")
            sorted_recipes = [recipes[i] for i, _ in sorted_weight_items]
            for index, (i, _) in enumerate(sorted_weight_items):
                print(f"{index + 1}. {my_dict['Name'][i]} - Total Weight: {my_dict['TotalWeight'][i]:.2f} grams")
            return sorted_recipes

        else:
            exit_loop = False
            return recipes
        
# Function to fetch nutrition info from API based on ingredient
def nutrition_info(ingredient):
    nutrition_app_id = '09665a39'
    nutrition_app_key = '97cf3242d59c663fbbe8138064cb67eb'
    result = requests.get(
        'https://api.edamam.com/api/nutrition-data?app_id={}&app_key={}&nutrition-type=logging&ingr={}'.format(
    nutrition_app_id, nutrition_app_key, ingredient)
    )
    
    if result.status_code == 200:
        data = result.json()
        return data
    else:
        print(f"Failed to fetch nutrition data for {ingredient}. Status code: {result.status_code}")
        return None

# Function to display nutrition info for a single ingredient
def display_nutrition_info_ing(ingredient):
    # Call Nutrition API
    nutrition_result = nutrition_info(ingredient)

    # Having to do this because the dictionary is nested
    ingredients = nutrition_result['ingredients'][0]
    ingredients2 = ingredients['parsed'][0]
    ingredients3 = ingredients2['nutrients']

    exit_loop = True
    while exit_loop == True:
        nutrition_menu = input("""Please select one of the following options:
            1 - Health Labels   4 - Vitamins         7 - Carbs
            2 - Cautions        5 - Cholesterol      8 - Fiber      10 - Water
            3 - Fats            6 - Protein          9 - Sugar      e - Exit
        """)

        if nutrition_menu == "1":
            print("Health Labels")
            valueresult = nutrition_result['healthLabels']
            for value in valueresult:
                print(value)
        elif nutrition_menu == "2":
            print("Cautions")
            valueresult = nutrition_result['cautions']
            for value in valueresult:
                print(value)
        elif nutrition_menu == "3":
            print("Fats")
            fats = {
                "Total Fat": ingredients3.get('FAT', {}),
                "Saturated Fat": ingredients3.get('FASAT', {}),
                "Polyunsaturated Fat": ingredients3.get('FAPU', {}),
                "Monounsaturated Fat": ingredients3.get('FAMS', {})
            }
            for fat_type, fat_value in fats.items():
                print(f"label: {fat_type}")
                print(f"quantity: {fat_value.get('quantity', 'N/A')}")
                print(f"unit: {fat_value.get('unit', '')}\n")
        elif nutrition_menu == "4":
            print("Vitamins")
            vitamins = {
                "Vitamin A": ingredients3.get('VITA_RAE', {}),
                "Vitamin E": ingredients3.get('TOCPHA', {}),
                "Riboflavin (B2)": ingredients3.get('RIBF', {}),
                "Thiamine (B1)": ingredients3.get('THIA', {}),
                "Niacin (B3)": ingredients3.get('NIA', {}),
                "Vitamin C": ingredients3.get('VITC', {}),
                "Vitamin B6": ingredients3.get('VITB6A', {}),
                "Vitamin B12": ingredients3.get('VITB12', {}),
                "Vitamin K": ingredients3.get('VITK1', {}),
                "Folate (Food)": ingredients3.get('FOLFD', {}),
                "Folic Acid": ingredients3.get('FOLAC', {}),
                "Dietary Folate Equivalents": ingredients3.get('FOLDFE', {}),
                "Potassium": ingredients3.get('K', {}),
                "Phosphorus": ingredients3.get('P', {}),
                "Sodium": ingredients3.get('NA', {}),
                "Zinc": ingredients3.get('ZN', {}),
                "Calcium": ingredients3.get('CA', {}),
                "Magnesium": ingredients3.get('MG', {}),
                "Iron": ingredients3.get('FE', {})
            }
            for vitamin, value in vitamins.items():
                print(f"label: {vitamin}")
                print(f"quantity: {value.get('quantity', 'N/A')}")
                print(f"unit: {value.get('unit', '')}\n")
        elif nutrition_menu == "5":
            print("Cholesterol")
            valueresult = ingredients3['CHOLE']
            for key, value in valueresult.items():
                print(" " + f"{key}: {value}")
        elif nutrition_menu == "6":
            print("Protein")
            valueresult = ingredients3['PROCNT']
            for key, value in valueresult.items():
                print(" " + f"{key}: {value}")
        elif nutrition_menu == "7":
            print("Carbs")
            valueresult = ingredients3['CHOCDF']
            for key, value in valueresult.items():
                print(" " + f"{key}: {value}")
        elif nutrition_menu == "8":
            print("Fiber")
            valueresult = ingredients3['FIBTG']
            for key, value in valueresult.items():
                print(" " + f"{key}: {value}")
        elif nutrition_menu == "9":
            print("Sugar")
            valueresult = ingredients3['SUGAR']
            for key, value in valueresult.items():
                print(" " + f"{key}: {value}")
        elif nutrition_menu == "10":
            print("Water")
            valueresult = ingredients3['WATER']
            for key, value in valueresult.items():
                print(" " + f"{key}: {value}")
        else:
            exit_loop = False

# Function to get nutrition info for the recipe
def get_recipe_nutrition(ingredient_lines):
    nutrition_app_id = '09665a39'
    nutrition_app_key = '97cf3242d59c663fbbe8138064cb67eb'
    url = 'https://api.edamam.com/api/nutrition-details?app_id={}&app_key={}'.format(nutrition_app_id, nutrition_app_key)
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'ingr': ingredient_lines
    }
    
    result = requests.post(url, json=body, headers=headers)
    if result.status_code == 200:
        return result.json()
    else:
        print(f"Failed to fetch nutrition data. Status code: {result.status_code}")
        return None

# Function to display nutrition info for the recipe
def display_nutrition_info(recipe):
    nutrition_data = get_recipe_nutrition(recipe['ingredientLines'])
    if not nutrition_data:
        print(f"No detailed nutrition information available for '{recipe['label']}'")
        return

    def print_nutrition_data(data, indent=0):
        for key, value in data.items():
            if isinstance(value, dict):
                label = value.get('label', key)
                quantity = value.get('quantity', 'N/A')
                unit = value.get('unit', '')
                print(" " * indent + f"{label}: {quantity:.2f} {unit}")
            else:
                print(" " * indent + f"{key}: {value}")

    nutrients = nutrition_data.get('totalNutrients', {})
    if not nutrients:
        print("No nutrient information available.")
        return

    print(f"Nutrition Information for {recipe['label']}:")

    nutrient_categories = {
        "Calories": "ENERC_KCAL",
        "Fats": ["FAT", "FASAT", "FATRN", "FAMS", "FAPU"],
        "Carbohydrates": ["CHOCDF", "FIBTG", "SUGAR"],
        "Protein": "PROCNT",
        "Vitamins": ["VITA_RAE", "VITC", "THIA", "RIBF", "NIA", "VITB6A", "FOLDFE", "FOLFD", "VITB12", "VITD", "TOCPHA", "VITK1"],
        "Minerals": ["CA", "MG", "K", "FE", "ZN", "P", "NA"]
    }

    for category, keys in nutrient_categories.items():
        print(f"\n{category}:")
        if isinstance(keys, list):
            for key in keys:
                if key in nutrients:
                    print_nutrition_data({key: nutrients[key]}, indent=2)
        else:
            if keys in nutrients:
                print_nutrition_data({keys: nutrients[keys]}, indent=2)

# Main function
def main():
    post_save_option = "11"
    last_search_results = None  # To store the last search results
    print("\nWelcome to the Recipe Finder App!")
    # Main menu
    while True:
        main_menu = input("""\nMain Menu\nPlease select one of the following options:
1 - Saved recipes
2 - Enter an ingredient
3 - Exit\n
""").lower()

        # Option 1: Display saved recipes
        if main_menu == "1":
            recipes = load_recipes_from_file()
            if not recipes:
                print("\nOops! You don't have any recipes saved yet. Choose another option from the main menu.\n")
            else:
                display_recipes(recipes)
                
                # Loop to view and interact with saved recipes
                while True:
                    try:
                        recipe_number = int(input("Enter the number of the recipe you want to see details for.\nEnter 0 to go back to the main menu. \n"))
                    except ValueError:
                        print("Invalid input. Please enter a number.\n")
                        continue

                    print()
                    if 1 <= recipe_number <= len(recipes):
                        recipe = display_recipe_details(recipes[recipe_number - 1]['recipe'])
                        
                        # Option to view nutrition info of the recipe
                        nutrition_recipe = input("\nDo you want to see the recipe's nutrition info? Y/N:\n ").lower()
                        if nutrition_recipe == "y":
                            display_nutrition_info(recipe)
                        
                        # New options after showing the saved recipe
                        post_view_option = input("""\nWhat would you like to do next?
1 - Come back to the saved recipes
2 - Go back to the main menu
                """).lower()
                        if post_view_option == "1":
                            display_recipes(recipes)
                            continue
                        elif post_view_option == "2":
                            break
                    elif recipe_number == 0:
                        break
                    else:
                        print("\nInvalid number. Please choose a valid recipe number.")
                        continue
        
        # Option 2: Search for recipes by ingredient
        elif main_menu == "2":
            while True:
                ingredient = input("\nEnter the name of an ingredient: ").lower()

                # Option to view nutrition info of the ingredient
                nutrition_info_ingr = input("\nDo you want to see the nutrition info for this ingredient? Y/N\n").lower()
                if nutrition_info_ingr == "y":
                    display_nutrition_info_ing(ingredient)

                 # Search for recipes with the given ingredient
                results = recipe_search(ingredient)
                last_search_results = results  # Store the last search results
                
                if not results:
                    print(f"No recipes found for '{ingredient}'. Please try again with a different ingredient.")
                    continue
                
                 # Loop to view and interact with search results
                while True:
                    display_recipes(results)
                    sort_search = input("Do you want to order the recipes by Calories or Total Weight? Y/N \n").lower()
                    if sort_search == "y":
                        ordered_results = order_recipes(results)
                    else:
                        ordered_results = results

                    try:
                        recipe_number = int(input("\nEnter the number of the recipe you want to see details for.\nEnter 0 to go to the main menu. \n"))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue

                    if 1 <= recipe_number <= len(ordered_results):
                        recipe = display_recipe_details(ordered_results[recipe_number - 1]['recipe'])

                        # Option to view nutrition info of the recipe
                        nutrition_recipe = input("Do you want to see the recipe's nutrition info? Y/N:\n ").lower()
                        if nutrition_recipe == "y":
                            display_nutrition_info(recipe)

                        # Option to save the recipe
                        save_option = input("Do you want to save this recipe? Y/N\n").lower()
                        if save_option == "y":
                            save_single_recipe(recipe)
                            
                            # New options after saving the recipe
                            post_save_option = input("""\nWhat would you like to do next?
1 - Come back to the last search
2 - Search for another ingredient
3 - Go back to the main menu
4 - Exit
""").lower()
                            if post_save_option == "1":
                                results = last_search_results
                                continue
                            elif post_save_option == "2":
                                break
                            elif post_save_option == "3":
                                return main()
                            elif post_save_option == "4":
                                print("\nThank you for using the Recipe Finder App. Goodbye!")
                                return
                        continue
                    elif recipe_number == 0:
                        break

                    else:
                        print("Invalid number. Please choose a valid recipe number.")
                        continue
                # This break ensures you can search for another ingredient without going back to the main menu
                if post_save_option == "2":
                    continue
                break
        
        # Option 3: Exit the app
        elif main_menu == "3":
            print("\nThank you for using the Recipe Finder App. Goodbye!")
            break

        # Handle invalid input in the main menu
        else:
            print("\nInvalid input. Please try again.")

main()