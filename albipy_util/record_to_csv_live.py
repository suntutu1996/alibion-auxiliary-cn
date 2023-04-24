from AlbiPy import sniffing_thread
from AlbiPy import HEADERS
from time import sleep
import pymysql

# 创建数据库连接
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='alibion_market'
)

# 获取游标
cursor = conn.cursor()


def orders_to_csv(orders, filename):
    # 打开文件
    output_file = open(output_filename, "w")

    # 写入表头到文件
    output_file.write(",".join(HEADERS) + "\n")

    # 写入解析后的数据到文件
    for order in orders:
        output_file.write(",".join(list(map(str, order.data))) + "\n")
        print(order.data)
        cursor.execute("""
            INSERT IGNORE INTO `market_data`
            (`Id`, `UnitPriceSilver`, `TotalPriceSilver`, `Amount`, `Tier`, `IsFinished`, `AuctionType`, `HasBuyerFetched`, `HasSellerFetched`, `SellerCharacterId`, `SellerName`, `BuyerCharacterId`, `BuyerName`, `ItemTypeId`, `ItemGroupTypeId`, `EnchantmentLevel`, `QualityLevel`, `Expires`, `ReferenceId`)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            order.Id,
            order.UnitPriceSilver,
            order.TotalPriceSilver,
            order.Amount,
            order.Tier,
            order.IsFinished,
            order.AuctionType,
            order.HasBuyerFetched,
            order.HasSellerFetched,
            order.SellerCharacterId,
            order.SellerName,
            order.BuyerCharacterId,
            order.BuyerName,
            order.ItemTypeId,
            order.ItemGroupTypeId,
            order.EnchantmentLevel,
            order.QualityLevel,
            order.Expires,
            order.ReferenceId
        ))

        # 提交事务
        conn.commit()

    # 关闭输出文件
    output_file.close()


# 获取用户输入的输出文件名
output_filename = input("输出 csv 文件名: ")

# 初始化并启动嗅探线程
print("启动嗅探线程...\n按 ctrl-c 停止记录并保存结果!")
thread = sniffing_thread()
thread.start()

# 每三秒获取记录的市场订单并写入文件
try:
    while True:
        print("等待三秒钟...")
        sleep(3)

        print("获取记录的订单...")
        orders = thread.get_data()


        print("将记录的订单写入", output_filename)
        orders_to_csv(orders.parsed, output_filename)
except KeyboardInterrupt:
    pass

# 停止嗅探线程
thread.stop()
print("\n线程已停止!")

# 获取捕获的数据
orders = thread.get_data()

# 将所有未写入的订单写入 csv 文件
print("将剩余订单写入", output_filename)
orders_to_csv(orders, output_filename)

# 关闭游标和数据库连接
cursor.close()
if conn.open:
    conn.close()