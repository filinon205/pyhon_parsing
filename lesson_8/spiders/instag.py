import scrapy
from scrapy.http import HtmlResponse
from insta.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    #атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'XXXX' # userId
    insta_pwd = 'XXXXXXXXXXXXXXXXXXXXXX'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['bigdatabigdata','data.vis', 'machinelearning']    #Пользователи, у которого собираем посты. Можно указать список
    # followers_link = parse_user + '/followers/'      #Подписчики у этого пользователя

    graphql_url = 'https://www.instagram.com/graphql/query/?'

    posts_hash = 'eddbde960fed6bde675388aac39a3657'     #hash для получения данных по постах с главной страницы
    followers_hash = 'c76146de99bb02f6415203be841dd25a' #hash для получения данных по Подписчиках с главной страницы
    subscription_hash = 'd04b0a864b4b54837c0d870b0e77e076' #hash для получения данных по Подписках с главной страницы

    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_parse(self, response:HtmlResponse):

        j_body = json.loads(response.text)
        if j_body['authenticated']:    #Проверяем ответ после авторизации
            for self.parse_user in self.parse_users:

                yield response.follow(                  #Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                    f'/{self.parse_user}',
                    callback= self.user_data_parse,
                    cb_kwargs={'username':self.parse_user}
                )

    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)       #Получаем id пользователя
        variables={'id':user_id,                                    #Формируем словарь для передачи даных в запрос
                   'first':50}                                      #12 постов. Можно больше (макс. 50)
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'    #Формируем ссылку для получения данных о постах
        url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}' #Формируем ссылку для получения данных о Подписчиках
        url_subscription = f'{self.graphql_url}query_hash={self.subscription_hash}&{urlencode(variables)}' #Формируем ссылку для получения данных о Подписках

        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,                      # передаем управление в user_posts_parse - ищем посты
            cb_kwargs={'username':username,
                       'user_id':user_id,
                       'variables':deepcopy(variables)}           #variables ч/з deepcopy во избежание гонок
        )

        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,                   # передаем управление в user_posts_parse - ищем подписчиков
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

        yield response.follow(
            url_subscription,
            callback=self.user_subscriptions_parse,                # передаем управление в user_posts_parse - ищем подписки
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def user_posts_parse(self, response: HtmlResponse, username, user_id,
                         variables):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):                # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')  # Сами посты
        for post in posts:  # Перебираем посты, собираем данные
            item = InstaparserItem(
                user_id=user_id,
                photo=post['node']['display_url'],
                likes=post['node']['edge_media_preview_like']['count'],
                post=post['node']
            )
            yield item  # В пайплайн



# отсюда собираем данные о подписчиках и подписках.

    def user_followers_parse(self, response:HtmlResponse,username,user_id, variables):

        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):                                          #Если есть следующая страница
            variables['after'] = page_info['end_cursor']
            url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'

            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')  # Сами подписчики
        for follower in followers:  # Перебираем подписчиков, собираем данные
            item = InstaparserItem(
                user_id=user_id,
                follower_id=follower['node']['id'],
                follower_name=follower['node']['username'],
                follower_full_name=follower['node']['full_name'],
                follower_photo=follower['node']['profile_pic_url'],
                follower=follower['node']
            )

            yield item # В пайплайн

    def user_subscriptions_parse(self, response:HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']
            url_subscription = f'{self.graphql_url}query_hash={self.subscription_hash}&{urlencode(variables)}'

            yield response.follow(
                url_subscription,
                callback=self.user_subscriptions_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscriptions = j_data.get('data').get('user').get('edge_follow').get('edges')  # Сами подписки .get(r'/d')
        for subscription in subscriptions:  # Перебираем подписки, собираем данные
            item = InstaparserItem(
                user_id=user_id,
                subscription_id =subscription['node']['id'],
                subscription_name=subscription['node']['username'],
                subscription_full_name=subscription['node']['full_name'],
                subscription_photo=subscription['node']['profile_pic_url'],
                subscription=subscription['node']
            )

            yield item # В пайплайн


        #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')