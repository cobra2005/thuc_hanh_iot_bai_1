"""Bai 3 - Controller: gui lenh dieu khien den va nhan trang thai."""

import os
import sys
import time

import paho.mqtt.client as mqtt

BROKER = os.environ.get("MQTT_BROKER", "test.mosquitto.org")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME", "")
PASSWORD = os.environ.get("MQTT_PASSWORD", "")
DEVICE_ID = "light01"
CMD_TOPIC = f"iot/lab/{DEVICE_ID}/cmd"
STATUS_TOPIC = f"iot/lab/{DEVICE_ID}/status"
LENH_HOP_LE = {"ON", "OFF"}


def tao_client(client_id: str) -> mqtt.Client:
    if hasattr(mqtt, "CallbackAPIVersion"):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    return mqtt.Client(client_id=client_id)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Da ket noi broker {BROKER}:{PORT}")
        client.subscribe(STATUS_TOPIC, qos=1)
        print(f"Dang theo doi trang thai: {STATUS_TOPIC}")
    else:
        print(f"Ket noi that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
    noi_dung = msg.payload.decode("utf-8", errors="replace")
    print("Trang thai nhan duoc:")
    print(noi_dung)
    print()


def main() -> None:
    client = tao_client(f"controller-bai3-{os.getpid()}")
    da_ket_noi = {"ok": False}

    def on_connect_wait(client, userdata, flags, rc, properties=None):
        if rc == 0:
            da_ket_noi["ok"] = True
        on_connect(client, userdata, flags, rc)

    client.on_connect = on_connect_wait
    client.on_message = on_message
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

    print("Nhap ON, OFF hoac EXIT.")
    try:
        while True:
            try:
                lenh = input("Nhap lenh: ").strip().upper()
            except EOFError:
                print()
                break

            if lenh == "EXIT":
                print("Ket thuc chuong trinh.")
                break
            if lenh not in LENH_HOP_LE:
                print("Lenh khong hop le. Chi chap nhan ON, OFF hoac EXIT.")
                continue

            info = client.publish(CMD_TOPIC, lenh, qos=1)
            info.wait_for_publish(timeout=5)
            print(f"Da gui lenh {lenh} toi {DEVICE_ID}")
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nKet thuc chuong trinh.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
