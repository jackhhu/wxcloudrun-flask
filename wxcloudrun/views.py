from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response



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



from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller



@app.route("/")
def index():


    
    chromedriver_autoinstaller.install()
    
    driver = webdriver.Chrome()
    
    urls =[
           # 'https://finance.sina.com.cn/futures/quotes/RB2210.shtml',
           # 'https://finance.sina.com.cn/futures/quotes/HC2210.shtml',
           # 'https://finance.sina.com.cn/futures/quotes/I2209.shtml',
           # 'https://finance.sina.com.cn/futures/quotes/J2209.shtml',
           'https://finance.sina.com.cn/futures/quotes/JM2209.shtml',        ]
    df2 = []
    for url in urls:
        # chromedriver  = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver'
        # driver = webdriver.Chrome(chromedriver)
        driver = webdriver.Chrome()
        
        # driver.get("http://www.python.org")
    
        headers = {'X-Requested-With': 'XMLHttpRequest','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    
        driver.get(url)
        # time.sleep(1) #这是为了让网页能够完全加载出来
        res = driver.page_source
        driver.close()
        soup = BeautifulSoup(res, "html.parser")
        news = soup.find_all('td',attrs = {"rowspan":"3"})
        df1 = []
        
        # for new in news:
        #     df1.append(new.text.strip().replace("\n","").replace("\r","").replace("\xa0","").replace("\t","")[0:22])         
        
        for new in news:
            df1.append(new.text)
        
        df2.append(df1[0]) 
        print (df2)

    return df2[0]







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
