import socket
import json
import threading
import platform
from datetime import datetime
# 网络异常字符串列表
PROBLEMS = ["'", "$", "QH", "?8", "H@", "ZP"]

# 信息表头
HEADERS = ["Id", "每单位银价", "总银价", "数量", "品质等级", "是否已结束", "拍卖类型", "是否被买家领取", "是否被卖家领取", "卖家角色ID", "卖家名称",
           "买家角色ID", "买家名称", "物品类型ID", "物品组类型ID", "附魔等级", "品质等级", "到期时间", "引用ID"]

def local_ip():
    # 获取本地ip地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


class datapoint:
    """单个市场数据点，包含游戏api提供的所有可用数据"""

    def __init__(self, data):
        # data属性
        self.data = data[:]
        # 修正银价
        data[1] //= 10000
        data[2] //= 10000
        # 将过期日期转换为datetime对象
        data[17] = datetime.strptime(data[17][0:16], "%Y-%m-%dT%H:%M")
        # 将数据索引设置为属性
        self.Id = data[0]
        self.UnitPriceSilver = data[1]
        self.TotalPriceSilver = data[2]
        self.Amount = data[3]
        self.Tier = data[4]
        self.IsFinished = data[5]
        self.AuctionType = data[6]
        self.HasBuyerFetched = data[7]
        self.HasSellerFetched = data[8]
        self.SellerCharacterId = data[9]
        self.SellerName = data[10]
        self.BuyerCharacterId = data[11]
        self.BuyerName = data[12]
        self.ItemTypeId = data[13]
        self.ItemGroupTypeId = data[14]
        self.EnchantmentLevel = data[15]
        self.QualityLevel = data[16]
        self.Expires = data[17]
        self.ReferenceId = data[18]


class sniffer_data:
    """组织捕获的市场数据"""

    def __init__(self, logs, parsed, malformed):
        self.logs = logs[:]
        self.parsed = parsed[:]
        self.malformed = malformed[:]

    def __getitem__(self, i):
        return self.parsed[i]

    def __len__(self):
        return len(self.parsed)

    def __str__(self):
        parsed = [{HEADERS[j]: attribute for j, attribute in enumerate(i.data)} for i in self.parsed]
        return json.dumps({"logs": self.logs, "parsed": parsed, "malformed": self.malformed})


class sniffing_thread(threading.Thread):
    """捕获线程类"""

    def __init__(self, problems=PROBLEMS):
        threading.Thread.__init__(self)

        # 设置问题列表
        self.problems = problems

        # 定义线程属性
        self.n = 0
        self.e = 0
        self.parsed = []  # 解析后的数据
        self.malformed = []  # 解析失败的数据
        self.recording = False  # 是否在录制数据
        self.last_parsed = True  # 上一次解析是否成功
        # 记录日志列表，第一个占位符为字符串空值
        self.logs = [""]

        # 初始化 socket 对象
        if platform.system() != "Windows":
            self.sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        # Windows 环境下的 socket 设置
        if platform.system() == "Windows":
            self.sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW)
            self.sniffer.bind((local_ip(), 0))
            self.sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def run(self):
        # 将 recording 设为 True
        self.recording = True

        # 当线程正在录制时，嗅探并记录数据
        while self.recording:

            # 等待市场数据
            try:
                data = self.sniffer.recvfrom(1350)[0]
            except OSError:
                pass

            # 从数据中移除已知的问题字符串
            data = str(data)
            for p in self.problems:
                data = data.replace(p, "")

            # 将清理过的数据分成多个块
            chunks = [s[3:] for s in data.split("\\") if len(s) > 5 and ("Silver" in s or "ReferenceId" in s)]

            # 处理块
            for chunk in chunks:
                # 如果该块是市场信息的起始，就在日志列表中添加新的记录
                if "{" in chunk[:4]:
                    self.logs.append(chunk[chunk.find("{"):])
                # 否则，假定该块是上一个块的延续，并将其简单地连接到末尾
                elif self.logs:
                    self.logs[-1] += chunk

            # 设置 last_parsed 为 false
            self.last_parsed = False

        if not self.last_parsed:
            self.parse_data()

    def parse_data(self):
        """解析当前线程收集的数据"""
        self.parsed = []
        self.malformed = []
        if not self.logs[0]:
            self.logs.pop(0)
        for i, log in enumerate(self.logs):
            try:
                self.parsed.append(datapoint(list(json.loads(log).values())))
            except json.decoder.JSONDecodeError:
                self.malformed.append(self.logs[i])
        self.last_parsed = True

    def get_data(self):
        """获取最新的捕获线程数据"""
        # 如果没有记录任何日志
        if self.logs == [""]:
            return sniffer_data([], [], [])

        # 解析日志、记录格式错误的日志，并计算总日志数和格式错误的日志数
        if not self.last_parsed:
            self.parse_data()

        # 返回解析后的数据
        return sniffer_data(self.logs, self.parsed, self.malformed)

    def stop(self):
        """停止捕获线程"""
        self.recording = False

