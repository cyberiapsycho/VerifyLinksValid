from google.colab import files

# upload your files from google.colab
uploaded = files.upload()

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm 

def check_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)  # 设置超时
        return (url, response.status_code == 200)
    except requests.exceptions.RequestException:
        return (url, False)

def main():
    # get the links from the file
    with open('links.txt', 'r') as file:
        links = [line.strip() for line in file if line.strip()]

    # Use a thread pool to check links concurrently
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:  # Set the number of concurrent threads
        future_to_url = {executor.submit(check_link, link): link for link in links}

        # showing the prograss bar
        for future in tqdm(as_completed(future_to_url), total=len(future_to_url), desc="check links"):
            url, is_valid = future.result()
            results[url] = is_valid

    # check the result and output
    invalid_links = [url for url, is_valid in results.items() if not is_valid]
    invalid_link_count = len(invalid_links)  # Count invalid links

    if not invalid_links:
        print("All Works!")
    else:
        print(f"Invalid Links: {invalid_link_count}")
        for link in invalid_links:
            print(link)

if __name__ == "__main__":
    main()
