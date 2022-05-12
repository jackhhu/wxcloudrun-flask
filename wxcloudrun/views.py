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
import time
import re
from datetime import timedelta


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
    # 内盘数据
    missions = ['ZC2209','RB2210','HC2210','J2209','JM2209','I2209','SM2209','SF2209',
                'FG2209','SA2209','AU2206','AG2206','CU2206','AL2206','ZN2206','PB2206',
                'NI2206','SS2206','BU2206','FU2209','MA2209','PF2209','TA2209','EG2209','PP2209',
                'V2209','L2209','UR2209','Y2209','A2209','M2209','Y2209','C2209','CS2209',
                'RM2209','OI2209','P2209','AP2210','JD2209','SR2209','CF2209','CY2209',
                'RU2209','LH2209','PK2210',
                ]
    # missions = ['HC2210','SF2209','ZC2209','RB2210']
    daytradecodes = ['SF','SM','AP','LH','PK','CJ','JD']
    data_df1 = ak.futures_zh_spot(symbol=",".join(missions), market="CF", adjust='0')

    # data_df1 = ak.futures_main_sina(symbol="RB0", start_date="20220501", end_date="20220512")


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

        
        dic = dict(code=data_df1['symbol'].iloc[i],
                   price= data_df1['current_price'].iloc[i],
                   pct= round(data_df1['pct'].iloc[i],1),                  
                   ma20= round(current_ma20,2),
                   line1= round(a1,1),
                   line2= round(a2,1),                 
                   )
        futuredata.append(dic)
  
        dic4 = dict(ma20_code1 = data_df1['symbol'].iloc[i],
                   ma20_1 = round(current_ma20*1.0025,1),
                   ma20_2 = round(current_ma20*1.005,1),
                   ma20_3 = round(current_ma20*1.0075,1),
                   ma20_4 = round(current_ma20*1.01,1),      
                   )
        futuredata.append(dic4)

        dic5 = dict(ma20_code2 = data_df1['symbol'].iloc[i],   
                   ma20_5 = round(current_ma20*0.9975,1),
                   ma20_6 = round(current_ma20*0.995,1),
                   ma20_7 = round(current_ma20*0.9925,1),
                   ma20_8 = round(current_ma20*0.99,1),    
                   )
        futuredata.append(dic5)
      
        i = i+1

    # 外盘数据
    missions1 = ['GC','SI','CAD','AHD','ZSD','PBD','NID','SND',
                 'OIL','NG','S','SM','BO','C','FCPO','TRB',
                ]
    
    # print("开始接收实时行情, 每 3 秒刷新一次")
    # subscribe_list = ak.futures_foreign_commodity_subscribe_exchange_symbol()
    # while True:
    #     time.sleep(3)
    #     futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(subscribe_list=subscribe_list)
    #     print(futures_foreign_commodity_realtime_df)
    
    


    for mission in missions1: 
        futures_foreign_hist_df = ak.futures_foreign_hist(symbol=mission)
        pct_a1 =  ((futures_foreign_hist_df['close'].iloc[-1]/futures_foreign_hist_df['close'].iloc[-2])-1)*100
        list_5 = futures_foreign_hist_df['close'].iloc[-5:]
        current_ma5 = list_5.mean() 
        list_20 = futures_foreign_hist_df['close'].iloc[-20:]
        current_ma20 = list_20.mean() 
        a1 = (current_ma5/current_ma20 - 1)*100
        a2 = (futures_foreign_hist_df['close'].iloc[-1]/current_ma20 - 1)*100         
        # print (mission,futures_foreign_hist_df['close'].iloc[-1],pct_a1,current_ma20,a1,a2)
        # print (type(futures_foreign_hist_df['close'].iloc[-1]),type(pct_a1),type(current_ma20),type(a1),type(a2))
        
        dic6 = dict(code=mission,
                   price= futures_foreign_hist_df['close'].iloc[-1].astype('float'),
                   pct= round(pct_a1,1),                  
                   ma20= round(current_ma20,1),
                   line1= round(a1,1),
                   line2= round(a2,1),                 
                   )
        futuredata.append(dic6)


    
    # # 新闻联播
    # d_time4 = datetime.datetime.strptime(str(datetime.datetime.now().date())+'20:00', '%Y-%m-%d%H:%M')
    # if now < d_time4:
    #     cctv_day = datetime.datetime.now().date() - timedelta(days=1)
    # else:
    #     cctv_day = datetime.datetime.now().date()
        
    # data_df2 = ak.news_cctv(date=str(cctv_day.strftime('%Y%m%d')))
    
   
    # for i in range(data_df2.shape[0]):
    #     dic1 = dict(num = i+1,
    #                 title =data_df2['title'].iloc[i]              
    #                 )                
    #     futuredata.append(dic1)
        
    # mystr = data_df2[data_df2['title']=='国内联播快讯']['content'].iloc[0]
    # list_b = re.split(r'。', mystr)
    # list_b.remove("")
    # for i in range(len(list_b)):
    #     dic2 = dict(num = i+1,
    #                 title = list_b[i]              
    #                 )                
    #     futuredata.append(dic2)              
              

    # 实时新闻
#     data_df3 = ak.js_news(timestamp=now)
    data_df3 = ak.js_news(timestamp=now + timedelta(hours=8)- timedelta(minutes=1))
    for i in range(data_df3.shape[0]-1,0,-1):
        dic3 = dict(datetime =data_df3['datetime'].iloc[i][-8:],
                    content =data_df3['content'].iloc[i]              
                   )                
        futuredata.append(dic3)    
 
 

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
