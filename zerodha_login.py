from calendar import c
import re
import os

import requests
import json
import pandas as pd
from datetime import datetime,timedelta,date
from decouple import config

def main():
    # ### Specify Interval
    ## minute,2minute,3minute,5minute,10minute,15minute,60minute
    interval="minute"

    s = requests.Session()

    user_id = config('USER_ID')
    password = config('PASSWORD')

    # Load tokens from .env (assumed to be present)
    enctoken = config('ENCTOKEN')
    kf_session = config('KF_SESSION')
    public_token = config('PUBLIC_TOKEN')

    # Test validity
    headers = {'authorization': f"enctoken {enctoken}"}
    test_response = requests.get('https://kite.zerodha.com/oms/user/profile', headers=headers)
    if test_response.status_code != 200:
        # Invalid, login process
        login_url = "https://kite.zerodha.com/api/login"
        twofa_url = "https://kite.zerodha.com/api/twofa"
        r = s.post(login_url, data={"user_id": user_id, "password": password})
        j = json.loads(r.text)
        request_id = j['data']["request_id"]
        twofa_value = input('Enter 2FA value:\n')
        data = {"user_id": user_id, "request_id": request_id, "twofa_value": twofa_value}
        r = s.post(twofa_url, data=data)
        j = json.loads(r.text)
        my_cookies = requests.utils.dict_from_cookiejar(s.cookies)
        public_token = my_cookies['public_token']
        kf_session = my_cookies['kf_session']
        enctoken = my_cookies['enctoken']
        # Save to .env
        env_lines = []
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_lines = f.readlines()
        # Remove existing token lines
        env_lines = [line for line in env_lines if not any(token in line for token in ['ENCTOKEN=', 'KF_SESSION=', 'PUBLIC_TOKEN='])]
        # Add new
        env_lines.append(f'ENCTOKEN={enctoken}\n')
        env_lines.append(f'KF_SESSION={kf_session}\n')
        env_lines.append(f'PUBLIC_TOKEN={public_token}\n')
        with open('.env', 'w') as f:
            f.writelines(env_lines)
    else:
        # Valid, set cookies in session
        s.cookies.set('public_token', public_token)
        s.cookies.set('kf_session', kf_session)
        s.cookies.set('enctoken', enctoken)

    from_date_input = input('From Date as ddmmyyyy (or ddmm or dd):\n')
    to_date_input = input('To Date as ddmmyyyy (or ddmm or dd):\n')

    def parse_date(input_str):
        now = datetime.now()
        current_year = str(now.year)
        current_month = f"{now.month:02d}"
        if len(input_str) == 2:  # dd
            dd = input_str
            mm = current_month
            yyyy = current_year
        elif len(input_str) == 4:  # ddmm
            dd = input_str[:2]
            mm = input_str[2:]
            yyyy = current_year
        elif len(input_str) == 8:  # ddmmyyyy
            dd = input_str[:2]
            mm = input_str[2:4]
            yyyy = input_str[4:]
        else:
            raise ValueError("Invalid date format")
        return f"{yyyy}-{mm}-{dd}"

    from_date = parse_date(from_date_input)
    to_date = parse_date(to_date_input)
    query = {
        'enctoken': enctoken,
        'kf_session': kf_session,
        'public_token': public_token,
        'user_id': user_id,
        'oi': "1",
        'from': from_date,
        'to': to_date
            }
    print(query)

    headers = {'authorization': f"enctoken {enctoken}"}

    FR = from_date.replace("-",'/')
    TO = to_date.replace("-",'/')
    st = datetime.strptime(FR, '%Y/%m/%d').date()
    en = datetime.strptime(TO, '%Y/%m/%d').date()
    today = date.today()

    s_c = pd.read_csv("symbol_code.csv")
    s_c.set_index('SYMBOL',inplace=True)
    sc_dict = s_c.to_dict()
    sym_dict= sc_dict['CODE']

    # Filter sym_dict to only include symbols present in symbol_list.csv
    symbol_list_df = pd.read_csv("symbol_list.csv")
    desired_symbols = symbol_list_df['SYMBOL'].tolist()
    sym_dict = {k: v for k, v in sym_dict.items() if k in desired_symbols}

    for index,(symbol,ID ) in enumerate(sym_dict.items()):
        print(symbol)
        print(ID)
        i = index + 1

        theDate = st
        datalist = {}
        big_data = pd.DataFrame()
        while theDate<=en:
            NextDate = theDate + timedelta(30)
            if NextDate > today:
                NextDate = today
            dt_range = str(theDate)[:-9] + "&to=" + str(NextDate)
    #         print(dt_range)
            fetch_url = 'https://kite.zerodha.com/oms/instruments/historical/{0}/{1}'.format(ID,interval)
            data= s.get(url = fetch_url, headers=headers,params=query).json()

            x = data['data']
            y = x['candles']
            df = pd.DataFrame(y)

            df[0] = pd.to_datetime(df[0])
            df['date'] = df[0].dt.date
            df['time'] = df[0].dt.time
            df['date'] = df['date'].apply(lambda x: x.strftime('%Y%m%d'))
            df['time'] = df['time'].apply(lambda x: x.strftime('%H:%M'))
            df.rename(columns={0:'delete',1:'open',2:"high",3:"low",4:"close",5:"volume",6:"empty"},inplace = True)
            df.drop(["delete",'empty'],axis=1,inplace=True)
            df["symbol"] = symbol
            columns_seq = ['symbol','date','open','high','low','close','volume','time']
            df = df.reindex(columns=columns_seq)
            datalist[i] = df # dictionary i = 1,2,3......

            theDate = theDate + timedelta(30)
            big_data = pd.concat([big_data,df])
            # print(big_data)

        big_data.to_csv("{}{}.csv".format("symbol_data/",symbol), index=False,header=True)
        print(theDate)

if __name__ == "__main__":
    main()