"""Bai 3 - Smart light: nhan lenh ON/OFF va phan hoi trang thai."""

import json
import os
import sys

import paho.mqtt.client as mqtt

BROKER = os.environ.get("MQTT_BROKER", "test.mosquitto.org")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME", "")
PASSWORD = os.environ.get("MQTT_PASSWORD", "")
DEVICE_ID = "light01"
CMD_TOPIC = f"iot/lab/{DEVICE_ID}/cmd"
STATUS_TOPIC = f"iot/lab/{DEVICE_ID}/status"
LENH_HOP_LE = {"ON", "OFF"}

trang_thai = "OFF"


def tao_client(client_id: str) -> mqtt.Client:
    if hasattr(mqtt, "CallbackAPIVersion"):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    return mqtt.Client(client_id=client_id)


def payload_trang_thai() -> str:
    return json.dumps(
        {"device_id": DEVICE_ID, "status": trang_thai},
        separators=(",", ":"),
    )


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Da ket noi broker {BROKER}:{PORT}")
        client.subscribe(CMD_TOPIC, qos=1)
        print(f"Dang lang nghe lenh: {CMD_TOPIC}")
        client.publish(STATUS_TOPIC, payload_trang_thai(), qos=1)
        print(f"Trang thai ban dau: {payload_trang_thai()}")
        print("Nhan Ctrl+C de dung thiet bi.")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    global trang_thai
    lenh = msg.payload.decode("utf-8", errors="replace").strip().upper()
    print(f"Nhan lenh: {lenh}")
    if lenh not in LENH_HOP_LE:
        print("Lenh khong hop le. Chi chap nhan ON hoac OFF.")
        return

    trang_thai = lenh
    noi_dung = payload_trang_thai()
    client.publish(STATUS_TOPIC, noi_dung, qos=1)
    print(f"Da gui trang thai moi: {noi_dung}")


def main() -> None:
    client = tao_client(f"device-bai3-{DEVICE_ID}-{os.getpid()}")
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
        print("\nDa dung thiet bi.")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
