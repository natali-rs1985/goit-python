from datetime import datetime, timedelta


def congratulate(src_users):

    current_date = datetime.now()
    date_from = (current_date +
                 timedelta(days=(6 - current_date.date().isoweekday()))).date()
    date_to = (current_date + timedelta(days=(13 -
               current_date.date().isoweekday()))).date()
    monday = (current_date + timedelta(days=(8 - current_date.date().isoweekday())))
    users = []
    for dicts in src_users:
        user = dict()
        for key, value in dicts.items():
            user['name'] = key
            user['birthday'] = datetime.strptime(
                value, '%d.%m.%Y').replace(year=current_date.year)
        users.append(user)

    users = [user for user in users if date_from <=
             user.get('birthday').date() < date_to]

    for dicts in users:
        if dicts['birthday'].isoweekday() == 6:
            dicts['birthday'] += timedelta(days=2)
            dicts['birthday'].strftime('%A')
        elif dicts['birthday'].isoweekday() == 7:
            dicts['birthday'] += timedelta(days=1)

    congrats_list = []
    for dicts in users:
        congrats_list.append([dicts['birthday'].isoweekday(), dicts['name']])
    # print(congrats_list)

    for i in range(1, 6):
        result = []
        for user in congrats_list:
            if i in user:
                result.append(user[1])
        # print(result)
        if len(result) > 0:
            day = (monday + timedelta(days=(i-1))).strftime('%A')
            print(f'{day}: {", ".join(result)}')


if __name__ == '__main__':

    user_list = [{'Jake': '16.05.2001'},
                 {'Ann': '30.01.1983'},
                 {'Kate': '11.02.1997'},
                 {'John': '16.05.2001'},
                 {'Nick': '19.05.1992'},
                 {'Sam': '30.05.2009'},
                 {'Alex': '11.05.1984'},
                 {'Jess': '28.02.2004'},
                 {'Ivan': '09.11.2007'},
                 {'Lesya': '08.03.1995'},
                 {'Nata': '15.05.2003'},
                 {'Phill': '22.05.1987'},
                 {'Yana': '20.05.2005'}]

    congratulate(user_list)
