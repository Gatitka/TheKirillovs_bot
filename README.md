# TheKirillovs_bot
Family budget managment Bot assistant

Current ChatBot helps to record and follow budget spendings within a certain list of users (my family).
Users can record expenses by selecting /add_expense button from reply menu or see monthly report by pushing /report.
Expenses are categorized by preset buttons and after recording bot messages the amount of money available to be spent this month.
Admin section enables to prepare the database, add/delete users, manage admin rights.

## Technologies used in project
Python, SQLight,
(currently developing: Docker, GitHub Actions)

## Launching
Clone repo
in project folder create new files accountant.db, config.py.
##### accountant.db
In the created database file must create following tables:
- users: list of users allowed to use Bot
- records: main records table with expenses list
Tables can be created in Tm itself by /create_tables command.

##### config.py
add bot token, received from BotFather like below
```
BOT_TOKEN="<token_received_from_BotFather>"
ADMIN_ID="<User_ID_in_TM>"
```


## Created by
Natalia Kirilova - author
I'm glad to receive your questions or comments at my box: gatitka@yandex.ru
