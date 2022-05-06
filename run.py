# # 创建应用实例
# import sys

# from wxcloudrun import app

# # 启动Flask Web服务
# if __name__ == '__main__':
#     app.run(host=sys.argv[1], port=sys.argv[2])
    
    
from openpyxl import load_workbook
from WindPy import w
from pandas import DataFrame 
import pandas as pd
import datetime
import numpy 
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import matplotlib.pyplot as plt
import math
import numpy as np
from dateutil.relativedelta import relativedelta
import seaborn as sns
from matplotlib.lines import Line2D

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import RGBColor
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches
from PIL import Image
import mplfinance as mpf
import talib
import time
import sys
import dataframe_image as dfi 
sys.path.append(r'G:\python data\数据函数使用案例')
import A
w.start();
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.options.display.max_columns=15 
pd.options.display.width=20000
aa = A.jacktime()
[today,yesterday,today1,yesterday1,today2,today3,
  month_start,month_end,last_month_end,last_month_start,next_month_start,next_month_end,
  month_start1,month_end1,last_month_end1,last_month_start1,next_month_start1,next_month_end1,
  month_start2,month_end2,last_month_end2,last_month_start2,next_month_start2,next_month_end2,
  month_start3,month_end3,last_month_end3,last_month_start3,next_month_start3,next_month_end3,        
]=aa

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    date1 = "2022-04-01" 
    missions = ['ZC.CZC','RB.SHF',
        'HC.SHF','J.DCE','JM.DCE','I.DCE',
        'FG.CZC','AU.SHF','AG.SHF',
        'CU.SHF',
        'AL.SHF','ZN.SHF','PB.SHF',
        'NI.SHF','SN.SHF','SC.INE','FU.SHF',
        'BU.SHF','MA.CZC','TA.CZC','EG.DCE','PP.DCE','L.DCE','SA.CZC',
        'SP.SHF','A.DCE','M.DCE','Y.DCE','C.DCE','CS.DCE','RM.CZC','V.DCE',
        'OI.CZC','P.DCE','SR.CZC','CF.CZC','RU.SHF',
        'PG.DCE','EB.DCE','B.DCE','CY.CZC',
        ]
    # _,data_df1 = w.wsd(code,"open,high,low,close",yesterday,today, usedf=True)
    _,data_df1 = w.wss(missions, "open,high,low,close,MA","tradeDate=20220505;priceAdj=U;cycle=D;MA_N=5",usedf=True)
    _,data_df2 = w.wsq(missions, "rt_last", usedf=True)
    _,data_df3 = w.wss(missions, ",MA","tradeDate=20220505;priceAdj=U;cycle=D;MA_N=20",usedf=True)
    data_df1['最新价'] = data_df2['RT_LAST']
    data_df1['MA20'] = data_df3['MA']
    data_df1['code'] = data_df1.index.map(lambda x:x[:2])
    data_df1['5/20'] = data_df1['MA']/data_df1['MA20'] - 1
    data_df1['5/20 %'] = data_df1['5/20'].apply(lambda x: '%.2f%%' % (x*100))
    data_df1['最新/20'] = data_df1['最新价']/data_df1['MA20'] - 1
    data_df1['最新/20 %'] = data_df1['最新/20'].apply(lambda x: '%.2f%%' % (x*100))    
    data_df1['方向'] = data_df1['5/20'].map(lambda x:'多头' if x >0 else '空头')    
    
    # data_df1['最新价_text'] = data_df1['最新价']
    
    data_df1['message'] = data_df1['code'].map(str) + "-" + data_df1['最新价'].map(str)  + "-" + data_df1['方向'].map(str) + "-" + data_df1['5/20 %'].map(str)  + "-" + data_df1['最新/20 %'].map(str)  + "-" + data_df1['MA20'].map(str)

    # data_df2 = data_df1.to_html()
    data_df2 = data_df1.to_json()
    # df_styled = data_df1.style.background_gradient() 				
    # dfi.export(df_styled,"G:/C img/1.png") 
    return data_df2




if __name__ == '__main__':
    # app.run()

    app.run(host="0.0.0.0", port=8090)











