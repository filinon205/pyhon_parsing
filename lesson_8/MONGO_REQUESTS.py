# 4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
# 5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient('127.0.0.1',27017)
db = client['instagram_base']

print('Количество документов в коллекции instagramsubscription:', db.instagramsubscription.estimated_document_count())
print('Количество документов в коллекции instagrampost:', db.instagrampost.estimated_document_count())
print('Количество документов в коллекции instagramfollower:', db.instagramfollower.estimated_document_count())

# collections : instagramsubscription, instagrampost, instagramfollower
# пользователи в базе (user_id: 27790688603, 4590787289, 4684506 )

user_id = input('Введите id пользователя для поиска его подписчиков (варианты: 27790688603, 4590787289, 4684506):')

num = 1
for follower in db.instagramfollower.find( { "user_id" : user_id} , {'_id': 0 , 'follower_id': 1 , 'follower_name': 1 } ):
    print(num)
    pprint(follower)
    num +=1

num_2 = 1
for follower in db.instagramsubscription.find( { "user_id" : user_id} , {'_id': 0 , 'subscription_id': 1 , 'subscription_name': 1 } ):
    print(num_2)
    pprint(follower)
    num_2 +=1

num_3 = 1
for post in db.instagrampost.find( { "user_id" : user_id} , {'_id': 0 , 'photo': 1 , 'likes': 1 } ):
    print(num_3)
    pprint(post)
    num_3 +=1

print("Всего у польователя", user_id, num, "подписчиков")
print("Всего у польователя", user_id, num_2, "подписок")
print("Всего у польователя", user_id, num_3, "постов")