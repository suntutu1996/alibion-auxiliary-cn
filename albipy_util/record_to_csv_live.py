from AlbiPy import sniffing_thread
from AlbiPy import HEADERS
from time import sleep


def orders_to_csv(orders, filename):
    # 打开文件
    output_file = open(output_filename, "w")

    # 写入表头到文件
    output_file.write(",".join(HEADERS) + "\n")

    # 写入解析后的数据到文件
    for order in orders:
        output_file.write(",".join(list(map(str, order.data))) + "\n")

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
        try:
            orders = thread.get_data()
        except Exception as e:
            print(f"在获取订单时发生异常: {str(e)}")
            print("跳过此迭代并移动到下一个迭代...")
            continue

        print("将记录的订单写入", output_filename)
        orders_to_csv(orders, output_filename)
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
