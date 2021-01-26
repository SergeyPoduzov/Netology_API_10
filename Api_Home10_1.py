# Задача №1
# Пользователя нужно описать с помощью класса и реализовать метод поиска общих друзей, используя API VK.

import requests
import time

#Токен из задания
token = ''


URL = 'https://api.vk.com/method/'
params = {
    'user_id':'1',
    'access_token': token,
    'v': '5.126',
    'fields': 'online, domain, sex, education'

}

def getting_info():
    params = {
        'user_id': '1',
        'access_token': token,
        'v': '5.126',
        'fields': 'online, domain, sex, education'
    }
    res = requests.get(URL + 'users.get', params=params)

    return res


def search_query(q, sorting = 0):
    params = {
        'q':q,
        'access_token': token,
        'v': '5.126',
        'sort': sorting,
        'count':300
    }
    req = requests.get(URL + 'groups.search', params).json()
    req = req['response']['items']

    return req

# print(search_query('python',0))

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']
        self.data_vk = {
            'first_name': None,
            'last_name': None,
            'can_access_closed':None,
            'sex':None,
            'id':None,
            'online':None,
            'domain':None,

        }



    def __str__(self):
        if self.data_vk['first_name'] == 'DELETED':
            txt = "Пользователь удален"
            return txt
        else:
            txt = ""
            txt += "\nИмя: "+str(self.data_vk['first_name'])+", фамилия: " + str(self.data_vk['last_name'])
            txt += "\nID: "+str(self.data_vk['id']) +", ссылка: " + str(self.data_vk['domain'])
            return txt

    def descriptive_user(self):
        if self.data_vk['first_name'] == 'DELETED':
            txt = str(self.data_vk['id'])+ " - пользователь удален."
            return txt
        else:
            txt = str(self.data_vk['id'])+ " -  Имя: " + str(self.data_vk['first_name']) + ", фамилия: " + str(self.data_vk['last_name'])
            return txt


    def get_user_description(self, user_id = None):
        if user_id is None:
            user_id = self.owner_id
        users_url = self.url + 'users.get'
        users_params  ={
            'user_id': user_id,
            'fields': 'online, domain, sex, education'
        }
        req = requests.get(users_url, params = {**self.params, **users_params })
        req = req.json()
        req = req['response'][0]

        if req['first_name'] == "DELETED":
            self.data_vk = {
                'first_name': 'DELETED',
                'last_name': None,
                'can_access_closed':None,
                'sex':None,
                'id':'id',
                'online':None,
                'domain':None,
                }
        else:
            domain=['https://vk.com/',req['domain'] ]
            domain=''.join(domain)
            self.data_vk = {
                'first_name': req['first_name'],
                'last_name': req['last_name'],
                'can_access_closed': req['can_access_closed'],
                'sex': req['sex'],
                'id': req['id'],
                'online': req['online'],
                'domain':domain,

            }


    def get_followers(self, user_id = None):
        if user_id is None:
            user_id = self.owner_id
        followers_url = self.url + 'users.getFollowers'
        followers_params  ={
            # 'offset':0,
            'count':1000,
            'user_id':user_id
        }
        res = requests.get(followers_url, params={**self.params, **followers_params})
        return res.json()

    def get_groups(self, user_id=None ):
        if user_id is None:
            user_id = self.owner_id
        groups_url = self.url + 'groups.get'
        groups_param = {
            'count': 1000,
            'user_id': user_id,
            'extended':1,
            'fields':'members_count'

        }
        res = requests.get(groups_url, params={**self.params, **groups_param})
        return res.json()

    def get_mutualfriends(self, source_uid, target_uid):
        mutualfriends_url = self.url + 'friends.getMutual'
        mutualfriends_param = {
            'source_uid': source_uid,
            'target_uid': target_uid,
        }
        res = requests.get(mutualfriends_url, params={**self.params, **mutualfriends_param})
        res = res.json()

        return res

    def __and__(self, others):


        list_mutualfriend_json = self.get_mutualfriends(str(self.data_vk['id']), str(others.data_vk['id']))

        return list_mutualfriend_json




    def get_friends(self, user_id = None ):
        if user_id is None:
            user_id = self.owner_id
        friends_url = self.url + 'friends.get'
        groups_param = {
            'count': 5000,
            'offset': 0,
            'fields':'city,domain',
            'name_case':'ins'

        }
        res = requests.get(friends_url, params = {**self.params, **groups_param})
        return res.json()


def is_digit(string):
    """Проверка ввода цифр"""
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

def getting_id(question1, question2):
    """Ввод ID пользователя"""

    active = True
    while active:
        num_id = input(question1)
        if is_digit(num_id) == True:
            if num_id.count('.') == 0:
                num_id = int(num_id)
                return num_id
            else:
                print(question2)
                continue
        else:
            print(question2)
            continue

