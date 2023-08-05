# 基础数据rpc服务使用说明


## 安装

- pip install sense-data

## 配置

- 在settings.ini中配置连接信息，比如：

```yaml
[data_rpc]
host = 59.110.226.207
port = 5001
```

## 使用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService() #调用SenseDataService方法
```

## SenseDataService方法说明：
    
- 1-实时股价，输入股票代码，输出最新的股票数据，数据形式为model

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_stock_price_tick(stock_code)
```

- 2-公司基本信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），'000045'或[]或['000045','000046']，
得到公司基本信息，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_company_info(stock_code)
```

- 3-公司别名，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到公司的别名，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_company_alias(stock_code)
```

- 4-每日股价，输入股票代码字符串，输出该股票历史信息，有三种查询方式，data_server.get_stock_price_day('000020')，
输出有史以来的所有数据，数据形式为model列表；data_server.get_stock_price_day('000020', '2018-12-2')，
输出指定某一天的数据，数据形式为model；data_server.get_stock_price_day('000020', '2018-12-2', '2019-1-4')，
输出指定时间段的数据，数据形式为model列表；

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_stock_price_day('000020')
res_1 = data_server.get_stock_price_day('000020', '2018-12-2')
res_2 = data_server.get_stock_price_day('000020', '2018-12-2', '2019-1-4')
```

- 5-子公司，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到子公司信息，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_subcompany(stock_code)
```


- 6-行业概念信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），
得到股票对应的行业概念信息，输出形式为model，或model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_industry_concept(stock_code)
```


- 7-董监高信息，输入股票代码，允许的输入形式为股票字符串，或股票字符串+职位，输出懂事和监事的信息，每个人的数据形式是model，然后将对象存入列表中。

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_chairman_supervisor('000045') #输出该公司所有的董监高人员信息，
res_1 = data_server.get_chairman_supervisor('000045', '董事') #输出该公司所有的懂事人员信息
```

- 8-股东信息，输入股票代码，输出十大股东信息，每个股东的数据形式是model，然后将对象存入列表中

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_stockholder('000045')
```


- 9-返回前一个交易收盘日期，无参数，返回值形如'2019-1-28 03:00:00'的时间戳，是int型数据，李军用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_trade_date()
```


- 10-返回四大板块（深市主板、沪市主板、创业板和中小板）的股票涨跌幅，无参数，输出板块涨跌幅model，暂时不用了

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_market_rise_fall()
```


- 11-返回60左右个行业的股票涨跌幅数据，无参数，输出涨跌幅model，暂时不用了

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_industry_rise_fall()
```


- 12-返回股市中概念板块的涨跌幅数据，无参数，输出涨跌幅model，暂时不用了

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_concept_rise_fall()
```

- 13-给个实体名字（人名，子公司名）查询其在相关上市公司扮演的角色信息，输出形式为model组成的列表

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_entity_role('重庆富桂电子有限公司')
```


- 14-输入股票代码，返回风觅个股质押财务信息

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_financial_info(stock_code)
```


- 15-输入股票代码，返回总股本，子龙用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_total_shares(stock_code)
```

- 16-返回stock_codes中所有公司名，子龙用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
data_server = SenseDataService()
res = data_server.get_company_name()
```

- 17-输入文章标题，通过正则（新大洲控股|000571|新大洲A|新大洲），找到股票代码，广彬用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_title_code(stock_code)
```

- 18-输入股票代码，返回实控人信息，子龙用

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_actual_control_person(stock_code)
```

- 19-输入实体识别的名字，返回该实体下对应的公司信息

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
entity_name = '石化油服'
data_server = SenseDataService()
res = data_server.get_origin_info_by_name(entity_name)

res_example = [
    {
        "other_name":"石化油服",
        "company_full_name":"中石化石油工程技术服务股份有限公司",
        "company_name":"中石化油服",
        "company_code":"10004315",
        "stock_code":"01033",
        "plate":"港股-H股"
    },
    {
        "other_name":"石化油服",
        "company_full_name":"中石化石油工程技术服务股份有限公司",
        "company_name":"石化油服",
        "company_code":"10004315",
        "stock_code":"600871",
        "plate":"上证主板-A股"
    }
]
```

