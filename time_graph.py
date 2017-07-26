
import pandas, json
from pandas.io.json import json_normalize
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

_file = open('polireddit-export.json', 'r')
data = json.loads(_file.read())
submissions = pandas.DataFrame.from_dict(data['submissions'])
submissions.drop(['id', 'media'], axis=1, inplace=True)
# Format to create data from time series
posted = submissions.loc[:,('created','score')]
posted = posted[posted['score'] < 150]
score_values = posted.values.tolist()
x_score = []
y_score = []
for _x, _y in score_values:
    x_score.append(_x)
    y_score.append(_y)

# Time Series by number of comments
comments = submissions.loc[:,('created','num_comments')]
comments = comments[comments['num_comments'] < 150]
comments_values = comments.values.tolist()


x_comments = []
y_comments = []
for _x, _y in comments_values:
    x_comments.append(_x)
    y_comments.append(_y)

plt.plot_date(x_comments,y_comments)
plt.plot_date(x_score,y_score)


plt.title("Submissions")
plt.ylabel("yes")
plt.grid(True)
plt.show()
