import json
from Code.LLama.LLAMA import API
from Code.Misc.Errors import AnswerFormattingError


class GeoGeusser:
    model = API("llava:34b-v1.6")
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

    locate_position_prompt_old2 = (
        "I want you to locate this image. Since it's not an easy task "
        "you should give me your three best prediction. You must not "
        "search the picture online for any reason, but you should use "
        "any element in the picture you deem usefull. You must give me "
        "a prediction in ANY POSSIBLE CASE, and i won't accept "
        "any kind of i can't answer you type of answer. "
        "You MUST give me an answer in the form of a json list, where "
        "eache prediction is a different json with the keywords: "
        "national_state, region and coordinates. The coordinates must be "
        "a list of latitude and logintude"
    )
    locate_position_prompt_old = (
        "Can you locate this image? Use any thing in the picture you think "
        "could be useful, but do not search it online. Return the result in "
        "a json lists containing the national state, the region and the "
        "coordinates of the approximate location. Give me your three "
        "best predictionas a json list, with no comment inside. Coordinates "
        "must use the latitude, longitude system."  # The key of each json should be: "
        # "'national_state', 'region', and 'coordinates'. If you are unsure still "
        # "try to guess"
    )
    locate_state_prompt = (
        "Analyze the given image and provide a list of exactly 3 states that "
        "are most likely based on the visual content. Consider factors such as "
        "geographical features, landmarks, architecture, vegetation, and any "
        "visible signs or text. Rank the states from most to least likely. I"
        "want the answer as a python list"
    )

    def __init__(self):
        pass

    def locate_state(self, image_path: str) -> str:
        return self.model.call_image(self.locate_state_prompt, image_path)

    def locate_position(self, image_path: str) -> dict:
        answer = self.model.call_image(self.locate_position_prompt, image_path)

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
