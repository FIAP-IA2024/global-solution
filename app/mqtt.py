import paho.mqtt.client as mqtt
import json
import random
import time
from database import save_event

BROKER = "test.mosquitto.org"
TOPIC = "home/events"
CONNECTED = False
PORT = 1883


def generate_random_event():
    device_id = random.randint(1, 5)
    event_type = random.choice(["state-change", "sensor-reading", "energy-consumption"])
    if event_type == "state-change":
        return {
            "device_id": device_id,
            "event_type": event_type,
            "value": random.choice(["on", "off"]),
        }
    elif event_type == "sensor-reading":
        return {
            "device_id": device_id,
            "event_type": event_type,
            "value": random.choice(["motion detected", "250 lux", "no motion"]),
        }
    elif event_type == "energy-consumption":
        return {
            "device_id": device_id,
            "event_type": event_type,
            "numeric_value": round(random.uniform(0.01, 5.0), 3),
        }


def on_connect(client, userdata, flags, rc):
    global CONNECTED
    if rc == 0:
        CONNECTED = True
        print(f"Connected to MQTT Broker: {BROKER}")
    else:
        print(f"Failed to connect, return code {rc}")


def main():
    global CONNECTED

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    client.loop_start()

    try:
        while not CONNECTED:
            print("Waiting for connection...")
            time.sleep(1)

        while True:
            event = generate_random_event()
            payload = json.dumps(event)

            # Publish event to MQTT Broker
            client.publish(TOPIC, payload)
            print(f"Published: {payload}")

            # Save event to database
            save_event(
                device_id=event["device_id"],
                event_type=event["event_type"],
                value=event.get("value"),
                numeric_value=event.get("numeric_value"),
            )

            print("Event saved to database.")

            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
