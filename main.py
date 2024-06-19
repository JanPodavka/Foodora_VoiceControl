import undetected_chromedriver as uc
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from web_control import web_help, web_inject  # Assuming these are custom functions defined in web_control.py


def extract_cuisines(driver):
    cuisines = {}
    try:
        cuisine_elements = driver.find_elements(By.CSS_SELECTOR,
                                                "ul.cuisines-filter__list > li.cuisines-filter__list-item")
        for element in cuisine_elements:
            label = element.find_element(By.TAG_NAME, "label")
            cuisine_name = label.text.strip()
            input_element = label.find_element(By.TAG_NAME, "input")
            cuisines[cuisine_name] = input_element
    except Exception as e:
        print(f"Failed to extract cuisines: {str(e)}")
    return cuisines


def extract_restaurants(driver):
    restaurants = {}
    try:
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        restaurant_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.vendor-list-revamp > li.vendor-tile-new-l")))
        # WebDriverWait(driver, 10)
        # restaurant_elements = driver.find_elements(By.CSS_SELECTOR, "ul.vendor-list-revamp > li.vendor-tile-new-l")
        for element in restaurant_elements:
            name_element = element.find_element(By.CSS_SELECTOR, "div.vendor-name")
            restaurant_name = name_element.text.strip()
            link_element = element.find_element(By.CSS_SELECTOR, "a[href*='/restaurant/']")
            restaurant_link = link_element.get_attribute('href')
            restaurants[restaurant_name] = restaurant_link
            print(restaurant_link)
    except Exception as e:
        print(f"Failed to extract restaurants: {str(e)}")
    return restaurants


def select_cuisine(option, cuisines, driver):
    if option.lower() == "home":
        try:
            home_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.bds-c-navbar__brand > a"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", home_link)
            home_link.click()
            print("Clicked on Home link.")
        except Exception as e:
            print(f"Failed to click on Home link: {str(e)}")
    elif option.lower() == "vyhodne":
        click_checkbox(driver, "offers-filter-checkbox-has_discount-label")
    elif option.lower() == "doprava":
        click_checkbox(driver, "offers-filter-checkbox-has_free_delivery-label")
    else:
        try:
            if option in cuisines:
                checkbox = cuisines[option]
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(1)  # Add a slight delay to ensure scrolling completes
                driver.execute_script("arguments[0].click();", checkbox)
                print(f"Selected cuisine: {option}")
            else:
                print(f"Cuisine '{option}' not found.")
        except Exception as e:
            print(f"Failed to select cuisine '{option}': {str(e)}")


def click_checkbox(driver, label_id):
    try:
        # Wait for the label to be present
        label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, label_id))
        )
        # Scroll the label into view
        driver.execute_script("arguments[0].scrollIntoView(true);", label)
        time.sleep(1)  # Ensure the scroll has completed

        # Use ActionChains to move to the label and click it
        actions = ActionChains(driver)
        actions.move_to_element(label).click().perform()
        print(f"Checkbox label with ID '{label_id}' clicked successfully.")
    except Exception as e:
        print(f"Failed to click the checkbox label with ID '{label_id}': {str(e)}")


def select_restaurant_by_index(driver, restaurants, index):
    try:
        selected_restaurant = list(restaurants.values())[index]
        print(f"Selecting restaurant: {selected_restaurant}")
        # Example: Navigate to the selected restaurant URL
        driver.get(selected_restaurant)
    except IndexError:
        print(f"Invalid index: {index}")
    except Exception as e:
        print(f"Failed to select restaurant: {str(e)}")


def extract_menu_items(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[@data-testid='menu-product']"))
    )
    li_elements = driver.find_elements(By.XPATH, "//li[@data-testid='menu-product']")
    products = []

    for li in li_elements:
        try:
            product_name_element = li.find_element(By.XPATH, ".//span[@data-testid='menu-product-name']")
            product_name = product_name_element.text.strip()
            products.append(product_name)

        except Exception as e:
            print(f"An error occurred while processing an item: {str(e)}")

    # Print the dictionary
    print(products)
    return products


def select_menu_items(driver, index):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[@data-testid='menu-product']"))
    )
    item = driver.find_elements(By.XPATH, "//li[@data-testid='menu-product']")
    item = item[index]
    # Locate the button within the selected li element
    button = item.find_element(By.XPATH, ".//button")

    # Scroll the button into view using JavaScript
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(1)  # Ensure the scroll has completed

    # Use ActionChains to click the button
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()


### MAIN STATES

def main_state1():
    url = "https://www.foodora.cz/restaurants/new?lng=15.08762&lat=50.77045&vertical=restaurants"  # Liberec
    # url = 'https://www.foodora.cz/restaurants/new?lng=14.43972&lat=50.08999&vertical=restaurants' #Praha Florenc
    # Initialize Chrome driver using undetected_chromedriver
    driver = uc.Chrome()

    try:
        ## INIT setup
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.url_to_be(url))
        cuisines = extract_cuisines(driver)
        print("Available cuisines:")
        for cuisine in cuisines.keys():
            print(cuisine)
        resturants = extract_restaurants(driver)
        print(list(resturants.keys()))
        rest_list = list(resturants.keys())
        help_list = ["restaurace"] + list(cuisines.keys()) + ["vyhodne", "doprava", "domů", "ukončit"]
        help_overlay = web_help(help_list, "Vybrané příkazy")
        web_inject(help_overlay, driver)
        for restaurant in resturants.keys():
            print(restaurant)

        # Interaction loop
        try:
            while True:
                driver.current_url  # Check if the browser is still open
                option = input("Enter cuisine name to select (or 'home' to navigate home, 'exit' to quit): ").strip()

                if option.lower() == 'exit':
                    break
                elif option.lower() == 'home':
                    cuisines = extract_cuisines(driver)
                    web_inject(help_overlay, driver)
                elif option.lower() == 'restaurace':
                    rest_list = list(resturants.keys())
                    overlay = web_help(rest_list)
                    web_inject(overlay, driver)
                elif option.isdigit() and int(option) < len(rest_list):
                    select_restaurant_by_index(driver, resturants, int(option))
                    main_state2(driver)
                else:
                    web_inject(help_overlay, driver)
                    select_cuisine(option, cuisines, driver)

                resturants = extract_restaurants(driver)
                time.sleep(1)  # Check every second
        except Exception as e:
            print(f"Exception occurred during interaction: {str(e)}")
    finally:
        driver.quit()


def main_state2(driver):
    menu = extract_menu_items(driver)
    overlay = web_help(menu, "Výběr z menu")
    web_inject(overlay, driver)

    try:
        while True:
            option = input("Enter cuisine name to select (or 'home' to navigate home, 'exit' to quit): ").strip()
            if option.lower() == 'exit':
                break
            elif option.isdigit() and int(option) < len(menu):
               item =  select_menu_items(driver, int(option))
    except Exception as E:
        print(E)


if __name__ == '__main__':
    main_state1()
