import base64


def image_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def image_to_base64_2(file_path: str) -> str:
    with open(file_path, "rb") as img_file:
        base64_data = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_data}"
