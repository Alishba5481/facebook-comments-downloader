import requests
import pandas as pd

page_id = "YOUR_PAGE_ID_HERE"
post_id = "YOUR_POST_ID_HERE"
access_token = "YOUR_ACCESS_TOKEN_HERE" 

url = f'https://graph.facebook.com/v21.0/{page_id}_{post_id}/comments'
params = {
    'access_token': access_token,
    'fields': 'from,created_time,message',
    'limit': 100,
}

comments = []

while url:
    response = requests.get(url, params=params)
    data = response.json()

    if 'error' in data:
        print("Facebook error:", data['error'].get('code'), "-", data['error'].get('message'))
        raise SystemExit

    comments.extend(data.get('data', []))
    url = data.get('paging', {}).get('next')
    params = None  


def get_comment(comment):
    return {
        'name': comment.get('from', {}).get('name', 'Unknown'),
        'time': comment.get('created_time'),
        'message': comment.get('message', ''),
    }


excel_data = list(map(get_comment, comments))
df = pd.DataFrame(excel_data)
df.to_excel('comments.xlsx', index=False)

print(len(df), "comments are save in  comments.xlsx.")
