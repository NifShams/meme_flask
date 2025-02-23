from flask import Flask, render_template
import requests
import random
import json

app = Flask(__name__)

def get_meme():
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        
        response = requests.get('https://www.reddit.com/r/memes/hot.json', headers=headers)
        response.raise_for_status()
        data = response.json()
        
       
        posts = [post['data'] for post in data['data']['children']
                if not post['data']['stickied'] and 
                post['data']['url'].endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        if not posts:
            return None, None
            
       
        post = random.choice(posts)
        
        return post['url'], post['subreddit']
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching meme: {e}")
        return None, None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing meme data: {e}")
        return None, None

@app.route("/")
def index():
    meme_pic, subreddit = get_meme()
    if meme_pic is None:
        return "Error fetching meme. Please try again.", 500
    return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)

if __name__ == "__main__":
    app.run(debug=True)