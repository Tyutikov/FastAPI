import pandas as pd
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
import pytz
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def postgres_upsert(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_update(
        constraint=f"{table.table.name}_pkey",
        set_={c.key: c for c in insert_statement.excluded},
    )
    conn.execute(upsert_statement)

def get_cbr_data(date_sync):
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_sync}'
    df = pd.read_xml(url, encoding='cp1251')
    df.rename(columns={
        'ID': 'id'
        , 'NumCode': 'num_code'
        , 'CharCode': 'char_code'
        , 'Nominal': 'nominal'
        , 'Name': 'name'
        , 'Value': 'value'
        , 'VunitRate': 'v_unit_rate'
    }, inplace=True)
    df['value'] = df['value'].str.replace(',', '.').astype(float)
    df['v_unit_rate'] = df['v_unit_rate'].str.replace(',', '.').astype(float)
    df['cbr_date'] = datetime.strptime(date_sync, "%d/%m/%Y").date()
    df['update_date'] = datetime.now(tz=pytz.timezone('Asia/Yekaterinburg'))

    conn_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}'

    db = create_engine(conn_string)
    conn = db.connect()

    df.to_sql('cbr_currency', con=conn, schema='public', if_exists="append", method=postgres_upsert, index=False)
    print(f'Data for {date_sync} has been imported')

#date = datetime.now().strftime("%d/%m/%Y")

start_dt = date(2024, 12, 3)
end_dt = date.today()
delta = timedelta(days=1)

while start_dt <= end_dt:
    get_cbr_data(start_dt.strftime("%d/%m/%Y"))
    start_dt += delta