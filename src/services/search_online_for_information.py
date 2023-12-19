import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_clean_text_from_url(url, char_limit=3000):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from specific tags
        texts = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'section', 'span']):
            texts.append(tag.get_text(separator=' ', strip=True))

        # Join and truncate the text
        page_text = ' '.join(texts)
        return page_text[:char_limit]  # Truncate to char_limit
    except Exception as e:
        return f"Error fetching page: {e}"


def extract_actual_url(redirect_url):
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('uddg', [None])[0]


def is_social_media(url):
    # List of domains to exclude
    social_media_domains = ['x.com', 'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'pinterest.com',  'youtube.com', 'vk.com', 'tiktok.com']
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in social_media_domains)


def search_online_for_information(query, top_k=2):
    if query.lower() == "none":
        return ""
    print(f"the query is {query}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        query = requests.utils.quote(query)
        response = requests.get(f"https://duckduckgo.com/html/?q={query}", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        results = soup.find_all('div', class_='result__body')
        top_texts = []
        count = 0

        for result in results:
            if count >= top_k:
                break  # Stop after top_k non-social media results

            redirect_link = result.find('a', class_='result__url', href=True)['href'] if result.find('a', class_='result__url', href=True) else None
            if redirect_link:
                actual_url = extract_actual_url(redirect_link)
                if actual_url and not is_social_media(actual_url):
                    title = result.find('h2', class_='result__title').get_text(strip=True)
                    page_text = get_clean_text_from_url(actual_url)
                    top_texts.append(f"Title: {title}\nText:\n{page_text}\nURL Reference: {actual_url}\n")
                    count += 1
        # print("Internet Search Result: \n" + "\n\n".join(top_texts))
        return "Internet Search Result: \n" + "\n\n".join(top_texts)
    except requests.RequestException as e:
        return f"Error: Unable to retrieve results for {query}. Details: {str(e)}"

