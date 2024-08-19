import json
import pywikibot
from pywikibot import exceptions

from Cand_Pool_Funcs_3 import gather_results, blend_results


# Create a function reading/writing jsonl file
def read_jsonl(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_object = json.loads(line.strip())
            result.append(json_object)
    return result

def write_jsonl(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(json.dumps(item) + '\n')


# 15. wiki
##########
print("Start")
##########
gathered_results = gather_results("ED_Test_Datasets_BLINK/wiki_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/wiki_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/wiki_pred.jsonl",
                                  "ED_Test_Datasets_GlobalED/wiki_pred.jsonl")
##########
print("Gathered")
##########
blended_results = blend_results(gathered_results)
##########
print("Blended")
##########
write_jsonl("ED_Test_Datasets_All/wiki_pred.jsonl", blended_results)
##########
print("15 done " + "-" * 90)
##########
print("Just Test")
print("-" * 90)
print(len(blended_results))
print("-" * 90)
print(len(blended_results[0]))
print("-" * 90)
print(len(blended_results[0]["predictions"]))
print("-" * 90)
for k in blended_results[0]["predictions"][0]:
    print(k)
print("-" * 90)
print("BLINK")
for m in range(len(blended_results[0]["predictions"])):
    print(len(blended_results[0]["predictions"][m]["predictions_blink"]))
print("-" * 90)
print("GENRE")
for m in range(len(blended_results[0]["predictions"])):
    print(len(blended_results[0]["predictions"][m]["predictions_genre"]))
print("-" * 90)
print("ReFinED")
for m in range(len(blended_results[0]["predictions"])):
    print(len(blended_results[0]["predictions"][m]["predictions_refined"]))
print("-" * 90)
print("All")
for m in range(len(blended_results[0]["predictions"])):
    print(len(blended_results[0]["predictions"][m]["predictions_all"]))
print("-" * 90)
##########