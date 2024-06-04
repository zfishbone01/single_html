import numpy as np   
import os, sys
import pandas as pd  
import google_auth_oauthlib.flow 
import googleapiclient.discovery 
import googleapiclient.errors
from googleapiclient.errors import HttpError 
 
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]   

def getVideos(channelId, youtube):
    nextPageToken = ''
    while nextPageToken != "null":
        try:
            request = youtube.search().list(part="snippet", channelId=channelId, order="date", maxResults=100, type="video", pageToken=nextPageToken)
            response = request.execute()
            for item in response["items"]:
                videoId = item["id"]["videoId"]
                titile = item["snippet"]["title"]
                description =item["snippet"]["description"]
                publishTime = item["snippet"]["publishTime"]
                channelTitle = item["snippet"]["channelTitle"]
                print('\t'.join([videoId, titile, description, publishTime, channelTitle]))
            nextPageToken = response["nextPageToken"]
        except Exception as e:
            print(str(e), file=sys.stderr)
            nextPageToken = "null"
            


        



def getVideoComment(videoId, videoName, youtube):
    #videoId = 'ZxvaS4Ho254'
    request = youtube.commentThreads().list(part="snippet,replies",videoId=videoId,maxResults=100)
    response = request.execute() 
    totalResults = 0
    totalResults = int(response['pageInfo']['totalResults']) 
     
    count = 0
    nextPageToken = ''   
    comments = []
    first = True 
    further = True   
    while further:   
        halt = False 
        #if first == False:   
        #    print('..')  
        try: 
            response = youtube.commentThreads().list(
                part="snippet,replies",  
                videoId=videoId, 
                maxResults = 100,
                textFormat='plainText',  
                pageToken=nextPageToken  
            ).execute()  
            totalResults = int(response['pageInfo']['totalResults']) 
            print(totalResults, file=sys.stderr)
        except HttpError as e:   
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            halt = True  

        if halt == False:
            count += totalResults
            for item in response["items"]:   
            # 这只是一部分数据，你需要啥自己选就行，可以先打印下你能拿到那些数据信息，按需爬取。  
                def retrieve(comment):
                    try:
                        author = comment["snippet"]["authorDisplayName"]
                        authorId = comment["snippet"]["authorChannelId"]["value"]
                    except:
                        author = ""
                        authorId = ""
                    videoId = comment["snippet"]["videoId"]
                    commentId = comment["id"]
                    text = comment["snippet"]["textDisplay"] 
                    text = text.replace('\n','. ')
                    likeCount = comment["snippet"]['likeCount']  
                    publishtime = comment['snippet']['publishedAt']
                    parentId = comment["snippet"].get("parentId",'0')
                    return [videoId, videoName, commentId, parentId, author, authorId, publishtime, str(likeCount), text]
                try:
                    comment = retrieve(item["snippet"]["topLevelComment"])
                except:
                    print(item["snippet"]["topLevelComment"])
                    exit(0)
                
                #print('\t'.join([videoId, commentId, author, authorId, publishtime, str(likeCount), text]))
                print('\t'.join(comment))

                if "replies" in item:
                    for r in item["replies"]["comments"]:
                        #print(r["textDisplay"])
                        comment = retrieve(r)
                        print('\t'.join(comment))

        if totalResults < 100:   
            further = False  
            first = False
        else:
            further = True   
            first = False
        try: 
            nextPageToken = response["nextPageToken"]
        except KeyError as e:
            print("An KeyError error occurred: %s" % (e), file=sys.stderr)
            further = False  
        print('get data count: ', str(count), file=sys.stderr)
 
def main():  
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
 
    api_service_name = "youtube" 
    api_version = "v3"   
    api_key = ""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # 这个文件需要自己注册完，自己下载json文件 
    #client_secrets_file = "client_secret_801260648842-0nfj6768e36ad8er3hfu8j4gi1mdr35c.apps.googleusercontent.com.json"
    # Get credentials and create an API client   
    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file)
    #credentials = flow.run_console() 
    #youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = api_key)
    #getVideoComment("ZxvaS4Ho254", youtube)
    #getVideos("UCoC47do520os_4DBMEFGg4A", youtube) #liqizi
    for line in sys.stdin:
        line = line.strip()
        items = line.split('\t')
        videoId = items[0]
        videoName = items[1]
        getVideoComment(videoId, videoName, youtube)


    #videoId = 'B6bJ_vTslyo'
## write to csv file 
    #data = np.array(comments)
    #df = pd.DataFrame(data, columns=['author', 'publishtime', 'likeCount', 'comment'])   
    #df.to_csv('liziqi_B6bJ_vTslyo_comments.csv', index=0, encoding='utf-8')  
 
if __name__ == "__main__":   
    main()                                                       

