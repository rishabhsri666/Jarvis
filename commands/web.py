import webbrowser
import urllib.parse


def open_website(site):

    websites = {
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "github": "https://github.com",
        "chatgpt": "https://chat.openai.com"
    }

    if site in websites:

        webbrowser.open(websites[site])

        return True

    return False


def google_search(query):

    url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )

    webbrowser.open(url)


def youtube_search(query):

    url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote(query)
    )

    webbrowser.open(url)