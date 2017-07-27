
import pandas, json
from pandas.io.json import json_normalize
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator, drange

_file = open('polireddit-export.json', 'r')
data = json.loads(_file.read())
submissions = pandas.DataFrame.from_dict(data['submissions'])
submissions.drop(['id', 'media'], axis=1, inplace=True)
# Format to create data from time series
posted = submissions.loc[:,('created','score')]
#posted = posted[posted['score'] < 150]
def to_js_date(x):
    d = datetime.date(*map(int, x[:11].split('-')[:3]))
    return ('{}/{}/1'.format(d.year, d.month))
posted['created'] = posted['created'].apply(to_js_date)
score_values = posted.values.tolist()
score_values = sorted(score_values, key=lambda x: datetime.date(*map(int, x[0].split('/'))))
x_score = []
y_score = []
current = score_values[0][0]
cumulative = 0
for _x, _y in score_values:
    if current != _x:
        x_score.append(_x)
        y_score.append(cumulative)
        cumulative = 0
        current = _x
    else:
        cumulative += _y
print (list(zip(x_score,y_score)))
# Time Series by number of comments
comments = submissions.loc[:,('created','num_comments')]
#comments = comments[comments['num_comments'] < 150]
comments['created'] = comments['created'].apply(to_js_date)
comments_values = comments.values.tolist()
comments_values = sorted(comments_values, key=lambda x: datetime.date(*map(int, x[0].split('/'))))


x_comments = []
y_comments = []
current = comments_values[0][0]
cumulative = 0
for _x, _y in comments_values:
    if current != _x:
        x_comments.append(_x)
        y_comments.append(cumulative)
        cumulative = 0
        current = _x
    else:
        cumulative += 1


rule = rrulewrapper(MONTHLY, interval=4)
loc = RRuleLocator(rule)
formatter = DateFormatter('%m/%y')
fig, ax = plt.subplots()
plt.plot_date(x_comments,y_comments, fmt="g-", xdate=True)
#plt.plot_date(x_score,y_score, fmt="-", xdate=True)
ax.xaxis.set_major_locator(loc)
ax.xaxis.set_major_formatter(formatter)
labels = ax.get_xticklabels()
plt.setp(labels, rotation=30, fontsize=10)
plt.legend(['Submission Frequency'])
plt.title("Historical Submission Activity")
plt.ylabel("Frequency")
plt.xlabel("Submission Date")
plt.show()
