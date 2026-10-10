"""Bai 1 - Publisher: gui thong diep len topic iot/lab/message."""

import os
import sys
import time

import paho.mqtt.client as mqtt

# Sua thong tin sinh vien truoc khi nop bai.
HO_TEN = os.environ.get("MQTT_HO_TEN", "Nguyen Van A")
MA_SINH_VIEN = os.environ.get("MQTT_MA_SV", "B23DCCN001")
LOI_CHAO = "Xin chao tu client Python MQTT"

BROKER = os.environ.get("MQTT_BROKER", "test.mosquitto.org")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME", "")
PASSWORD = os.environ.get("MQTT_PASSWORD", "")
TOPIC = "iot/lab/message"
SO_THONG_DIEP = 3
KHOANG_CACH_GIAY = 1


def tao_client(client_id: str) -> mqtt.Client:
    if hasattr(mqtt, "CallbackAPIVersion"):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    return mqtt.Client(client_id=client_id)


def main() -> None:
    client = tao_client(f"publisher-bai1-{os.getpid()}")
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

    payload = f"{LOI_CHAO} - {MA_SINH_VIEN} - {HO_TEN}"
    try:
        for i in range(1, SO_THONG_DIEP + 1):
            info = client.publish(TOPIC, payload, qos=1)
            info.wait_for_publish(timeout=5)
            print(f"Da gui thong diep {i}/{SO_THONG_DIEP}")
            print(f"Topic: {TOPIC}")
            print(f"Payload: {payload}")
            if i < SO_THONG_DIEP:
                time.sleep(KHOANG_CACH_GIAY)
    finally:
        client.loop_stop()
        client.disconnect()
        print("Da ngat ket noi.")


if __name__ == "__main__":
    main()