- 20-输入实体识别的名字，返回该实体下对应的公司信息，广彬用的数据结构

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
entity_name = '石化油服'
data_server = SenseDataService()
res = data_server.get_detail_info_by_name(entity_name)

res_example = {
    "company_code":"10004315",
    "other_name":"石化油服",
    "company_full_name":"中石化石油工程技术服务股份有限公司",
    "plate":[
        "上证主板-A股",
        "港股-H股"
    ],
    "plate_value":{
        "港股-H股":{
            "stock_code":"01033",
            "company_name":"中石化油服"
        },
        "上证主板-A股":{
            "stock_code":"600871",
            "company_name":"石化油服"
        }
    }
}

```

- 21-输入股票代码，返回该股票代码对应的公司所有人员和相关公司与该公司的关系

```python
import sense_core as sd
sd.log_init_config('data_server', sd.config('log_path'))
from sense_data import SenseDataService
stock_code = '000001'
data_server = SenseDataService()
res = data_server.get_company_role_info(stock_code)
res_example = {
    "stock_code":"600871",
    "plate":"上证主板-A股",
    "company_name":"石化油服",
    "company_full_name":"中石化石油工程技术服务股份有限公司",
    "person":{
        "刘中云":{
            "name":"刘中云",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "董事长",
                "法定代表人",
                "董事"
            ]
        },
        "卢立勇":{
            "name":"卢立勇",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "香港联交所授权代表"
            ]
        },
        "吴朝阳":{
            "name":"吴朝阳",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "香港联交所授权代表"
            ]
        },
        "姜波":{
            "name":"姜波",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "独立非执行董事"
            ]
        },
        "左尧久":{
            "name":"左尧久",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "副总经理"
            ]
        },
        "张剑波":{
            "name":"张剑波",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非职工代表监事"
            ]
        },
        "张永杰":{
            "name":"张永杰",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "副总经理"
            ]
        },
        "张洪山":{
            "name":"张洪山",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "职工代表监事"
            ]
        },
        "张琴":{
            "name":"张琴",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非职工代表监事"
            ]
        },
        "张锦宏":{
            "name":"张锦宏",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "副总经理"
            ]
        },
        "李天":{
            "name":"李天",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "总会计师"
            ]
        },
        "李洪海":{
            "name":"李洪海",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "董事会秘书"
            ]
        },
        "李炜":{
            "name":"李炜",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "职工代表监事",
                "监事会主席"
            ]
        },
        "杜江波":{
            "name":"杜江波",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非职工代表监事"
            ]
        },
        "樊中海":{
            "name":"樊中海",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非执行董事"
            ]
        },
        "沈泽宏":{
            "name":"沈泽宏",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "董事会助理秘书"
            ]
        },
        "潘颖":{
            "name":"潘颖",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "独立非执行董事"
            ]
        },
        "翟亚林":{
            "name":"翟亚林",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非职工代表监事"
            ]
        },
        "肖毅":{
            "name":"肖毅",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "董事"
            ]
        },
        "胡旭仓":{
            "name":"胡旭仓",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第10大流通股东"
            ]
        },
        "董秀成":{
            "name":"董秀成",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "独立非执行董事"
            ]
        },
        "蔡惜莲":{
            "name":"蔡惜莲",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第9大流通股东",
                "第10大股东"
            ]
        },
        "袁建强":{
            "name":"袁建强",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "董事",
                "总经理"
            ]
        },
        "路保平":{
            "name":"路保平",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非执行董事"
            ]
        },
        "陈卫东":{
            "name":"陈卫东",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "独立非执行董事"
            ]
        },
        "陈惟国":{
            "name":"陈惟国",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "职工监事"
            ]
        },
        "陈锡坤":{
            "name":"陈锡坤",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "执行董事",
                "副董事长"
            ]
        },
        "魏然":{
            "name":"魏然",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "非执行董事"
            ]
        }
    },
    "company":{
        "东海基金-兴业银行-华鑫信托-慧智投资47号结构化集合资金信托计划":{
            "name":"东海基金-兴业银行-华鑫信托-慧智投资47号结构化集合资金信托计划",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第5大流通股东",
                "第5大股东"
            ]
        },
        "东海基金-兴业银行-华鑫信托-慧智投资49号结构化集合资金信托计划":{
            "name":"东海基金-兴业银行-华鑫信托-慧智投资49号结构化集合资金信托计划",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第5大流通股东",
                "第5大股东"
            ]
        },
        "中国中信有限公司":{
            "name":"中国中信有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第3大流通股东",
                "第3大股东"
            ]
        },
        "中国石化集团国际石油工公司":{
            "name":"中国石化集团国际石油工公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司"
            ]
        },
        "中国石化集团国际石油工程有限公司":{
            "name":"中国石化集团国际石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司"
            ]
        },
        "中国石油化工集团有限公司":{
            "name":"中国石油化工集团有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第1大流通股东",
                "第1大股东"
            ]
        },
        "中威联合国际能源服务有限公司":{
            "name":"中威联合国际能源服务有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "合营企业",
                "合营企业"
            ]
        },
        "中石化中原石油工程有限公司":{
            "name":"中石化中原石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "中石化华东石油工程有限公司":{
            "name":"中石化华东石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "中石化华北石油工程有限公司":{
            "name":"中石化华北石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "中石化江汉石油工程有限公司":{
            "name":"中石化江汉石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "中石化海洋石油工程有限公司":{
            "name":"中石化海洋石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "中石化石油工程地球物理公司":{
            "name":"中石化石油工程地球物理公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司"
            ]
        },
        "中石化石油工程地球物理有限公司":{
            "name":"中石化石油工程地球物理有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司"
            ]
        },
        "中石化石油工程建设有限公司":{
            "name":"中石化石油工程建设有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "中石化石油工程技术服务公司":{
            "name":"中石化石油工程技术服务公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司"
            ]
        },
        "中石化石油工程技术服务有限公司":{
            "name":"中石化石油工程技术服务有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司"
            ]
        },
        "中石化胜利石油工程有限公司":{
            "name":"中石化胜利石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "中石化西南石油工程有限公司":{
            "name":"中石化西南石油工程有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司",
                "全资子公司"
            ]
        },
        "华安基金-兴业银行-中国对外经济贸易信托有限公司":{
            "name":"华安基金-兴业银行-中国对外经济贸易信托有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第7大流通股东",
                "第8大股东"
            ]
        },
        "华美孚泰油气增产技术服务有限责任公司":{
            "name":"华美孚泰油气增产技术服务有限责任公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "合营企业",
                "合营企业"
            ]
        },
        "江苏油服建设总公司":{
            "name":"江苏油服建设总公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "全资子公司"
            ]
        },
        "深圳市永泰投资有限公司":{
            "name":"深圳市永泰投资有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第8大流通股东",
                "第9大股东"
            ]
        },
        "迪瑞资产管理(杭州)有限公司":{
            "name":"迪瑞资产管理(杭州)有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第4大流通股东",
                "第4大股东"
            ]
        },
        "长江养老保险股份有限公司-长江盛世华章集合型团体养老保障管理产品进取增利2号组合":{
            "name":"长江养老保险股份有限公司-长江盛世华章集合型团体养老保障管理产品进取增利2号组合",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第7大股东"
            ]
        },
        "香港中央结算(代理人)有限公司":{
            "name":"香港中央结算(代理人)有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "第2大流通股东",
                "第2大股东"
            ]
        },
        "中石化石油工程技术服务股份有限公司":{
            "name":"中石化石油工程技术服务股份有限公司",
            "company_name":"石化油服",
            "stock_code":"600871",
            "role":[
                "上证主板-A股"
            ]
        }
    }
}
```









