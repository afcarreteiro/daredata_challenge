import requests

response = requests.post(
    "http://16.171.198.135:5000/predict",
    json={
        "idx": 150001,
        "features": {"attr_a": 1, "attr_b": "c", "scd_a": 0.55, "scd_b": 3},
    },
)

print(response.json())
