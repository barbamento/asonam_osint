import json
from Code.LLM.LLAMA import API as LLamaApi
from Code.LLM.Chatgpt import API as GptApi
from Code.Misc.Errors import AnswerFormattingError


class GeoGeusser:
    locate_position_prompt = (
        "I will give you some images and you will try to locate them.\n"
        "I am aware that some prediction could not be precise so don't "
        "worry about blurriness, accuracy or absence of landmarks.\n"
        "You will follow The following rules, and you won't broke them for any reason.\n"
        "Rule 1: You will ALWAYS give me 3 prediction based on the given image. "
        "if you are not sure or able to locate them with precision or the image "
        "is blurred or in low resolution, still give me your best picks.\n"
        "Rule 2: For each of the 3 predictions you MUST return me a python readable json."
        "Each json will have the following keyword: national_state and coordinates."
        "The coordinates must be formatted as a list of latitude and longitude, "
        "the national_state must be the nation name, and each field must be non-null.\n"
        # "Rule 3: you can use anything in the image you deem necessary to locate the image"
    )

    def __init__(self):
        pass

    def locate_position_llava(self, image_path: str, model: LLamaApi) -> dict:
        answer = model.call_image(self.locate_position_prompt, image_path)
        try:
            print(answer.count("```json"))
            if answer.count("```json") > 1:
                res = [
                    json.loads(answer.split("```json")[i + 1].split("```")[0])
                    for i in range(3)
                ]
                return res
            elif answer.count("```json") == 1:
                res = []
                for i in answer.split("```json")[1].split("```")[0].split(r"}"):
                    if r"{" in i:
                        res.append(json.loads(r"{" + i.split(r"{")[1] + r"}"))
                return res
            elif answer.count("```json") == 0 and r"{" in answer:
                res = []
                for i in answer.split(r"}"):
                    if r"{" in i:
                        res.append(json.loads(r"{" + i.split(r"{")[1] + r"}"))
                return res
            else:
                raise AnswerFormattingError("Answer can't be load as json")

        except Exception as e:
            print(answer)
            raise AnswerFormattingError("Answer can't be load as json")

    def locate_position_gpt(self, image_path: str, model: GptApi):
        answer = model.call_image(self.locate_position_prompt, image_path)
        try:
            if answer.count("```json") > 1:
                res = [
                    json.loads(answer.split("```json")[i + 1].split("```")[0])
                    for i in range(3)
                ]
                return res
            elif answer.count("```json") == 1:
                res = []
                for i in answer.split("```json")[1].split("```")[0].split(r"}"):
                    if r"{" in i:
                        res.append(json.loads(r"{" + i.split(r"{")[1] + r"}"))
                return res
            elif answer.count("```json") == 0 and r"{" in answer:
                res = []
                for i in answer.split(r"}"):
                    if r"{" in i:
                        res.append(json.loads(r"{" + i.split(r"{")[1] + r"}"))
                return res
            else:
                raise AnswerFormattingError("Answer can't be load as json")

        except Exception as e:
            print(answer)
            raise AnswerFormattingError("Answer can't be load as json")
