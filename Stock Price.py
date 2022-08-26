'''
实现功能1：查询股票历史数据
实现功能2：预测股票走势
实现功能3：关注股票价格变动
'''

#-*- coding : utf-8 -*-
# coding: utf-8
import tkinter as tk
import pandas as pd
import numpy as np
import os
import threading
import time
import json
import requests
from joblib import dump, load
from datetime import datetime
from datetime import timedelta
from datetime import timezone

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

# 北京时间
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
beijing_now = utc_now.astimezone(SHA_TZ)

#创建一个窗口
window = tk.Tk()
#窗口的标题
window.title('my window')
#窗口的大小
window.geometry('1200x800')


# 功能1：一个label来显示结果，一个entry来获取用户要查询的股票，一个按钮来确认输入
df_stock = pd.read_csv('./stock2020 部分股票.csv')
# stock_code = tk.StringVar()
# l1 = tk.Label(window, textvariable=var1, bg='grey', font=('Arial', 12),
#              width=15, height=5).place(x=10, y=10, anchor='nw')
#
# e1 = tk.Entry(window, show=None).place(x=17.5, y=16, anchor='center')

l1 = tk.Label(window, text='股票信息', bg='grey', font=('Consolas', 12),width=25, height=20,
              justify='left', anchor='nw',wraplength=200)
# l1 = tk.Label(window, text='股票信息', bg='grey', font=('Arial', 12))
l1.place(x=10, y=10, anchor='nw')

e1 = tk.Entry(window, show=None)
e1.place(x=55, y=400)

# 获取股票信息
def financial_figure():
    k=0
    index = None
    stock_code = str(e1.get()) + '.SZ'
    for i in df_stock.index:
        if df_stock.loc[i]['SECUCODE'] == stock_code:
            k = 1
            index = i
            break
    if k==1:
        l1.config(
            text=f'股票名称：{df_stock.loc[index]["SECURITY_NAME_ABBR"]},\nBASIC_EPS:{df_stock.loc[index]["BASIC_EPS"]}, BPS:{df_stock.loc[index]["BPS"]}, '
                 f'PARENT_NETPROFIT:{df_stock.loc[index]["PARENT_NETPROFIT"]}, SJLHZ:{df_stock.loc[index]["SJLHZ"]}, SJLTZ:{df_stock.loc[index]["SJLTZ"]}, '
                 f'TOTAL_OPERATE_INCOME:{df_stock.loc[index]["TOTAL_OPERATE_INCOME"]}, WEIGHTAVG_ROE:{df_stock.loc[index]["WEIGHTAVG_ROE"]}, XSMLL:{df_stock.loc[index]["XSMLL"]}, '
                 f'YSHZ:{df_stock.loc[index]["YSHZ"]}, YSTZ:{df_stock.loc[index]["YSTZ"]}, MGJYXJJE:{df_stock.loc[index]["MGJYXJJE"]}')
    else:
        l1.config(text='没有此股票的信息！')

b1 = tk.Button(window, text='点击获取股票信息', width=15, height=2,
              command=financial_figure)
b1.place(x=70, y=430)


# 功能2：预测股票走势，输入股票代码，预测该股票近期价格走势
# 一个entry输入股票代码，一个label显示股票涨跌，一个button确认输入

l2 = tk.Label(window, text='输入股票财务信息，用","分隔开，指标包括有：营收同比增长，营收季度环比增长，净利润同比增长，净利润季度环比增长，'
                           '第四季度营收增长， 第四季度净利润增长，市盈率，市净率，股价变动，市盈率百分位，市净率百分位。',
              bg='grey', font=('Consolas', 12), width=25, height=20, justify='left', anchor='nw',wraplength=200)
l2.place(x=500, y=10)

rf = load('Random Forest.joblib')
e2 = tk.Entry(window, show=None)
e2.place(x=540, y=400)

def financial_predict():
    stock_figure_str = str(e2.get())
    stock_figure_str_list = stock_figure_str.split(',')
    stock_figure_float_list = list(map(float, stock_figure_str_list))
    stock_figure_series = pd.DataFrame(stock_figure_float_list)

    predict_result = rf.predict(stock_figure_series.T)
    if int(predict_result) == 0:
        l2.config(text=f'预测结果为：股价下跌')
    else:
        l2.config(text=f'预测结果为：股价上涨')


b2 = tk.Button(window, text='点击', width=15, height=2,
              command=financial_predict)
b2.place(x=555, y=430)

# 功能3：关注股票，通知股票变动
l3 = tk.Label(window, text='请输入股票代码', bg='grey', font=('Consolas', 12),width=25, height=20,
              justify='left', anchor='nw',wraplength=200)
# l1 = tk.Label(window, text='股票信息', bg='grey', font=('Arial', 12))
l3.place(x=960, y=10)

e3 = tk.Entry(window, show=None)
e3.place(x=1000, y=400)

