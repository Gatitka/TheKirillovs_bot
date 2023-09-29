# TheKirillovs_bot

## Family budget managment Bot assistant

Current ChatBot helps to record and follow budget spendings within a certain list of users. One bot manage only one circle of users - hence each users group shall create their own bot.

* Users record expenses and receive short/detailed reports
* Admin can edit user list, share admin rights, create tables in db
* Docker and GitHub actions is to be developed


## Technologies used in project
Python, SQLight,
(currently developing: Docker, GitHub Actions)

## Launching
1. Clone the repo
2. Inside the project folder create new files: accountant.db, config.py.
##### accountant.db
Create the database file and afterwards data tables must be created inside(users, records) - either through admin section in TM after launching the bot or manualy.


##### config.py
Contains the bot token, received from BotFather like, admin id in Tm and a path to the database file (local path differs from the server one)
```
BOT_TOKEN="<token_received_from_BotFather>"
ADMIN_ID="<User_ID_in_TM>"
DB_FILE = 'accountant.db'
```

3. Launch the bot.py file

4. Work manual:
Logging in under admin user enables ADMIN panel allowing tables creation inside the db file, add/delete users, share admin rights.
Users can record expenses by secelting /add_expense button in bottom menu or see monthly report by choosing /report button.
Expenses are categorized by preset buttons of inline menu. After choosing the category send expenses amount and comment, for example:
```
10.15 apples for dinner
```
After recording the expense bot will message the amount of money available to be spent this month.

## Created by
Natalia Kirillova - author
I'm glad to receive your questions or comments
gatitka@yandex.ru
Tm: @Gatitka5
