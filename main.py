import requests
import datetime as dt
import time


class StackOverflowAPI:
    api_url = "https://api.stackexchange.com/2.3/questions"

    def __init__(self, period, tag):
        """
        period задаёт период времени за который выводить вопросы c тэгом tag
        """
        self.tag = tag
        dt_now = dt.datetime.now()
        dt_period = dt.timedelta(days=period)
        dt_period_before = dt_now - dt_period
        unixtime_period_before = int(time.mktime(dt_period_before.timetuple()))
        self.parameters = {
            "fromdate": unixtime_period_before,
            "order": "desc",
            "sort": "creation",
            "tagged": self.tag,
            "site": "stackoverflow",
            "pagesize": 100,
            "page": 1
        }

    def show_last_questions(self):
        counter = 1  # счётчик постов
        running = True
        while running:
            response = requests.get(self.api_url, params=self.parameters)
            response_dict = response.json()
            if 'error_id' in response_dict:
                print('Error',
                      response_dict['error_id'],
                      response_dict['error_message'],
                      response_dict['name']
                      )
                break
            for item in response_dict['items']:
                ts = int(item['creation_date'])  # дата вопроса
                post_dt = dt.datetime.fromtimestamp(ts)
                cnt = str(counter).rjust(5)
                print(cnt, post_dt.strftime('%Y-%m-%d %H:%M:%S'),
                      item['title'])
                counter += 1
            if 'has_more' in response_dict:
                more_results = input('Есть ещё результаты. Вывести? [y/n]')
                if more_results in ['y', 'Y']:
                    self.parameters['page'] += 1
                else:
                    running = False
        else:
            print('Это все результаты на данный момент.')


if __name__ == '__main__':
    StackOverflowAPI(1, 'Python').show_last_questions()
