##### Quick start

- Clone this [repo](https://github.com/achicha/travel): `git clone https://github.com/achicha/travel`
- go to repo's folder: `cd travel`
- Install dependencies
    * with [pipenv](https://github.com/kennethreitz/pipenv): `pipenv install` or `pip install -r Pipfile`
    * or using pip: `pip install -r requirements.txt`

- create `.env` file: `touch .env`
- add private parameters to `.env`:

        TOKEN=your_telegram_token
        CHAT_ID=your_telegram_chat_id
        DATABASE_NAME=db_name
        DATABASE_CON=sqlite:///
        HEROKU_URL=https://your_app.herokuapp.com/
        TRAVEL_ROUTE=my_api
    
- activate virtualenv: `pipenv shell`
- run this app: `python run.py aviasales -from LWN -to MOW -s 2018-04-28 -e 2018-05-03 -p 10200`
    
