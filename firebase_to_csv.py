import json, csv

with open('polireddit-export_flair_time.json', 'r') as _file:
    data = json.loads(_file.read())

def generate_submissions(data):
    with open("submissions_flair.csv", 'w') as sub:
        writer = csv.writer(sub)
        header = [
            'Submission',
            'id',
            'title',
            'media',
            'selftext',
            'num_comments',
            'ups',
            'downs',
            'flair',
            'score',
            'link',
            'created',
            'flair_assigned'
        ]
        writer.writerow(header)
        for x in range(len(data['submissions'])):
            values = [
                x,
                data['submissions'][x]['id'],
                data['submissions'][x]['title'],
                data['submissions'][x]['media'],
                data['submissions'][x]['selftext'],
                data['submissions'][x]['num_comments'],
                data['submissions'][x]['ups'],
                data['submissions'][x]['downs'],
                data['submissions'][x]['flair'],
                data['submissions'][x]['score'],
                data['submissions'][x]['link'],
                data['submissions'][x]['created'],
                data['submissions'][x]['flair_assigned'] if 'flair_assigned' in data['submissions'][x] else None
            ]
            writer.writerow(values)

def generate_comments(data):
    with open("comments.csv", 'w') as sub:
        data = data['comments']
        writer = csv.writer(sub)
        header = [
            'Submission', 'commment_num', 'created', 'comment_id', 'author',
            'parent_id', 'score','text'
        ]
        writer.writerow(header)
        for x in range(len(data)):
            times =  ((len(data[x])-2)//7) if len(data[x]) > 2 else 0
            if times != 0:
                for y in range(times):
                    values = [
                        data[x][str(y) + '_sub_id'], y, data[x][str(y) + '_posted'],
                        data[x][str(y) + '_id'],
                        data[x][str(y) + '_author'],
                        data[x][str(y) + '_parent_id'],
                        data[x][str(y) + '_score'],
                        data[x][str(y)]
                    ]
                    writer.writerow(values)

#generate_comments(data)
generate_submissions(data)
