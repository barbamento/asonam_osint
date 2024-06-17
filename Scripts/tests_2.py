from Code.LLama.LLAMA import API
from Code.GeoData.GeoGuesser import GeoGeusser

ll = API("llava:34b-v1.6")

prompt = "describe the image"

prompt_geo = (
    "Locate this image! Use any thing in the picture you think "
    "could be useful, but do not search it online. Return the result in "
    "a json lists containing the national state, the region and the "
    "coordinates of the approximate location. Give me your three "
    "best predictionas a json list"
)

print(GeoGeusser().locate_position_llava("Dataset/archive/dataset/0.png"))

# print(ll.call_test(prompt_geo, "Dataset/archive/dataset/0.png"))
