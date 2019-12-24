import settings
import requests
import oseti
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

SLACK_URL = "https://slack.com/api/conversations.history"
START_DATE = datetime(2019,1,1,0,0)
END_DATE = datetime(2019,12,31,0,0)

def main():
    texts = getTextFromSlack(START_DATE, END_DATE)
    results = getResult(texts, START_DATE, END_DATE)
    output(results)

def getTextFromSlack(fromDate, toDate):
    # see: https://api.slack.com/methods/conversations.history
    texts = []
    cursor = ''

    while True:
        payload = {
            "channel": settings.SLACK_CHANNEL_ID,
            "token": settings.SLACK_TOKEN,
            "latest": toDate.strftime('%s'),
            "oldest": fromDate.strftime('%s'),
            "limit": 1000,
            "cursor": cursor
        }
        response = requests.get(SLACK_URL, params=payload)
        json_data = response.json()
        msgs = json_data['messages']
        texts += [{"text" : msg.get('text'), "unixtime" : msg.get('ts')[0:10]} for msg in msgs]

        # 1000件以上の場合ページネイトして結果を取得する
        if json_data.get('response_metadata') == None:
            break
        cursor = json_data['response_metadata']['next_cursor']

    return texts

def getResult(texts, fromDate, toDate):
    i = 0
    results = []
    tmp_texts = []
    dates = date_range(fromDate, toDate)

    for text in reversed(texts):
        if dates[i].strftime('%s') <= text.get('unixtime') < (dates[i] + timedelta(1)).strftime('%s'):
            tmp_texts.append(text) 
        else:
            results.append({'date': dates[i], 'score': score(tmp_texts)})
            i += 1
            tmp_texts = []
    return results

def date_range(start_date: datetime, end_date: datetime):
    diff = (end_date - start_date).days + 1
    return [start_date + timedelta(i) for i in range(diff)]

def score(texts):
    # see: https://github.com/ikegami-yukino/oseti
    analyzer = oseti.Analyzer()
    count = 0
    total_score = 0
    for text in texts:
        try:
            txt_scores = analyzer.analyze(text.get('text'))
            if len(txt_scores) == 0:
                continue
            total_score += np.average(txt_scores) 
        except IndexError:
            print("error起きたけどながしとくわ！")
    return total_score

def output(results):
    x = []
    y = []
    for result in results:
        x.append(result.get('date').strftime("%Y/%m/%d"))
        y.append(result.get('score'))
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x,y)

    dayｓ = mdates.DayLocator() 
    daysFmt = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    plt.xticks(x[::30], x[::30],rotation=90, size='small')

    plt.show()

if __name__ == "__main__":
    main()