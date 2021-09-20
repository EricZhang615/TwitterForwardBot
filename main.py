
import os
import json
import twint
import time
import telebot
import schedule


class TwitterUser(twint.config.Config):
    def __init__(self, name, username):
        self.name = str(name)
        self.recentTweet = []
        self.newTweet = []
        self.Username = str(username)
        self.Since = ''
        self.Limit = 1
        self.Output = 'tweets/' + self.name + '.json'
        self.Store_json = True
        self.Custom["tweet"] = ["name", "id", "username"]
        if not os.path.exists(self.Output):
            with open(self.Output, 'w') as f:
                pass

    def get_recent_tweet(self):
        self.recentTweet = []
        if os.path.getsize(self.Output) != 0:
            with open(self.Output, 'r+') as f:
                for line in f.readlines():
                    self.recentTweet.append(json.loads(line.strip()))
                f.seek(0)
                f.truncate()
        return 0

    def get_new_tweet(self):
        self.Since = time.strftime("%Y-%m-%d", time.localtime())
        twint.run.Profile(self)
        self.newTweet = []
        if os.path.getsize(self.Output) != 0:
            with open(self.Output, 'r+') as f:
                for line in f.readlines():
                    self.newTweet.append(json.loads(line.strip()))
        return 0

    def message_list(self):
        m_list = []
        if self.newTweet == []:
            return m_list
        else:
            if self.recentTweet == []:
                for t in self.newTweet:
                    m_list.append(t['name'] + ': https://twitter.com/' + t['username'] + '/status/' + str(t['id']))
            else:
                if self.recentTweet[0]['id'] >= self.newTweet[0]['id']:
                    return m_list
                else:
                    for t in self.newTweet:
                        if t['id'] > self.recentTweet[0]['id']:
                            m_list.append(t['name'] + ': https://twitter.com/' + t['username'] + '/status/' + str(t['id']))
        return m_list


def pull_and_send(user: TwitterUser):
    user.get_recent_tweet()
    # print('get_recent_tweet()')
    # print(user.recentTweet)
    user.get_new_tweet()
    # print('get_new_tweet()')
    # print(user.newTweet)
    for m in user.message_list():
        bot.send_message(p["chat_id"], m)


if __name__ == '__main__':
    # load settings
    with open('settings.json', 'r', encoding='utf-8') as f:
        p = json.load(f)
    bot = telebot.TeleBot(p["token"])
    # bot.polling()
    # load users data
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    # initial
    twitter_user_list = [TwitterUser(k, v) for k, v in users.items()]

    def job():
        for u in twitter_user_list:
            pull_and_send(u)

    schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


    # s = time()
    #
    # run_time = time() - s
    # print(f'Request Took {run_time} ms')
