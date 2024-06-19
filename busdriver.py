import paho.mqtt.client as mqtt
from time import sleep
import json
import board
import neopixel
import RPi.GPIO as GPIO

MY_ID = "22"

MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_SUB_TOPIC = f"mobile/{MY_ID}/sensing"
MQTT_PUB_TOPIC = f"mobile/{MY_ID}/sensing"
STOP_MESSAGE = "정차"

pixel_pin = board.D10
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

BUTTON = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print(f"Received message from topic '{topic}': {payload}")

    if payload == "한밭대":
        pixels.fill((255, 0, 0))  
        pixels.show()
        print("한밭대 도착")
    elif payload == "삼성화재연수원":
        pixels.fill((0, 255, 0))  
        pixels.show()
        print("삼성화재연수원 도착")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.subscribe(MQTT_SUB_TOPIC)
client.loop_start()

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.HIGH:
            sleep(1.0)
            if GPIO.input(BUTTON) == GPIO.HIGH:
                pixels.fill((0, 0, 0))  
                pixels.show()
                print("정차했습니다.")
                client.publish(MQTT_PUB_TOPIC, STOP_MESSAGE)  
except KeyboardInterrupt:
    print("종료")
    pixels.fill((0, 0, 0))  
    pixels.show()
finally:
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()
