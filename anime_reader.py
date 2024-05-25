import requests
import re

def fetch_anime_data(page=1):
    url = 'https://graphql.anilist.co'
    query = '''
    query ($page: Int) {
        Page(page: $page, perPage: 50) {
            media(type: ANIME, sort: SCORE_DESC) {
                title {
                    romaji
                    english
                    native
                }
                description
            }
        }
    }
    '''
    variables = {'page': page}
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()

def clean_html(raw_html):
    clean_text = re.sub(r'<.*?>', '', raw_html)  # Remove HTML tags
    return clean_text

def main():
    all_anime_strings = []
    page = 1
    while page <= 2:  # To get top 100 anime, since 50 per page
        data = fetch_anime_data(page)
        for anime in data['data']['Page']['media']:
            title = anime['title']['english'] or anime['title']['romaji']
            description = anime['description'] or ""
            cleaned_description = clean_html(description)
            anime_string = f"Title: {title}\nDescription: {cleaned_description}"
            all_anime_strings.append(anime_string)
        page += 1

    # Print a sample to verify
    # for i, anime in enumerate(all_anime_strings[:5]):
    #     print(f"Anime {i+1}:\n{anime}\n")

    return all_anime_strings

if __name__ == "__main__":
    anime_data_list = main()
    print(anime_data_list)
