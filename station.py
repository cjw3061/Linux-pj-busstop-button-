import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep

MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MY_ID = "22"  # 사용자 ID 설정
MQTT_TOPIC = f"mobile/{MY_ID}/sensing"

BUTTON = 24
LED = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

led_state = False 
button_pressed = False 

def on_message(client, userdata, message):
    global led_state
    if message.topic == MQTT_TOPIC:
        payload = message.payload.decode('utf-8')
        if payload == "정차":
            print("정차")
            if led_state:
                GPIO.output(LED, GPIO.LOW)
                led_state = False

client.on_message = on_message

client.subscribe(MQTT_TOPIC)

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.HIGH:
            
            if not button_pressed:  
                print("LED 켜짐")
                GPIO.output(LED, GPIO.HIGH)
                led_state = True
                value = "한밭대"
                client.publish(MQTT_TOPIC, value)
                print(f"MQTT 메시지 발행: {value}")
                button_pressed = True
            sleep(0.1)

except KeyboardInterrupt:
    print("종료합니다!!")

finally:
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()
