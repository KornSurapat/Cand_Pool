import json
import pywikibot
import numpy as np


qcode_to_title = {}
with open("qcode_to_title.jsonl", 'r', encoding='utf-8') as file:
    for line in file:
        if line == "\n": continue
        qcode_and_title = line.strip("\n")[1 : len(line) - 2].split(" -> ")
        qcode_to_title[qcode_and_title[0]] = qcode_and_title[1]

title_to_qcode = {}       
with open("title_to_qcode.jsonl", 'r', encoding='utf-8') as file:
    for line in file:
        if line == "\n": continue
        qcode_and_title = line.strip("\n")[1 : len(line) - 2].split(" -> ")
        title_to_qcode[qcode_and_title[0]] = qcode_and_title[1]

# Create functions converting between wikidata_id (qcode) and wikipedia_title (title)  
def get_wikidata_id(wikipedia_title):
    try:
        site = pywikibot.Site('en', 'wikipedia')
        page = pywikibot.Page(site, wikipedia_title)
        if not page.exists():
            return None
        item = pywikibot.ItemPage.fromPage(page)
        return item.title()
    except pywikibot.exceptions.NoPageError:
        return None
    except pywikibot.exceptions.IsRedirectPageError:
        page = page.getRedirectTarget()
        item = pywikibot.ItemPage.fromPage(page)
        return item.id
    except pywikibot.exceptions.NoWikibaseEntityError:
        return None
    except Exception as e:
        return None

def get_wikipedia_title(wikidata_id):
    try:
        site = pywikibot.Site("wikidata", "wikidata")
        item = pywikibot.ItemPage(site, wikidata_id)
        sitelinks = item.sitelinks
        if "enwiki" in sitelinks:
            return sitelinks['enwiki'].title
        else:
            return None
    except pywikibot.exceptions.NoPageError:
        return None
    except pywikibot.exceptions.IsRedirectPageError:
        if not item.exists():
            return None
        sitelinks = item.sitelinks
        if "enwiki" in sitelinks:
            return sitelinks['enwiki'].title
        else:
            return None
    except Exception as e:
        return None


# Create a function reading/appending jsonl file
def read_jsonl(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_object = json.loads(line.strip())
            result.append(json_object)
    return result

def append_jsonl_for_title_to_qcode(file_path, title, qcode):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write('\n' + json.dumps(str(title) + " -> " + str(qcode)))

def append_jsonl_for_qcode_to_title(file_path, qcode, title):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write('\n' + json.dumps(str(qcode) + " -> " + str(title)))


# Normalize function using softmax
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis = 0)


# Add BLINK's result
def add_result_blink(file_path_blink):
    result = read_jsonl(file_path_blink)
    # Normalize
    for d in range(len(result)):
        for m in range(len(result[d]["gold_spans"])):
            scores= []
            for p in range(len(result[d]["gold_spans"][m]["predictions_blink"])):
                scores.append(result[d]["gold_spans"][m]["predictions_blink"][p][1])
            if scores:
                normalized_scores = softmax(scores)
                for p in range(len(result[d]["gold_spans"][m]["predictions_blink"])):
                    result[d]["gold_spans"][m]["predictions_blink"][p][1] = normalized_scores[p]
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
                    # Append added title_to_qcode into title_to_qcode.jsonl
                    # append_jsonl_for_title_to_qcode("title_to_qcode.jsonl", result[d]["gold_spans"][m]["predictions_blink"][p][0], qcode)
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
    # Normalize
    for d in range(len(result)):
        for m in range(len(result[d]["gold_spans"])):
            scores= []
            for p in range(len(result[d]["gold_spans"][m]["predictions_genre"])):
                scores.append(result[d]["gold_spans"][m]["predictions_genre"][p][1])
            if scores:
                normalized_scores = softmax(scores)
                for p in range(len(result[d]["gold_spans"][m]["predictions_genre"])):
                    result[d]["gold_spans"][m]["predictions_genre"][p][1] = normalized_scores[p]
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
                    # Append added title_to_qcode into title_to_qcode.jsonl
                    # append_jsonl_for_title_to_qcode("title_to_qcode.jsonl", result[d]["gold_spans"][m]["predictions_genre"][p][0], qcode)
                added_result_genre[d]["predictions"][m]["predictions_genre"].append((
                    qcode, 
                    result[d]["gold_spans"][m]["predictions_genre"][p][0], 
                    result[d]["gold_spans"][m]["predictions_genre"][p][1]))
    return added_result_genre

