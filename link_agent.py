import openai
import requests
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
user_id = os.getenv("LINKEDIN_USER_ID")

# Step 1: Generate a post
def generate_post():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Write a professional post about how AI is transforming education"}]
    )
    return response['choices'][0]['message']['content']

# Step 2: Post to LinkedIn
def post_to_linkedin(content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    post_data = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    response = requests.post(url, headers=headers, json=post_data)
    print(response.status_code, response.text)

# Run it
post_to_linkedin(generate_post())
