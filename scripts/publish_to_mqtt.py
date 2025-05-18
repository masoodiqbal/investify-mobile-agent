import paho.mqtt.client as mqtt
import json
import time

BROKER = "broker.hivemq.com"         # public test broker (no password)
PORT = 1883
TOPIC = "sea/psx/snap/testdevice"    # use your device ID for uniqueness

def publish_snapshot(payload):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    client.publish(TOPIC, json.dumps(payload), qos=0)
    client.loop_stop()
    client.disconnect()
    print(f"Published snapshot to {TOPIC}")

if __name__ == "__main__":
    # Example: load your scraped JSON file
    with open("artifacts/day4/sample_snap_1.json", "r") as f:
        data = json.load(f)
    publish_snapshot(data)
