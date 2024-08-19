import pywikibot
import json

def read_jsonl(file_path):
  data = []
  with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
      json_object = json.loads(line.strip())
      data.append(json_object)
  return data

def write_jsonl(file_path, data):
  with open(file_path, 'w', encoding='utf-8') as file:
    for item in data:
      file.write(json.dumps(item) + '\n')

def get_wikidata_info(qid):
  try:
    site = pywikibot.Site('wikidata', 'wikidata')
    page = pywikibot.ItemPage(site, qid)
    if not page.exists():
      return {"error": "The page does not exist."}
    labels = page.labels.get('en', 'No label available')
    descriptions = page.descriptions.get('en', 'No description available')
    url = f"https://www.wikidata.org/wiki/{qid}"
    return {
      "qid": qid,
      "label": labels,
      "description": descriptions,
      "url": url
    }
  except pywikibot.exceptions.InvalidTitleError:
    return {"error": "The provided QID is invalid."}
  except pywikibot.exceptions.NoPageError:
    return {"error": "The page does not exist."}
  except pywikibot.exceptions.PageRelatedError as e:
    return {"error": f"An error related to the page occurred: {e}"}
  except Exception as e:
    return {"error": f"An unexpected error occurred: {e}"}

def add_description_and_link(file_path):
  result = read_jsonl(file_path)
  entities = read_jsonl("entity.jsonl")
  added_result = []
  for d in range(len(result)):
    document = {}
    document["text"] = result[d]["text"]
    document["predictions"] = []
    for m in range(len(result[d]["predictions"])):
      mention = {}
      mention["start"] = result[d]["predictions"][m]["start"]
      mention["length"] = result[d]["predictions"][m]["length"]
      mention["predictions_blink"] = result[d]["predictions"][m]["predictions_blink"]
      mention["predictions_genre"] = result[d]["predictions"][m]["predictions_genre"]
      mention["predictions_refined"] = result[d]["predictions"][m]["predictions_refined"]
      mention["predictions_globaled"] = result[d]["predictions"][m]["predictions_globaled"]
      mention["predictions_all"] = []
      for p in range(len(result[d]["predictions"][m]["predictions_all"])):
        prediction = {}
        prediction["wikidata_qid"] = result[d]["predictions"][m]["predictions_all"][p][0]
        prediction["wikipedia_title"] = result[d]["predictions"][m]["predictions_all"][p][1]
        prediction["score"] = result[d]["predictions"][m]["predictions_all"][p][2]
        # Add Wikipedia description and link
        if result[d]["predictions"][m]["predictions_all"][p][1] and result[d]["predictions"][m]["predictions_all"][p][1] != "None":
          found = False
          for ent in entities:
            if ent["title"] == result[d]["predictions"][m]["predictions_all"][p][1]:
              found = True
              wikipedia_description = ent["text"]
              wikipedia_link = ent["idx"]
              break
          if not found:
            wikipedia_description = None
            wikipedia_link = None
        else:
          wikipedia_description = None
          wikipedia_link = None
        prediction["wikipedia_description"] = wikipedia_description
        prediction["wikipedia_link"] = wikipedia_link
        # Add Wikidata description and link
        if result[d]["predictions"][m]["predictions_all"][p][0] and result[d]["predictions"][m]["predictions_all"][p][0] != "None":
          wikidata_info = get_wikidata_info(result[d]["predictions"][m]["predictions_all"][p][0])
          if "error" in wikidata_info:
            wikidata_description = None
            wikidata_link = None
          else:
            wikidata_description = wikidata_info["description"]
            wikidata_link = wikidata_info["url"]
        else:
          wikidata_description = None
          wikidata_link = None
        prediction["wikidata_description"] = wikidata_description
        prediction["wikidata_link"] = wikidata_link
        # Append completed prediction
        mention["predictions_all"].append(prediction)
      document["predictions"].append(mention)
    added_result.append(document)
  return added_result

##########
print("Start")
##########

# 1. ace2004
added_result = add_description_and_link("ED_Test_Datasets_All/ace2004_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/ace2004_pred.jsonl", added_result)
print("1 done " + "-" * 90)

# 2. aida
added_result = add_description_and_link("ED_Test_Datasets_All/aida_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/aida_pred.jsonl", added_result)
print("2 done " + "-" * 90)

# 3. aquaint
added_result = add_description_and_link("ED_Test_Datasets_All/aquaint_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/aquaint_pred.jsonl", added_result)
print("3 done " + "-" * 90)

# 4. cweb
added_result = add_description_and_link("ED_Test_Datasets_All/cweb_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/cweb_pred.jsonl", added_result)
print("4 done " + "-" * 90)

# 5. graphq
added_result = add_description_and_link("ED_Test_Datasets_All/graphq_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/graphq_pred.jsonl", added_result)
print("5 done " + "-" * 90)

# 6. mintaka
added_result = add_description_and_link("ED_Test_Datasets_All/mintaka_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/mintaka_pred.jsonl", added_result)
print("6 done " + "-" * 90)

# 7. msnbc
added_result = add_description_and_link("ED_Test_Datasets_All/msnbc_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/msnbc_pred.jsonl", added_result)
print("7 done " + "-" * 90)

# 8. reddit_comments
added_result = add_description_and_link("ED_Test_Datasets_All/reddit_comments_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/reddit_comments_pred.jsonl", added_result)
print("8 done " + "-" * 90)

# 9. reddit_posts
added_result = add_description_and_link("ED_Test_Datasets_All/reddit_posts_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/reddit_posts_pred.jsonl", added_result)
print("9 done " + "-" * 90)

# 10. shadow
added_result = add_description_and_link("ED_Test_Datasets_All/shadow_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/shadow_pred.jsonl", added_result)
print("10 done " + "-" * 90)

# 11. tail
added_result = add_description_and_link("ED_Test_Datasets_All/tail_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/tail_pred.jsonl", added_result)
print("11 done " + "-" * 90)

# 12. top
added_result = add_description_and_link("ED_Test_Datasets_All/top_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/top_pred.jsonl", added_result)
print("12 done " + "-" * 90)

# 13. tweeki
added_result = add_description_and_link("ED_Test_Datasets_All/tweeki_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/tweeki_pred.jsonl", added_result)
print("13 done " + "-" * 90)

# 14. webqsp
added_result = add_description_and_link("ED_Test_Datasets_All/webqsp_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/webqsp_pred.jsonl", added_result)
print("14 done " + "-" * 90)

# 15. wiki
added_result = add_description_and_link("ED_Test_Datasets_All/wiki_pred.jsonl")
write_jsonl("Added_ED_Test_Datasets_All/wiki_pred.jsonl", added_result)
print("15 done " + "-" * 90)