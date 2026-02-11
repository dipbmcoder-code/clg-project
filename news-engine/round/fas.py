import requests
import json
import base64

user = "user"
password = "pass"
url2 = "https://URL/wp-json/wp/v2/posts"

payload = json.dumps({
    "title": "title",
    "status": "draft",
    "content": "text_all"
    })
credentials = user + ':' + password
token = base64.b64encode(credentials.encode())
headers2 = {'Authorization': 'Basic ' + token.decode('utf-8') ,
    'Content-Type': 'application/json'}

print(headers2)
print(payload)

response = requests.request("POST", url2, headers=headers2, data=payload)
# response = requests.request(url2, {"id":20457,"date":"2023-01-09T19:11:53","date_gmt":"2023-01-09T16:11:53","guid":{"rendered":"https:\/\/malanka.media\/?p=20456","raw":"https:\/\/malanka.media\/?p=20456"},"modified":"2023-01-09T19:11:53","modified_gmt":"2023-01-09T16:11:53","password":"","slug":"","status":"draft","type":"post","link":"https:\/\/malanka.media\/?p=20456","title":{"raw":"title","rendered":"title"},"content":{"raw":"text_all","rendered":"<p>text_all<\/p>\n","protected":'false',"block_version":0},"excerpt":{"raw":"","rendered":"<p>text_all<\/p>\n","protected":'false'},"author":13,"featured_media":0,"comment_status":"","ping_status":"","sticky":'false',"template":"","format":"standard","meta":[],"categories":[1],"tags":[],"permalink_template":"https:\/\/malanka.media\/news\/20456","generated_slug":"title","_links":{"self":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"collection":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts"}],"about":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/types\/post"}],"author":[{"embeddable":'true',"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/users\/13"}],"replies":[{"embeddable":'true',"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/comments?post=20456"}],"version-history":[{"count":0,"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456\/revisions"}],"wp:attachment":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/media?parent=20456"}],"wp:term":[{"taxonomy":"category","embeddable":'true',"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/categories?post=20456"},{"taxonomy":"post_tag","embeddable":'true',"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/tags?post=20456"}],"wp:action-publish":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"wp:action-unfiltered-html":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"wp:action-sticky":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"wp:action-assign-author":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"wp:action-create-categories":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"wp:action-assign-categories":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"wp:action-create-tags":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"wp:action-assign-tags":[{"href":"https:\/\/malanka.media\/wp-json\/wp\/v2\/posts\/20456"}],"curies":[{"name":"wp","href":"https:\/\/api.w.org\/{rel}","templated":'true'}]}})
print(response)
print(response.text)

print(f"[INFO]  posted")
