import threading
import time
import random
from pymongo import MongoClient

# Conexão com o banco de dados MongoDB
client = MongoClient('localhost', 27017)
db = client.bancoiot
collection = db.sensores

# Função para simular o comportamento de um sensor
def sensor_simulador(nome_sensor):
    while True:
        temperatura = random.uniform(30, 40)
        print(f"{nome_sensor}: {temperatura}°C")
        
        # Atualiza o documento no banco de dados
        collection.update_one({"nomeSensor": nome_sensor}, {"$set": {"valorSensor": temperatura}})
        
        # Verifica se a temperatura está acima do limite
        if temperatura > 38:
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {nome_sensor}!")
            collection.update_one({"nomeSensor": nome_sensor}, {"$set": {"sensorAlarmado": True}})
            break
        
        time.sleep(random.uniform(1, 5))  # Tempo de espera aleatório

# Criação de três threads para simular três sensores
threads = []
sensores = ["Temp1", "Temp2", "Temp3"]

# Inicializa os documentos dos sensores no banco de dados
for sensor in sensores:
    collection.insert_one({"nomeSensor": sensor, "valorSensor": 0, "unidadeMedida": "C°", "sensorAlarmado": False})

for sensor in sensores:
    t = threading.Thread(target=sensor_simulador, args=(sensor,))
    threads.append(t)
    t.start()

# Espera todas as threads terminarem
for thread in threads:
    thread.join()
