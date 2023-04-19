from datetime import datetime

data = "2023-05-02T08:25:50.759558"
data = datetime.strptime(data[0:19], "%Y-%m-%dT%H:%M:%S")

print(data)