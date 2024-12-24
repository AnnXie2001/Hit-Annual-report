需要自行从https://xyk.hit.edu.cn/爬虫获取校园卡消费信息记录。得到json串格式如下：
RO,OCCTIME,EFFECTDATE,MERCNAME,TRANAMT,TRANNAME,TRANCODE,CARDBAL,JDESC,JNUM,MACCOUNT,F1,F2,F3,SYSCODE,POSCODE,CMONEY,ZMONEY,ACCTYPENAME
301,2024-08-30 08:55:17,2024-08-30 08:53:46,校园车载POS,-1.0,扫码支付,99,31.58,二维码=[40961229043560415043] [reserve=40961229043560415043],3121778,1000339.0,1,11,2,58,64,31.58,31.58,电子账户
302,2024-08-30 08:05:00,2024-08-30 08:05:17,A17公寓浴池,-0.2,电子账户消费,94,32.58,"posno:2808,dealval:13,costunit:5 秒,发生时间2024-08-30 08:05",265448,1000007.0,1,11,2,37,8,32.58,32.58,电子账户

savefile.py文件用于合并多个json串。

convert.py文件用于额外增加json串信息内容。

show.py文件用于生成报告所需要的图表。

make_report.py用于生成年度消费记录markdown文件，采用VS code的Markdown PDF插件可创建PDF文件。
