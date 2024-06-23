from bs4 import BeautifulSoup
import requests
import os

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_images_with_pagination(base_url, search_term, headers, directory, prefix, max_images):
    session = requests.Session()
    session.headers.update(headers)
    page = 1
    count = 0

    while count < max_images:
        url = f"{base_url}/search/{search_term}/?page={page}"
        response = session.get(url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'lxml')
        img_links = soup.select('img[src^="https://images.pexels.com/photos"]')
        
        if not img_links:
            break
        
        for img_link in img_links:
            if count >= max_images:
                break
            img_url = img_link['src']
            img_name = f"{directory}/{prefix}_{count}.jpg"
            try:
                img_data = session.get(img_url).content
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)
                count += 1
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")
        
        page += 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://www.pexels.com/'
}

animal_types = ['cat', 'dog', 'bird']
base_url = 'https://www.pexels.com'
save_dir = 'C:/Users/PC/Documents/AnimalImages'

for animal in animal_types:
    create_directory(f"{save_dir}/{animal.capitalize()}s")
    download_images_with_pagination(base_url, animal, headers, f"{save_dir}/{animal.capitalize()}s", animal.capitalize(), 2000)
