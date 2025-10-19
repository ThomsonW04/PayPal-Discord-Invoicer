# How to use
## Please begin with building a Virtual Environment and ensure the following are installed with pip:
- discord.py
- requests
- dotenv

## Setup the .env
- Copy the .env.template
- Fill it in and rename it to .env
- Please ensure the INVOICE PREFIX is unique, maybe put the company name followed by INV- (this is to keep it clashing with others on PayPal)

## Setup the database
- Run the migrations in the migration folder. Please run 0 first and then build upto the file starting with the highest number. (If you ever use a later released version you will not need to rebuild the database from the start, just run new numbers)

## Running the app
- python3 main.py
