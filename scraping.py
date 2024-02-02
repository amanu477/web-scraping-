import requests
from bs4 import BeautifulSoup
import time

bot_token = '6625808706:AAHKttXjNJpPkmrv2bQ-Tf_sG78fjYvqIHQ'
chat_id = '383065177' # here MR. add your own chat id so you can see what is posted in the bot
website_url = 'https://www.ethiojobs.net/jobs-in-ethiopia/'
previous_result = ""

def get_job_title(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        page = requests.get(url, headers=headers)
        page.raise_for_status() 

        soup = BeautifulSoup(page.content, "html.parser")
        post = soup.find("div", class_="single_listing")

        title = post.find("span", class_="text-left")
        if title:
            return title.text.strip(), url
        else:
            return "Title not found in the post.", None

    except requests.RequestException as e:
        return f"Error during request: {e}", None
    except Exception as e:
        return f"An unexpected error occurred: {e}", None

def send_to_telegram(bot_token, chat_id, text, job_link):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {'chat_id': chat_id, 'text': f"{text}\nLink: {job_link}"}
    requests.post(url, params=params)

def auto_post():
    global previous_result
    while True:
        result, job_link = get_job_title(website_url)
        
        if (result != previous_result) and job_link:
            send_to_telegram(bot_token, chat_id, result, job_link)
            previous_result = result 
            print("New job update posted!")

            time.sleep(300)  # Sleep for 5 minute and check for un update

if __name__ == "__main__":
    auto_post()
