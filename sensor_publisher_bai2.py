"""Bai 2 - Sensor publisher: gui nhiet do va do am dinh ky qua MQTT."""

import json
import os
import random
import sys
import time

import paho.mqtt.client as mqtt

BROKER = os.environ.get("MQTT_BROKER", "test.mosquitto.org")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME", "")
PASSWORD = os.environ.get("MQTT_PASSWORD", "")
# Them ma thiet bi vao danh sach nay de mo phong nhieu cam bien.
DEVICES = ["sensor01", "sensor02"]
CHU_KY_GIAY = 3


def tao_client(client_id: str) -> mqtt.Client:
    if hasattr(mqtt, "CallbackAPIVersion"):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    return mqtt.Client(client_id=client_id)


def sinh_du_lieu(device_id: str) -> dict:
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(25.0, 40.0), 1),
        "humidity": round(random.uniform(30.0, 80.0), 1),
    }


def main() -> None:
    client = tao_client(f"sensor-bai2-{os.getpid()}")
    da_ket_noi = {"ok": False}

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            da_ket_noi["ok"] = True
            print(f"Da ket noi broker {BROKER}:{PORT}")
        else:
            print(f"Ket noi that bai, ma loi: {rc}")

    client.on_connect = on_connect
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)

    print(f"Dang ket noi toi {BROKER}:{PORT} ...")
    try:
        client.connect(BROKER, PORT, keepalive=60)
    except OSError as exc:
        print(f"Khong ket noi duoc broker: {exc}")
        sys.exit(1)

    client.loop_start()
    for _ in range(40):
        if da_ket_noi["ok"]:
            break
        time.sleep(0.25)

    if not da_ket_noi["ok"]:
        print("Het thoi gian cho ket noi.")
        client.loop_stop()
        client.disconnect()
        sys.exit(1)

    print(f"Bat dau gui du lieu moi {CHU_KY_GIAY} giay. Nhan Ctrl+C de dung.")
    try:
        while True:
            for device_id in DEVICES:
                data = sinh_du_lieu(device_id)
                topic = f"iot/lab/{device_id}/data"
                payload = json.dumps(data)
                info = client.publish(topic, payload, qos=1)
                info.wait_for_publish(timeout=5)
                print(f"Da gui {topic}: {payload}")
            time.sleep(CHU_KY_GIAY)
    except KeyboardInterrupt:
        print("\nDa dung sensor publisher.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
