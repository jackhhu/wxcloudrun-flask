from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

from flask import Flask
import json
import datetime
import akshare as ak


# import tushare as ts 
# token='6f367740359ff6c86432dee3e3b8f8d09843c553adbc6f05c51f17aa'
# ts.set_token(token)
# pro=ts.pro_api(token)


# @app.route('/')
# def index():
#     """
#     :return: 返回index页面
#     """
#     missions = ['HC.SHF','RB.SHF']
# #     _,data_df1 = w.wss(missions, "open,high,low,close,MA","tradeDate=20220505;priceAdj=U;cycle=D;MA_N=5",usedf=True)
#     data_df1 = pro.daily(ts_code='300002.SZ', start_date='20200701', end_date='20201218')

#     data_df2 = data_df1.to_json()
# #     return render_template('index.html')
#     return data_df2




@app.route("/")
def index():
    futuredata=[]
    missions = ['ZC2209','RB2210','HC2210','J2209','JM2209','I2209','SF2209','SM2209',
                # 'FG2209','SA2209','AU2206','AG2206','CU2206','AL2206','ZN2206','PB2206',
                ]
    # missions = ['HC2210','SF2209']
    daytradecodes = ['SF','SM','AP','LH','PK','CJ']
    data_df1 = ak.futures_zh_spot(symbol=",".join(missions), market="CF", adjust='0')
    data_df1['pct'] = (data_df1['current_price']/data_df1['last_settle_price']-1)*100

    now = datetime.datetime.now()
    d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date())+'8:59', '%Y-%m-%d%H:%M')
    d_time2 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'15:00', '%Y-%m-%d%H:%M')
    d_time3 = datetime.datetime.strptime(str(datetime.datetime.now().date())+'20:59', '%Y-%m-%d%H:%M')

    i=0
    for mission in missions:
        futures_zh_daily_sina_df = ak.futures_zh_daily_sina(symbol=mission)         
        if (mission[:2] in daytradecodes):
            if ((now < d_time1) or (now > d_time2)):
                list_5 = futures_zh_daily_sina_df['close'].iloc[-5:]
                current_ma5 = list_5.mean()                
                list_20 = futures_zh_daily_sina_df['close'].iloc[-20:]
                current_ma20 = list_20.mean()       
                a1 = (current_ma5/current_ma20 - 1)*100
                a2 = (data_df1['current_price'].iloc[i]/current_ma20 - 1)*100 
            else:                        
                list_5 = futures_zh_daily_sina_df['close'].iloc[-4:]
                list_5[list_5.index[-1]+1] = data_df1['current_price'].iloc[i]
                current_ma5 = list_5.mean()
                                
                list_20 = futures_zh_daily_sina_df['close'].iloc[-19:]
                list_20[list_20.index[-1]+1] = data_df1['current_price'].iloc[i]
                current_ma20 = list_20.mean()
        
                a1 = (current_ma5/current_ma20 - 1)*100
                a2 = (data_df1['current_price'].iloc[i]/current_ma20 - 1)*100                 
        else:
            if ((now > d_time2) and (now < d_time3)):
                list_5 = futures_zh_daily_sina_df['close'].iloc[-5:]
                current_ma5 = list_5.mean()                
                list_20 = futures_zh_daily_sina_df['close'].iloc[-20:]
                current_ma20 = list_20.mean()       
                a1 = (current_ma5/current_ma20 - 1)*100
                a2 = (data_df1['current_price'].iloc[i]/current_ma20 - 1)*100                
            else:
                list_5 = futures_zh_daily_sina_df['close'].iloc[-4:]
                list_5[list_5.index[-1]+1] = data_df1['current_price'].iloc[i]
                current_ma5 = list_5.mean()
                
                list_20 = futures_zh_daily_sina_df['close'].iloc[-19:]
                list_20[list_20.index[-1]+1] = data_df1['current_price'].iloc[i]
                current_ma20 = list_20.mean()
        
                a1 = (current_ma5/current_ma20 - 1)*100
                a2 = (data_df1['current_price'].iloc[i]/current_ma20 - 1)*100         

        

 
    # for i in range(data_df1.shape[0]):
        dic = dict(code=data_df1['symbol'].iloc[i],
                   price= data_df1['current_price'].iloc[i],
                   pct= round(data_df1['pct'].iloc[i],2),                  
                   ma20= round(current_ma20,2),
                   line1= round(a1,2),
                   line2= round(a2,2),                 
                   )
        futuredata.append(dic)
        
        i = i+1
    
    print (futuredata)

    return json.dumps(futuredata)





@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
