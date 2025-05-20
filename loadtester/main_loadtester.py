import time
import requests
import random

# URL del endpoint de la API
URL = "http://api:8000/predict"

# Posibles valores de entrada
islands = ["Torgersen", "Biscoe", "Dream"]
sexes = ["MALE", "FEMALE"]

def generate_random_input():
    return {
        "island": random.choice(islands),
        "sex": random.choice(sexes),
        "culmen_length_mm": round(random.uniform(35.0, 50.0), 1),
        "culmen_depth_mm": round(random.uniform(14.0, 22.0), 1),
        "flipper_length_mm": round(random.uniform(170.0, 230.0), 1),
        "body_mass_g": round(random.uniform(2700.0, 6000.0), 1)
    }

if __name__ == "__main__":
    while True:
        data = generate_random_input()
        try:
            response = requests.post(URL, json=data)
            print(f"Sent: {data} | Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)