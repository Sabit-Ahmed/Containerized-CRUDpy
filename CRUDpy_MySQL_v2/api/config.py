import os

user = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
database = os.environ['MYSQL_DATABASE']

DATABASE_CONNECTION_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'