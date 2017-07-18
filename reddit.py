'''
Script that parses reddit and stores the data in a firebase database
'''

import praw, re
from urlextract import URLExtract
import datetime
_reddit = praw.Reddit(client_id='U-9whxE5yXShxA', client_secret='OQVVmWYy2rediR-6jm0zophXizM', user_agent='python:fact:1.00 (by /u/kalebr80)')

import pyrebase
config = {
  "apiKey": " AIzaSyBi1QOGpckOdZnanlDl3o1Dlbz8gfqOxVU",
  "authDomain": "polireddit",
  "databaseURL": "https://polireddit.firebaseio.com",
  "storageBucket": "polireddit.appspot.com",
  "serviceAccount": "poliReddit-serviceAccount.json"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
#authenticate a user
user = auth.sign_in_with_email_and_password("jsuarez@go.olemiss.edu", "polipoli")
_userId = user['idToken']

db = firebase.database()


status = {}
total_votes = 0
total_comments = 0

default_inner = lambda: {
                'id': '',
                'title': '',
                'media': '',
                'selftext': '',
                'num_comments': 0,
                'ups': 0,
                'downs': 0,
                'flair': '',
                'score': 0,
                'link': '',
                'created': ''
}

def get_links(string):
    # write formula for extracting the links from the string.
    # return string with no link
    urls = re.findall(r'(https?://[^\s]+)', string)
    #extractor = URLExtract()
    #urls = extractor.find_urls(string)
    return urls

def update_downs():
    submissions = {}
    for num, sub in enumerate(_reddit.subreddit('politicalfactchecking').hot(limit=530)):
        temp_dict = {'downs': 0}
        score = sub.score
        ratio = sub.upvote_ratio
        ups = round((ratio*score)/(2*ratio - 1)) if ratio != 0.5 else round(score/2)
        downs = ups - score
        downs = 0.0 if downs == -0.0 else downs
        temp_dict['downs'] = downs
        submissions[num] = temp_dict
        #print num, score, ratio, ups, downs
    #print submissions
    db.child('submissions').set(submissions, _userId)


def save_submission_db():
    submissions = {}
    comments = {}
    total_comments = 0
    for num, sub in enumerate(_reddit.subreddit('politicalfactchecking').hot(limit=550)):
        temp_dict = default_inner()
        temp_dict['id'] = sub.id
        temp_dict['title'] = sub.title.strip().replace('\n', '')
        temp_dict['media'] = str(sub.media)
        temp_dict['selftext'] = sub.selftext.strip().replace('\n', '')
        temp_dict['num_comments'] = sub.num_comments
        score = sub.score
        ratio = sub.upvote_ratio
        ups = round((ratio*score)/(2*ratio - 1)) if ratio != 0.5 else round(score/2)
        downs = ups - score
        downs = 0.0 if downs == -0.0 else downs
        ups = 0.0 if ups == -0.0 else ups
        temp_dict['ups'] = ups
        temp_dict['downs'] = downs
        temp_dict['flair'] = str(sub.link_flair_text)
        temp_dict['score'] = score
        temp_dict['created'] = str(datetime.datetime.fromtimestamp(sub.created))
        links  = get_links(temp_dict['title'])
        links.extend(get_links(temp_dict['selftext']))
        temp_dict['link'] = ','.join(links) if links else ''
        #print (links)
        #print (temp_dict['link'] + '-')
        submissions[num] = temp_dict
        sub.comments.replace_more(limit=0)
        y = 0
        comments[num] = {}
        links = []
        time = sub.created

        for comment in sub.comments.list():
            total_comments += 1
            #print (vars(comment))
            comments[num][y] = comment.body.strip().replace('\n', '')
            comments[num][str(y) + '_posted'] = str(datetime.datetime.fromtimestamp(comment.created))
            comments[num][str(y) + '_id'] = comment.id
            comments[num][str(y) + '_author'] = str(comment.author)
            comments[num][str(y) + '_parent_id'] = comment.parent_id
            comments[num][str(y) + '_score'] = comment.score
            comments[num][str(y) + '_sub_id'] = sub.id

            links.extend(get_links(comments[num][y]))
            print ('working on {}-{}'.format(num, y))
            y += 1
            time = time +  (comment.created -time) /2

        comments[num]['link'] = ','.join(links) if links else ''
        comments[num]['created'] = str(datetime.datetime.fromtimestamp(time))
        print ('Comments: {}'.format(total_comments))

    #db.child('submissions').set(submissions, _userId)
    db.child('comments').set(comments, _userId)


#update_downs()
save_submission_db()