# Add ReFinED's result
def add_result_refined(added_result_genre, file_path_refined):
    result = read_jsonl(file_path_refined)
    # Normalize
    for d in range(len(result)):
        for m in range(len(result[d]["gold_spans"])):
            scores= []
            for p in range(len(result[d]["gold_spans"][m]["predictions_refined"])):
                scores.append(result[d]["gold_spans"][m]["predictions_refined"][p]["score"])
            if scores:
                normalized_scores = softmax(scores)
                for p in range(len(result[d]["gold_spans"][m]["predictions_refined"])):
                    result[d]["gold_spans"][m]["predictions_refined"][p]["score"] = normalized_scores[p]
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
                    # Append added qcode_to_title into qcode_to_title.jsonl
                    # append_jsonl_for_qcode_to_title("qcode_to_title.jsonl", result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"], title)
                added_result_refined[d]["predictions"][m]["predictions_refined"].append((
                    result[d]["gold_spans"][m]["predictions_refined"][p]["wikidata_qid"], 
                    title, 
                    result[d]["gold_spans"][m]["predictions_refined"][p]["score"]))
    return added_result_refined


# Add GlobalED's result
def add_result_glabaled(added_result_refined, file_path_globaled):
    result = read_jsonl(file_path_globaled)
    # Normalize
    for d in range(len(result)):
        for m in range(len(result[d]["gold_spans"])):
            scores= []
            for p in range(len(result[d]["gold_spans"][m]["predictions_globaled"])):
                scores.append(result[d]["gold_spans"][m]["predictions_globaled"][p][1])
            if scores:
                normalized_scores = softmax(scores)
                for p in range(len(result[d]["gold_spans"][m]["predictions_globaled"])):
                    result[d]["gold_spans"][m]["predictions_globaled"][p][1] = normalized_scores[p]
    added_result_globaled = added_result_refined
    for d in range(len(result)):
        for m in range(len(result[d]["gold_spans"])):
            added_result_globaled[d]["predictions"][m]["predictions_globaled"] = []
            for p in range(len(result[d]["gold_spans"][m]["predictions_globaled"])):
                if result[d]["gold_spans"][m]["predictions_globaled"][p][0] != "[PAD]" and result[d]["gold_spans"][m]["predictions_globaled"][p][0] != "[UNK]" and result[d]["gold_spans"][m]["predictions_globaled"][p][0] != "[MASK]" and result[d]["gold_spans"][m]["predictions_globaled"][p][0] != "[MASK2]":
                    if result[d]["gold_spans"][m]["predictions_globaled"][p][0] in title_to_qcode:
                        qcode = title_to_qcode[result[d]["gold_spans"][m]["predictions_globaled"][p][0]]
                    else:
                        qcode = get_wikidata_id(result[d]["gold_spans"][m]["predictions_globaled"][p][0])
                        title_to_qcode[result[d]["gold_spans"][m]["predictions_globaled"][p][0]] = qcode
                        # Append added title_to_qcode into title_to_qcode.jsonl
                        # append_jsonl_for_title_to_qcode("title_to_qcode.jsonl", result[d]["gold_spans"][m]["predictions_globaled"][p][0], qcode)
                    added_result_globaled[d]["predictions"][m]["predictions_globaled"].append((
                        qcode, 
                        result[d]["gold_spans"][m]["predictions_globaled"][p][0], 
                        result[d]["gold_spans"][m]["predictions_globaled"][p][1]))
    return added_result_globaled


