import openai
import requests
import os
from openai import OpenAI
import os

print("✅ Starting LinkedIn auto-post script...")

openai.api_key = os.getenv("OPENAI_API_KEY")
access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
user_id = os.getenv("LINKEDIN_USER_ID")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post():
    print("🧠 Generating post using OpenAI v1.0+...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Write a professional post about how AI is transforming education"}
        ]
    )
    return response.choices[0].message.content


def post_to_linkedin(content):
    print("📤 Sending post to LinkedIn...")
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    data = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    res = requests.post(url, headers=headers, json=data)
    print("📊 Response:", res.status_code, res.text)

# Run it
post_text = generate_post()
print("📝 Generated Post:\n", post_text)
post_to_linkedin(post_text)
