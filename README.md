# Thực hành buổi 1: Python MQTT

Ba bài mô phỏng giám sát và điều khiển thiết bị IoT qua MQTT: gửi/nhận thông điệp, cảm biến nhiệt độ–độ ẩm, và đèn thông minh hai chiều.

## Broker sử dụng

Mặc định mọi chương trình kết nối tới broker công cộng:

- Host: `test.mosquitto.org`
- Port: `1883`
- Không cần username/password

Có thể đổi broker bằng biến môi trường, không cần sửa code:

```bash
export MQTT_BROKER=localhost
export MQTT_PORT=1883
export MQTT_USERNAME=user        # bỏ qua nếu broker không yêu cầu
export MQTT_PASSWORD=secret
```

### Chạy Mosquitto trên máy local

```bash
# Debian/Ubuntu
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

Sau đó đặt `MQTT_BROKER=localhost` trước khi chạy các file Python.

## Cài đặt

Yêu cầu Python 3.

```bash
pip install -r requirements.txt
```

Hoặc:

```bash
pip install paho-mqtt
```

## Sửa thông tin sinh viên (Bài 1)

Mở `publisher_bai1.py` và sửa hai hằng số đầu file:

- `HO_TEN`
- `MA_SINH_VIEN`

Hoặc truyền khi chạy:

```bash
export MQTT_HO_TEN="Nguyen Van A"
export MQTT_MA_SV="B23DCCN001"
```

## Cách chạy

Mỗi bài cần **hai terminal**: một chương trình lắng nghe, một chương trình gửi. Chạy bên lắng nghe trước.

### Bài 1 — Publisher / Subscriber

Terminal 1:

```bash
python subscriber_bai1.py
```

Terminal 2:

```bash
python publisher_bai1.py
```

Publisher gửi 3 thông điệp liên tiếp lên `iot/lab/message`. Subscriber in topic, nội dung và thời điểm nhận, rồi chạy đến khi nhấn Ctrl+C.

Ví dụ phía subscriber:

```text
Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN001 - Nguyen Van A
Time: 10:15:20
```

### Bài 2 — Cảm biến và giám sát

Terminal 1:

```bash
python monitor_subscriber_bai2.py
```

Terminal 2:

```bash
python sensor_publisher_bai2.py
```

Cảm biến gửi JSON mỗi 3 giây lên:

- `iot/lab/sensor01/data`
- `iot/lab/sensor02/data`

Payload:

```json
{"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}
```

Nhiệt độ ngẫu nhiên trong khoảng 25–40°C, độ ẩm 30–80%. Monitor cảnh báo khi nhiệt độ > 35°C hoặc độ ẩm < 40%. Cả hai chương trình dừng bằng Ctrl+C.

### Bài 3 — Đèn thông minh

Terminal 1 (thiết bị):

```bash
python device_bai3.py
```

Terminal 2 (điều khiển):

```bash
python controller_bai3.py
```

Trong controller, nhập `ON`, `OFF` hoặc `EXIT`.

- Lệnh điều khiển: `iot/lab/light01/cmd`
- Trạng thái phản hồi: `iot/lab/light01/status`

Thiết bị chỉ chấp nhận `ON` và `OFF`. Lệnh khác bị từ chối, trạng thái không đổi. `EXIT` kết thúc controller.

Ví dụ:

```text
Nhap lenh: ON
Da gui lenh ON toi light01

Trang thai nhan duoc:
{"device_id":"light01","status":"ON"}
```

## Kết quả đạt được

- Kết nối được MQTT broker, publish và subscribe đúng topic.
- Bài 1 in đủ topic, payload và thời điểm nhận.
- Bài 2 gửi JSON định kỳ và cảnh báo đúng ngưỡng nhiệt độ, độ ẩm.
- Bài 3 điều khiển đèn hai chiều: lệnh đi một topic, trạng thái trả về topic khác.
