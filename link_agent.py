#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Set your keys
openai.api_key = os.getenv("OPENAI_API_KEY")
access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
user_id = os.getenv("LINKEDIN_USER_ID")

# Step 1: Generate content using OpenAI
def generate_post():
    prompt = "Write a professional and engaging LinkedIn post about the importance of AI in future jobs."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Step 2: Post content to LinkedIn
def post_to_linkedin(content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    payload = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.text

# Run the bot
if __name__ == "__main__":
    content = generate_post()
    status, msg = post_to_linkedin(content)
    print(f"Status: {status} | Message: {msg}")