# Gather the results
def gather_results(file_path_blink, file_path_genre, file_path_refined, file_path_globaled):
    added_result_blink = add_result_blink(file_path_blink)
    added_result_genre = add_result_genre(added_result_blink, file_path_genre)
    added_result_refined = add_result_refined(added_result_genre, file_path_refined)
    added_result_globaled = add_result_glabaled(added_result_refined, file_path_globaled)
    return added_result_globaled


# Blend the results
def compare(p):
    return p[2]

def blend_results(gathered_results):
    for d in range(len(gathered_results)):
        for m in range(len(gathered_results[d]["predictions"])):
            predictions_all = {}
            # BLINK
            for p in range(len(gathered_results[d]["predictions"][m]["predictions_blink"])):
                predictions_all[str(gathered_results[d]["predictions"][m]["predictions_blink"][p][0]) + " <-> " +
                                str(gathered_results[d]["predictions"][m]["predictions_blink"][p][1])] = gathered_results[d]["predictions"][m]["predictions_blink"][p][2] * 0.25
            # Genre
            for p in range(len(gathered_results[d]["predictions"][m]["predictions_genre"])):
                if str(gathered_results[d]["predictions"][m]["predictions_genre"][p][0]) + " <-> " + str(gathered_results[d]["predictions"][m]["predictions_genre"][p][1]) in predictions_all:
                    predictions_all[str(gathered_results[d]["predictions"][m]["predictions_genre"][p][0]) + " <-> " + 
                                    str(gathered_results[d]["predictions"][m]["predictions_genre"][p][1])] += gathered_results[d]["predictions"][m]["predictions_genre"][p][2] * 0.25
                else:
                    predictions_all[str(gathered_results[d]["predictions"][m]["predictions_genre"][p][0]) + " <-> " + 
                                    str(gathered_results[d]["predictions"][m]["predictions_genre"][p][1])] = gathered_results[d]["predictions"][m]["predictions_genre"][p][2] * 0.25
            # ReFinED
            for p in range(len(gathered_results[d]["predictions"][m]["predictions_refined"])):
                if str(gathered_results[d]["predictions"][m]["predictions_refined"][p][0]) + " <-> " + str(gathered_results[d]["predictions"][m]["predictions_refined"][p][1]) in predictions_all:
                    predictions_all[str(gathered_results[d]["predictions"][m]["predictions_refined"][p][0]) + " <-> " + 
                                    str(gathered_results[d]["predictions"][m]["predictions_refined"][p][1])] += gathered_results[d]["predictions"][m]["predictions_refined"][p][2] * 0.25
                else:
                    predictions_all[str(gathered_results[d]["predictions"][m]["predictions_refined"][p][0]) + " <-> " + 
                                    str(gathered_results[d]["predictions"][m]["predictions_refined"][p][1])] = gathered_results[d]["predictions"][m]["predictions_refined"][p][2] * 0.25
            # GlobalED
            for p in range(len(gathered_results[d]["predictions"][m]["predictions_globaled"])):
                if str(gathered_results[d]["predictions"][m]["predictions_globaled"][p][0]) + " <-> " + str(gathered_results[d]["predictions"][m]["predictions_globaled"][p][1]) in predictions_all:
                    predictions_all[str(gathered_results[d]["predictions"][m]["predictions_globaled"][p][0]) + " <-> " + 
                                    str(gathered_results[d]["predictions"][m]["predictions_globaled"][p][1])] += gathered_results[d]["predictions"][m]["predictions_globaled"][p][2] * 0.25
                else:
                    predictions_all[str(gathered_results[d]["predictions"][m]["predictions_globaled"][p][0]) + " <-> " + 
                                    str(gathered_results[d]["predictions"][m]["predictions_globaled"][p][1])] = gathered_results[d]["predictions"][m]["predictions_globaled"][p][2] * 0.25
            # Transform
            transformed_predictions_all = []
            for k, v in predictions_all.items():
                l = k.split(" <-> ")
                transformed_predictions_all.append((l[0], l[1], v))
            transformed_predictions_all.sort(reverse = True, key = compare)
            gathered_results[d]["predictions"][m]["predictions_all"] = transformed_predictions_all
    return gathered_results