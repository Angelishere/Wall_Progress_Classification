import os
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
def get_image_urls(search_term, num_images):
    search_url = f"https://www.istockphoto.com/search/2/image?phrase={urllib.parse.quote(search_term)}&tbm=isch"
    # Initialize the WebDriver (ensure you have the appropriate driver installed and in your PATH)
    driver = webdriver.Chrome()
    driver.get(search_url)
    image_urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(image_urls) < num_images:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        image_elements = soup.find_all('img')
        for img in image_elements:
            src = img.get('src')
            if src and 'http' in src:
                image_urls.add(src)
                if len(image_urls) >= num_images:
                    break
        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.quit()
    return list(image_urls)
def save_images(image_urls, search_term):
    save_folder = search_term
    os.makedirs(save_folder, exist_ok=True)
    for i, url in enumerate(image_urls):
        try:
            file_name = os.path.join(save_folder, f"{search_term}_{i}.jpg")
            urllib.request.urlretrieve(url, file_name)
            print(f"Image {i} saved as {file_name}")
        except Exception as e:
            print(f"Failed to download image {i} from {url}. Error: {e}")
# Main code
search_term = input("Enter the keyword: ")
num_images = int(input("Enter the number of images to download: "))
image_urls = get_image_urls(search_term, num_images)
save_images(image_urls, search_term)
