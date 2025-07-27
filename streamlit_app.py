import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def download_single_image(url):
    try:
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        timestamp = int(time.time() * 1000)
        separator = '&' if '?' in url else '?'
        url_with_timestamp = f"{url}{separator}nocache={timestamp}"
        
        proxies = {
            'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080',
        }
        response = requests.get(url_with_timestamp, proxies=proxies, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        return None
    except Exception as e:
        return None

def download_images_parallel():
    base_url = "https://alfredplpl.github.io/img/without_copyright.png"
    
    urls = [base_url for _ in range(4096)]
    images = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=32) as executor:
        future_to_url = {executor.submit(download_single_image, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as e:
                print(f"{str(e)}")
    
    total_time = time.time() - start_time
    st.title("🎈 My new app")
    st.write(
        f"{total_time:.2f}second"
    )
    
    return images

download_images_parallel()


