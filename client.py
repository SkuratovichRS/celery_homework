import time

import requests


def send_image(api_url: str, image_path: str):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = requests.post(api_url, files={"file": image_bytes})

    print(response.status_code)

    return response.json().get("task_id")


def get_image_id(api_url: str):
    response = requests.get(api_url)

    print(response.status_code)

    return response.json()


def get_image(api_url: str, image_id: str):
    url = f"{api_url}/{image_id}"
    print(url)
    response = requests.get(url)

    print(response.status_code)

    img_bytes = response.content

    with open(f"image_{image_id}.png", "wb") as img_file:
        img_file.write(img_bytes)


if __name__ == "__main__":
    task_id = send_image("http://localhost:5000/upscale", "lama_300px.png")
    print(task_id)
    status = None
    result = None
    while status not in ["SUCCESS", "FAILED"]:
        response_json = get_image_id(f"http://localhost:5000/tasks/{task_id}")
        status = response_json.get("status")
        result = response_json.get("result")
        print(status, result)
        time.sleep(1)
    if result is not None:
        get_image(f"http://localhost:5000/processed", result)
