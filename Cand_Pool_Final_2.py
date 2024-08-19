import json
import pywikibot
from pywikibot import exceptions

from Cand_Pool_Funcs_2 import gather_results, blend_results


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


# 1. ace2004
gathered_results = gather_results("ED_Test_Datasets_BLINK/ace2004_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/ace2004_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/ace2004_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/ace2004_pred.jsonl", blended_results)
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
print("1 done " + "-" * 90)

# 2. aida
gathered_results = gather_results("ED_Test_Datasets_BLINK/aida_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/aida_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/aida_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/aida_pred.jsonl", blended_results)
print("2 done " + "-" * 90)

# 3. aquaint
gathered_results = gather_results("ED_Test_Datasets_BLINK/aquaint_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/aquaint_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/aquaint_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/aquaint_pred.jsonl", blended_results)
print("3 done " + "-" * 90)

# 4. cweb
gathered_results = gather_results("ED_Test_Datasets_BLINK/cweb_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/cweb_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/cweb_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/cweb_pred.jsonl", blended_results)
print("4 done " + "-" * 90)

# 5. graphq
gathered_results = gather_results("ED_Test_Datasets_BLINK/graphq_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/graphq_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/graphq_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/graphq_pred.jsonl", blended_results)
print("5 done " + "-" * 90)

# 6. mintaka
gathered_results = gather_results("ED_Test_Datasets_BLINK/mintaka_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/mintaka_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/mintaka_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/mintaka_pred.jsonl", blended_results)
print("6 done " + "-" * 90)

# 7. msnbc
gathered_results = gather_results("ED_Test_Datasets_BLINK/msnbc_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/msnbc_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/msnbc_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/msnbc_pred.jsonl", blended_results)
print("7 done " + "-" * 90)

# 8. reddit_comments
gathered_results = gather_results("ED_Test_Datasets_BLINK/reddit_comments_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/reddit_comments_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/reddit_comments_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/reddit_comments_pred.jsonl", blended_results)
print("8 done " + "-" * 90)

# 9. reddit_posts
gathered_results = gather_results("ED_Test_Datasets_BLINK/reddit_posts_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/reddit_posts_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/reddit_posts_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/reddit_posts_pred.jsonl", blended_results)
print("9 done " + "-" * 90)

# 10. shadow
gathered_results = gather_results("ED_Test_Datasets_BLINK/shadow_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/shadow_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/shadow_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/shadow_pred.jsonl", blended_results)
print("10 done " + "-" * 90)

# 11. tail
gathered_results = gather_results("ED_Test_Datasets_BLINK/tail_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/tail_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/tail_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/tail_pred.jsonl", blended_results)
print("11 done " + "-" * 90)

# 12. top
gathered_results = gather_results("ED_Test_Datasets_BLINK/top_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/top_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/top_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/top_pred.jsonl", blended_results)
print("12 done " + "-" * 90)

# 13. tweeki
gathered_results = gather_results("ED_Test_Datasets_BLINK/tweeki_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/tweeki_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/tweeki_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/tweeki_pred.jsonl", blended_results)
print("13 done " + "-" * 90)

# 14. webqsp
gathered_results = gather_results("ED_Test_Datasets_BLINK/webqsp_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/webqsp_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/webqsp_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/webqsp_pred.jsonl", blended_results)
print("14 done " + "-" * 90)

# 15. wiki
gathered_results = gather_results("ED_Test_Datasets_BLINK/wiki_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/wiki_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/wiki_pred.jsonl")
blended_results = blend_results(gathered_results)
write_jsonl("ED_Test_Datasets_All/wiki_pred.jsonl", blended_results)
print("15 done " + "-" * 90)