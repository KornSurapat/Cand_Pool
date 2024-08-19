import json
import pywikibot
from pywikibot import exceptions

# Read qcode_to_title.txt and create a dictionary named qcode_to_title
qcode_to_title = {}
title_to_qcode = {}
with open("qcode_to_title.txt", "r", encoding="utf-8") as file:
    for line in file:
        qcode_and_title = line.split(" -> ")
        qcode_to_title[qcode_and_title[0]] = qcode_and_title[1][:-1]
        title_to_qcode[qcode_and_title[1][:-1]] = qcode_and_title[0]

# Create functions converting between wikidata_id (qcode) and wikipedia_title (title)  
def get_wikidata_id(wikipedia_title):
    site = pywikibot.Site('en', 'wikipedia')
    try:
        page = pywikibot.Page(site, wikipedia_title)
        if not page.exists():
            return None
        item = pywikibot.ItemPage.fromPage(page)
        return item.title()
    except exceptions.NoPageError:
        return None
    except exceptions.IsRedirectPageError:
        page = page.getRedirectTarget()
        item = pywikibot.ItemPage.fromPage(page)
        return item.id
    except exceptions.NoWikibaseEntityError:
        return None

def get_wikipedia_title(wikidata_id, language='en'):
    site = pywikibot.Site('wikidata', 'wikidata')
    item = pywikibot.ItemPage(site, wikidata_id)
    if not item.exists():
        return None
    sitelinks = item.sitelinks
    wiki_site = f'{language}wiki'
    if wiki_site in sitelinks:
        return sitelinks[wiki_site].title
    else:
        return None

# Create a function reading jsonl file
def read_jsonl(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for l in f:
            json_object = json.loads(l.strip())
            result.append(json_object)
    return result

# Add BLINK's result
def add_result_blink(file_path_blink):
    result = read_jsonl(file_path_blink)
    added_result_blink = []
    for d in range(len(result)):
        document = {}
        document["text"] = result[d]["text"]
        document["predictions"] = []
        for m in range(len(result[d]["gold_spans"])):
            mention = {}
            mention["start"] = result[d]["gold_spans"][m]["start"]
            mention["length"] = result[d]["gold_spans"][m]["length"]
            mention["predictions_blink"] = []
            for p in range(len(result[d]["gold_spans"][m]["predictions_blink"])):
                if result[d]["gold_spans"][m]["predictions_blink"][p][0] in title_to_qcode:
                    qcode = title_to_qcode[result[d]["gold_spans"][m]["predictions_blink"][p][0]]
                else:
                    qcode = get_wikidata_id(result[d]["gold_spans"][m]["predictions_blink"][p][0])
                    title_to_qcode[result[d]["gold_spans"][m]["predictions_blink"][p][0]] = qcode
                mention["predictions_blink"].append((
                    qcode, 
                    result[d]["gold_spans"][m]["predictions_blink"][p][0], 
                    result[d]["gold_spans"][m]["predictions_blink"][p][1]))
            document["predictions"].append(mention)
        added_result_blink.append(document)
    return added_result_blink

# Add GENRE's result
def add_result_genre(added_result_blink, file_path_genre):
    result = read_jsonl(file_path_genre)
    added_result_genre = added_result_blink
    for d in range(len(result)):
        for m in range(len(result[d]["gold_spans"])):
            added_result_genre[d]["predictions"][m]["predictions_genre"] = []
            for p in range(len(result[d]["gold_spans"][m]["predictions_genre"])):
                if result[d]["gold_spans"][m]["predictions_genre"][p][0] in title_to_qcode:
                    qcode = title_to_qcode[result[d]["gold_spans"][m]["predictions_genre"][p][0]]
                else:
                    qcode = get_wikidata_id(result[d]["gold_spans"][m]["predictions_genre"][p][0])
                    title_to_qcode[result[d]["gold_spans"][m]["predictions_genre"][p][0]] = qcode
                added_result_genre[d]["predictions"][m]["predictions_genre"].append((
                    qcode, 
                    result[d]["gold_spans"][m]["predictions_genre"][p][0], 
                    result[d]["gold_spans"][m]["predictions_genre"][p][1]))
    return added_result_genre

# Add ReFinED's result
def add_result_refined(added_result_genre, file_path_refined):
    result = read_jsonl(file_path_refined)
    added_result_refined = added_result_genre
    for d in range(len(result)):
        for m in range(len(result[d]["gold_spans"])):
            added_result_refined[d]["predictions"][m]["predictions_refined"] = []
            for p in range(len(result[d]["gold_spans"][m]["predictions_refined"])):
                if result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"] in qcode_to_title:
                    title = qcode_to_title[result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"]]
                elif result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"] == "Q-1":
                    continue
                else:
                    title = get_wikipedia_title(result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"])
                    qcode_to_title[result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"]] = title
                added_result_refined[d]["predictions"][m]["predictions_refined"].append((
                    result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"], 
                    title, 
                    result[d]["gold_spans"][m]["predictions_refined"][p]["score"]))
    return added_result_refined

# Gather the results
def gather_results(file_path_blink, file_path_genre, file_path_refined, file_path_globaled = ""):
    added_result_blink = add_result_blink(file_path_blink)
    added_result_genre = add_result_genre(added_result_blink, file_path_genre)
    added_result_refined = add_result_refined(added_result_genre, file_path_refined)
    return added_result_refined

# 1. ace2004
gathered_results = gather_results("ED_Test_Datasets_BLINK/ace2004_pred.jsonl",
                                  "ED_Test_Datasets_GENRE/ace2004_pred.jsonl", 
                                  "ED_Test_Datasets_ReFinED/ace2004_pred.jsonl")

print(len(gathered_results))
print()
print(len(gathered_results[0]))
print()
print(len(gathered_results[0]["predictions"]))
print()
for k in gathered_results[0]["predictions"][0]:
    print(k)
print()
print("BLINK")
for i in range(len(gathered_results[0]["predictions"])):
    print(len(gathered_results[0]["predictions"][i]["predictions_blink"]))
print()
print("GENRE")
for i in range(len(gathered_results[0]["predictions"])):
    print(len(gathered_results[0]["predictions"][i]["predictions_genre"]))
print()
print("ReFinED")
for i in range(len(gathered_results[0]["predictions"])):
    print(len(gathered_results[0]["predictions"][i]["predictions_refined"]))

# 2. aida
# 3. aquaint
# 4. cweb
# 5. graphq
# 6. mintaka
# 7. msnbc
# 8. reddit_comments
# 9. reddit_posts
# 10. shadow
# 11. tail
# 12. top
# 13. tweeki
# 14. webqsp
# 15. wiki