def follow_stock():
    stock_code = str(e3.get())
    dict_param = {"code": stock_code, "market": "ab", "type": "stock"}
    s = json.dumps(dict_param)

    global timer  # 定义全局变量
    # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer = threading.Timer(86400, follow_stock)   # 10秒调用一次函数

    cookies = {
        'BIDUPSID': 'E99148484BB3A01B6E2E830FAA75F18A',
        'PSTM': '1637230443',
        '__yjs_duid': '1_48c4cd8c7d3a06c5066b8e8e6ef686c21637542441855',
        'MAWEBCUID': 'web_IamRvffbowDCTZJaYQqHvfnQFJboIaRsaXlhjwuusBbdHvgyfd',
        'BAIDUID': 'E99148484BB3A01B28F1FF63357708E1:SL=0:NR=10:FG=1',
        'BDUSS': '0ZOYk9XZ3VBa25kWG0wbUhPd09GbDl1OUxZaGpxNDZOY2tIc1ZraDA5ckowdGRpRVFBQUFBJCQAAAAAAAAAAAEAAADS-l9lZmZmZ2pqYgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMlFsGLJRbBiZ',
        'BDUSS_BFESS': '0ZOYk9XZ3VBa25kWG0wbUhPd09GbDl1OUxZaGpxNDZOY2tIc1ZraDA5ckowdGRpRVFBQUFBJCQAAAAAAAAAAAEAAADS-l9lZmZmZ2pqYgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMlFsGLJRbBiZ',
        'BAIDUID_BFESS': 'E99148484BB3A01B28F1FF63357708E1:SL=0:NR=10:FG=1',
        'rsv_i': 'd0b5CAxtjLqkUJHDc52ie%2BwOIs8AopzqEueWs15LW17Ik0P3xbH%2FKOa2MarHuWfYkS%2BxH39GcahRRK0G3jOUWCpTAbWwqXw',
        'BA_HECTOR': '8la524a08l8k0k80801hb8dm914',
        'BDORZ': 'AE84CDB3A529C0F8A2B9DCDD1D18B695',
        'SE_LAUNCH': '5%3A27599627_16%3A27599627',
        'BDPASSGATE': 'IlPT2AEptyoA_yiU4VK23kIN8efjMLK4AhXJSkpPQlStfCaWmhH3BrUrWz0HSieXBDP6wZTXebZda5XKXlVXa_EqnBsZp5pQeiXcxvqOucPTKtB88b1tINvsViEp9OXPbf-PxdYXQOVEUFoKewPJpuo4ivClbApwhPWFsELVg_bfWYSRBWn2r7aTY767O-0APNu5-fqfhCpDMpihVPXkSS3FbCJHFCAr70aOatY6C3D5rkoXJ3rLRMIxG8LdHWl80humBhOL5qeKEZIuvo1nSkVJ7_',
        'delPer': '0',
        'H_WISE_SIDS': '110085_127969_132547_180636_185633_188742_189755_191527_194085_196426_196527_197096_197471_197711_199568_204916_205709_206704_208721_208809_209568_210321_210443_210444_211953_212295_212533_212726_212739_212874_212967_213045_213079_213271_213359_213870_214094_214205_214379_214596_214642_214656_214799_215071_215108_215635_215731_215856_215957_216049_216252_216274_216305_216335_216342_216352_216354_216570_216596_216631_216635_216844_216884_216942_216963_217148_217184_217268_217343_217387_217411_217761_218020_218330_218399_218404_218444_218457_218463_218540_218548_218599',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://wap.baidu.com',
        'Referer': 'https://wap.baidu.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = (
        (f'stock', f'[{s}]'),
    )

    response = requests.get(
        'https://sp1.baidu.com/5LMDcjW6BwF3otqbppnN2DJv/finance.pae.baidu.com/selfselect/getlatestprice',
        headers=headers, params=params, cookies=cookies)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://sp1.baidu.com/5LMDcjW6BwF3otqbppnN2DJv/finance.pae.baidu.com/selfselect/getlatestprice?stock=%5B%7B%22code%22%3A%22600796%22%2C%22market%22%3A%22ab%22%2C%22type%22%3A%22stock%22%7D%5D', headers=headers, cookies=cookies)
    # 把获取到的数据拿出来，转换为字典
    dict_0 = eval(response.text)
    print(dict_0)
    list_0 = dict_0['Result']['stock']
    print(list_0)
    dict_1 = list_0[0]
    stock_price = dict_1['price']
    l3.config(text=f'{beijing_now}股票{stock_code}价格是{stock_price}')

    timer.start()    #启用定时器


# 关注股票按钮
b3 = tk.Button(window, text='关注该股票', width=15, height=2,
              command=follow_stock)
b3.place(x=1015, y=430)


#相当于一个大的while循环，如果没有这个循环，只执行一次就会结束
window.mainloop()