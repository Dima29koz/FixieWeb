import requests


def send_incident(name: str, emai: str, subject: str, description: str):
    requests.post(url='http://127.0.0.1:5000/api/create_incident',
                  json={
                      'name': name,
                      'email': emai,
                      'subject': subject,
                      'description': description,
                  })
