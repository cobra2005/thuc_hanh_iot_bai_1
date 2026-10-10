THUC HANH BUOI 1 - PYTHON MQTT
================================

1. Broker su dung
- Mac dinh: test.mosquitto.org, cong 1883, khong can tai khoan.
- Doi broker bang bien moi truong:
    export MQTT_BROKER=localhost
    export MQTT_PORT=1883
    export MQTT_USERNAME=user
    export MQTT_PASSWORD=secret
- Mosquitto local (Debian/Ubuntu):
    sudo apt install mosquitto mosquitto-clients
    sudo systemctl start mosquitto
    export MQTT_BROKER=localhost

2. Cai dat
    pip install -r requirements.txt

Sua HO_TEN va MA_SINH_VIEN trong publisher_bai1.py truoc khi chay bai 1.
Hoac:
    export MQTT_HO_TEN="Nguyen Van A"
    export MQTT_MA_SV="B23DCCN001"

3. Cach chay tung chuong trinh
Moi bai chay ben lang nghe truoc, ben gui sau. Dung chuong trinh dai bang Ctrl+C.

Bai 1
    python subscriber_bai1.py
    python publisher_bai1.py
Topic: iot/lab/message
Publisher gui 3 thong diep lien tiep (ho ten, ma sinh vien, loi chao).
Subscriber in topic, payload va thoi diem nhan.

Bai 2
    python monitor_subscriber_bai2.py
    python sensor_publisher_bai2.py
Topic: iot/lab/sensor01/data va iot/lab/sensor02/data
Payload JSON: device_id, temperature, humidity. Gui moi 3 giay.
Canh bao neu nhiet do > 35 C hoac do am < 40%.

Bai 3
    python device_bai3.py
    python controller_bai3.py
Lenh: iot/lab/light01/cmd (ON / OFF)
Trang thai: iot/lab/light01/status
Controller nhan ON, OFF, EXIT. Lenh sai se bi tu choi.

4. Ket qua dat duoc
- Ket noi broker, publish va subscribe dung topic.
- Bai 1 hien thi topic, noi dung va thoi diem nhan.
- Bai 2 gui JSON tuan hoan va canh bao dung nguong.
- Bai 3 dieu khien den hai chieu: lenh va phan hoi trang thai tach topic.
