

import json
import twint
import twint.token
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
        # self.Output = 'tweets/' + self.name + '.json'
        # self.Store_json = True
        # self.Custom["tweet"] = ["name", "id", "username"]
        self.Store_object = True
        self.Store_object_tweets_list = self.newTweet
        self.Hide_output = True
        # init pull
        self.Since = time.strftime("%Y-%m-%d", time.localtime())
        try:
            twint.run.Profile(self)
        except twint.token.RefreshTokenException as e:
            print("TokenException:", e)

    def get_recent_tweet(self):
        self.recentTweet = self.newTweet

    def get_new_tweet(self):
        t = self.newTweet
        self.newTweet = []
        self.Store_object_tweets_list = self.newTweet
        self.Since = time.strftime("%Y-%m-%d", time.localtime())
        try:
            twint.run.Profile(self)
        except BaseException as e:
            print("TokenException:", e)
            self.newTweet = t

    def message_list(self):
        m_list = []
        if self.newTweet == []:
            return m_list
        else:
            if self.recentTweet == []:
                for t in self.newTweet:
                    m_list.append('<b>'+t.name+':</b> '+t.tweet[:60]+'... <a href=\'https://twitter.com/'+t.username+'/status/'+str(t.id)+'\'>Detail</a>')
            else:
                if self.recentTweet[0].id >= self.newTweet[0].id:
                    return m_list
                else:
                    for t in self.newTweet:
                        if t.id > self.recentTweet[0].id:
                            m_list.append('<b>'+t.name+':</b> '+t.tweet[:60]+'... <a href=\'https://twitter.com/'+t.username+'/status/'+str(t.id)+'\'>Detail</a>')
                        else:
                            break
        return m_list


def pull_and_send(user: TwitterUser):
    user.get_recent_tweet()
    # print('get_recent_tweet()')
    # print(user.recentTweet)
    user.get_new_tweet()
    # print('get_new_tweet()')
    # print(user.newTweet)
    for m in user.message_list():
        bot.send_message(p["chat_id"], m, parse_mode="HTML")


if __name__ == '__main__':
    # load settings
    with open('settings.json', 'r', encoding='utf-8') as f:
        p = json.load(f)
    bot = telebot.TeleBot(p["token"])
    print("load settings complete")
    # bot.polling()
    # load users data
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    print("load user data complete")
    # initial
    twitter_user_list = [TwitterUser(k, v) for k, v in users.items()]

    def job():
        for u in twitter_user_list:
            pull_and_send(u)

    def refresh_user_list():
        global twitter_user_list
        with open('users.json', 'r', encoding='utf-8') as f:
            ref_users = json.load(f)
        if not ref_users == users:
            twitter_user_list = [TwitterUser(k, v) for k, v in ref_users.items()]

    schedule.every(30).seconds.do(job)
    schedule.every(10).minutes.do(refresh_user_list)

    while True:
        schedule.run_pending()
        time.sleep(1)