def creating_vk_user(list_friends):
    vk_users = []
    """Создает VKuser - пользоваетелй  и создает спискок класса VKusers"""
    for mutual_friend in list_friends:
        vk_client_new = VkUser(token, '5.126')
        vk_client_new.get_user_description(str(mutual_friend))
        time.sleep(0.7)
        vk_users.append(vk_client_new)
        time.sleep(0.7)
    return vk_users



def main():
    # starting_condition()
    vk_client = VkUser(token, '5.126')

    choice = True
    while choice:
        print \
            ("""
                    Домашняя работа по 10-й Лекции "АПИ".
            Введите команду 0-7:
                0 - Завершить работу
                1 - Вывести текущий ID и print(user)
                2 - Поискать друзей между двумя пользователями с помощью общих друзей, используя API VK.
                3 - Поиск общих друзей должен происходить с помощью оператора &, т.е. user1 & user2
            """)

        choice = input("Ваш выбор: ")
        print()
        # выход
        if choice == "0":
            print("До свидания.")
            break

        elif choice == "1":

            choice1 = True
            while choice1:
                print \
                    ("""
                                Домашняя работа по АПИ.
                            Вывести текущий ID и print(user)
                            Введите команду 0-2:
                                0 - Вернуться обратно
                                1 - Вывести информацию по введенному ID
                                2 - Вывести информациб по себе
                            """)
                choice1 = input("Ваш выбор: ")
                print()
                # выход
                if choice1 == "0":
                    break
                elif choice1 == "1":
                    num_id = getting_id("Введите ID пользователя цифрами: ", "Вы ввели с ошибкой, повторите ввод: ")
                    vk_client.get_user_description(str(num_id))
                    print(vk_client)
                elif choice1 == "2":
                    print("Текущий ID пользователя: ", str(vk_client.owner_id))
                    vk_client.get_user_description(str(vk_client.owner_id))
                    print(vk_client)

                else:
                    print("Извините, в меню нет пункта")
                    continue

        elif choice == "2":

            choice2 = True
            while choice2:
                print \
                    ("""
                                Домашняя работа по АПИ.
                            Поискать друзей между двумя пользователями с помощью общих друзей, используя API VK.
                            Введите команду 0-1:
                                0 - Вернуться обратно
                                1 - Ввести ID двух пользователей и с помощью API получите список совместных друзей
                                
                            """)
                choice2 = input("Ваш выбор: ")
                print()
                # выход
                if choice2 == "0":
                    break
                elif choice2 == "1":
                    num1_id = getting_id("Введите ID первого пользователя цифрами: ", "Вы ввели с ошибкой, повторите ввод: ")
                    num2_id = getting_id("Введите ID второго пользователя цифрами: ",
                                         "Вы ввели с ошибкой, повторите ввод: ")

                    list_mutualfriend_json = vk_client.get_mutualfriends(str(num1_id), str(num2_id))

                    try:

                        res = list_mutualfriend_json['response']
                        if res:
                            print("Общее количество друзей: ", len(res))
                            print("Вывод результатов. Делаем запрос...Может потребоваться некоторое время...")
                            vk_users_list = creating_vk_user(res)
                            print("Список общих друзей: \n")
                            for vk_user in vk_users_list:
                                print(vk_user)

                        else:
                            print("К сожалению общих друзей нет")

                    except:
                        res = list_mutualfriend_json['error']
                        print("К сожалению ошибка, попробуйте указать других друзей. ")
                        print(res['error_msg'])

        elif choice == "3":

            choice3 = True
            while choice3:
                print \
                    ("""
                                Домашняя работа по АПИ.
                            Поиск общих друзей должен происходить с помощью оператора &, т.е. user1 & user2
                            Введите команду 0-1:
                                0 - Вернуться обратно
                                1 - Ввести ID двух пользователей и с помощью user1 & user 2

                            """)
                choice3 = input("Ваш выбор: ")
                print()
                # выход
                if choice3 == "0":
                    break
                elif choice3 == "1":
                    num1_id = getting_id("Введите ID первого пользователя цифрами: ",
                                         "Вы ввели с ошибкой, повторите ввод: ")
                    num2_id = getting_id("Введите ID второго пользователя цифрами: ",
                                         "Вы ввели с ошибкой, повторите ввод: ")
                    user1 = VkUser(token,'5.126')
                    user1.get_user_description(str(num1_id ))
                    user2 = VkUser(token, '5.126')
                    user2.get_user_description(str(num2_id))

                    list_mutualfriend_json2 = user1 & user2

                    try:

                        res = list_mutualfriend_json2['response']
                        if res:
                            print("Общее количество друзей: ", len(res))
                            print("Вывод результатов. Делаем запрос...Может потребоваться некоторое время...")
                            vk_users_list = creating_vk_user(res)
                            print("Список общих друзей: \n")
                            for vk_user in vk_users_list:
                                print(vk_user)

                        else:
                            print("К сожалению общих друзей нет")

                    except:
                        res = list_mutualfriend_json2['error']
                        print("К сожалению ошибка, попробуйте указать других друзей. ")
                        print(res['error_msg'])


        else:
            print("Извините, в меню нет пункта")
            continue

main()
