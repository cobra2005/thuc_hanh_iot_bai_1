"""Bai 1 - Subscriber: lang nghe topic iot/lab/message."""

import os
import sys
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = os.environ.get("MQTT_BROKER", "test.mosquitto.org")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME", "")
PASSWORD = os.environ.get("MQTT_PASSWORD", "")
TOPIC = "iot/lab/message"


def tao_client(client_id: str) -> mqtt.Client:
    if hasattr(mqtt, "CallbackAPIVersion"):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    return mqtt.Client(client_id=client_id)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Da ket noi broker {BROKER}:{PORT}")
        client.subscribe(TOPIC, qos=1)
        print(f"Dang lang nghe topic: {TOPIC}")
        print("Nhan Ctrl+C de dung.")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    thoi_diem = datetime.now().strftime("%H:%M:%S")
    noi_dung = msg.payload.decode("utf-8", errors="replace")
    print("Nhan duoc message:")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {noi_dung}")
    print(f"Time: {thoi_diem}")
    print()


def main() -> None:
    client = tao_client(f"subscriber-bai1-{os.getpid()}")
    client.on_connect = on_connect
    client.on_message = on_message
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)

    print(f"Dang ket noi toi {BROKER}:{PORT} ...")
    try:
        client.connect(BROKER, PORT, keepalive=60)
    except OSError as exc:
        print(f"Khong ket noi duoc broker: {exc}")
        sys.exit(1)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDa dung subscriber.")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
