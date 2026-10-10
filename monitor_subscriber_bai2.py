"""Bai 2 - Monitoring subscriber: nhan du lieu cam bien va canh bao nguong."""

import json
import os
import sys

import paho.mqtt.client as mqtt

BROKER = os.environ.get("MQTT_BROKER", "test.mosquitto.org")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME", "")
PASSWORD = os.environ.get("MQTT_PASSWORD", "")
TOPICS = [
    ("iot/lab/sensor01/data", 1),
    ("iot/lab/sensor02/data", 1),
]
NGUONG_NHIET_DO = 35.0
NGUONG_DO_AM = 40.0


def tao_client(client_id: str) -> mqtt.Client:
    if hasattr(mqtt, "CallbackAPIVersion"):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    return mqtt.Client(client_id=client_id)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Da ket noi broker {BROKER}:{PORT}")
        client.subscribe(TOPICS)
        for topic, _qos in TOPICS:
            print(f"Dang lang nghe topic: {topic}")
        print("Nhan Ctrl+C de dung.")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        device_id = data["device_id"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Payload khong hop le tren {msg.topic}: {exc}")
        return

    print(f"Device: {device_id}")
    print(f"Temperature: {temperature} C")
    print(f"Humidity: {humidity} %")
    if temperature > NGUONG_NHIET_DO:
        print("CANH BAO: Nhiet do cao")
    if humidity < NGUONG_DO_AM:
        print("CANH BAO: Do am thap")
    print()


def main() -> None:
    client = tao_client(f"monitor-bai2-{os.getpid()}")
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
        print("\nDa dung monitor.")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
