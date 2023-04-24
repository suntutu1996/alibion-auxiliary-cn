from sqlalchemy import create_engine
import pandas as pd

# 假设你的数据库 URL 是这样的
db_url = 'mysql+pymysql://root:root@localhost:3306/alibion_market'

# 创建引擎对象
engine = create_engine(db_url)

# 从数据库中读取表格数据
df = pd.read_sql_query('SELECT * FROM market_data', con=engine)

# ... 然后可以对 df 进行操作，例如过滤、排序、聚合等