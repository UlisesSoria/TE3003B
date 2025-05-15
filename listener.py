import paho.mqtt.client as mqtt
import json

# Dirección IP del broker MQTT (puede ser localhost o el IP del Puzzlebot)
BROKER = "localhost"  # o "192.168.x.x" si es tu Puzzlebot
PORT = 1883
TOPIC = "puzzlebot/goal"

def on_connect(client, userdata, flags, rc):
    print(f"🟢 Conectado al broker con código: {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"📩 Mensaje recibido en {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        x = payload.get("x")
        y = payload.get("y")
        theta = payload.get("theta")
        print(f"🧭 Coordenadas recibidas: x={x}, y={y}, θ={theta}")
    except json.JSONDecodeError:
        print("❌ Error al decodificar JSON")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🔄 Conectando al broker...")
client.connect(BROKER, PORT, 60)

client.loop_forever()
