
import praw, re
from urlextract import URLExtract
import json, csv
_reddit = praw.Reddit(client_id='U-9whxE5yXShxA', client_secret='OQVVmWYy2rediR-6jm0zophXizM', user_agent='python:fact:1.00 (by /u/kalebr80)')


def writeToFiles(stances, body):
    with open('stances_test_reddit.csv', 'w') as out:
        writer = csv.writer(out)
        stances_header = ['Headline', 'Body ID', 'redditId']
        writer.writerow(stances_header)
        for stance in stances:
            writer.writerow([stances[stance]['title'], stances[stance]['Body ID'], stances[stance]['id']])
    with open('body_test_reddit.csv', 'w') as bout:
        writer = csv.writer(bout)
        body_header = ['Body ID', 'articleBody']
        writer.writerow(body_header)
        for bod in body:
            writer.writerow([body[bod]['Body ID'], body[bod]['articleBody']])


def save_submission_db():
    stances = {}
    body = {}
    for num, sub in enumerate(_reddit.subreddit('politicalfactchecking').hot(limit=550)):
        temp_dict = {}
        temp_dict['id'] = sub.id
        temp_dict['title'] = sub.title.strip().replace('\n', '')
        temp_dict['selftext'] = sub.selftext.strip().replace('\n', '')
        temp_dict['Body ID'] = num
        sub.comments.replace_more(limit=0)
        y = 0
        body_temp = ''
        for comment in sub.comments:
            #print (vars(comment))
            body_temp += comment.body.strip().replace('\n', '')
            print ('working on {}-{}'.format(num, y))
            y += 1
        if body_temp:
            stances[num] = temp_dict
            body[num] = {'Body ID': num}
            body[num]['articleBody']= body_temp


    return stances, body

#update_downs()
stances, body = save_submission_db()
writeToFiles(stances, body)
