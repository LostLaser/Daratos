from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='4922b83d01234149be2ba02e37e0592f')
src_list=['msnbc']
content_list=[]
source_list=[]
print(src_list[0])
for i in range(1,2):
    api_ret=newsapi.get_everything(sources=src_list[0],language='en',page=1,sort_by='popularity')
                            
    articles=api_ret['articles']
    if len(articles) == 0:
        print("breaking")
        break

    for article in articles:
        content_list.append(article['content'])
        source_list.append(article['source']['name'])

print(content_list)
print(source_list)

    