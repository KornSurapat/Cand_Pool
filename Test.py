import pywikibot
from pywikibot import exceptions
from pywikibot.exceptions import NoPageError, InvalidTitleError, SiteDefinitionError

def wikidata_id_to_wikipedia_title(wikidata_id, site='en'):
    # Define the Wikidata site and the Wikipedia site
    wikidata_site = pywikibot.Site('wikidata', 'wikidata')
    wikipedia_site = pywikibot.Site(site, 'wikipedia')

    # Get the Wikidata item
    item = pywikibot.ItemPage(wikidata_site, wikidata_id)
    item.get()  # Load the item content

    # Get the Wikipedia title from the sitelinks
    wikipedia_title = item.sitelinks.get(f'{site}wiki')

    if wikipedia_title:
        return wikipedia_title
    else:
        return None

# Example usage
wikidata_id = "Q1397"  # Wikidata ID for Douglas Adams
wikipedia_title = wikidata_id_to_wikipedia_title(wikidata_id)

if wikipedia_title:
    print(f"The Wikipedia title for Wikidata ID {wikidata_id} is: {wikipedia_title}")
else:
    print(f"No Wikipedia title found for Wikidata ID {wikidata_id}")


# def get_wikidata_id(wikipedia_title):
#     # Connect to the English Wikipedia site
#     site = pywikibot.Site('en', 'wikipedia')
    
#     # Get the page object for the given title
#     page = pywikibot.Page(site, wikipedia_title)
    
#     # Check if the page exists
#     if not page.exists():
#         return None
    
#     # Get the Wikidata item associated with the page
#     item = pywikibot.ItemPage.fromPage(page)
    
#     # Return the Wikidata ID
#     return item.title()

# # Example usage
# wikipedia_title = "Bandar Seri Begawan"
# wikidata_id = get_wikidata_id(wikipedia_title)
# print(f"Wikidata ID for '{wikipedia_title}': {wikidata_id}")


# def get_wikipedia_title(wikidata_id, language='en'):
#     # Connect to Wikidata site
#     wikidata_site = pywikibot.Site('wikidata', 'wikidata')
    
#     # Get the Wikidata item using the Wikidata ID
#     item = pywikibot.ItemPage(wikidata_site, wikidata_id)
    
#     # Check if the item exists
#     if not item.exists():
#         return None
    
#     # Get the sitelink for the specified language Wikipedia
#     sitelinks = item.sitelinks
#     wiki_site = f'{language}wiki'
    
#     if wiki_site in sitelinks:
#         return sitelinks[wiki_site].title
#     else:
#         return None

# # Example usage
# wikidata_id = "Q16001327"  # Wikidata ID for Python (programming language)
# language = "en"  # English Wikipedia
# wikipedia_title = get_wikipedia_title(wikidata_id, language)
# print(f"Wikipedia title for Wikidata ID '{wikidata_id}' on {language} Wikipedia: {wikipedia_title}")


def get_wikidata_id(wikipedia_title, site_lang='en'):
    # Set up the site and repository
    site = pywikibot.Site(site_lang, 'wikipedia')
    repo = site.data_repository()

    try:
        # Fetch the page by title
        page = pywikibot.Page(site, wikipedia_title)
        # Fetch the item (Wikidata entity) for the page
        item = pywikibot.ItemPage.fromPage(page)

        # Return the Wikidata ID
        return item.id

    except exceptions.NoPageError:
        # Page does not exist on Wikipedia
        return None
    except exceptions.IsRedirectPageError:
        # Page is a redirect, follow the redirect
        page = page.getRedirectTarget()
        item = pywikibot.ItemPage.fromPage(page)
        return item.id
    except exceptions.NoWikibaseEntityError:
        # No Wikidata item associated with the page
        return None

# Example usage:
wikipedia_title = "Kaohsiung main station"
wikidata_id = get_wikidata_id(wikipedia_title)

if wikidata_id:
    print(f"Wikidata ID for '{wikipedia_title}' is {wikidata_id}")
else:
    print(f"No Wikidata ID found for '{wikipedia_title}'")


# # Set up the site and repository
# site = pywikibot.Site("en", "wikipedia")  # You can change 'en' to any other language code
# repo = site.data_repository()

# # Function to get Wikipedia title from Wikidata QID
# def get_wikipedia_title(qid):
#     try:
#         # Create the item object using the QID
#         item = pywikibot.ItemPage(repo, qid)
#         item.get()  # Fetch the item data

#         # Get the Wikipedia page title in the specified language
#         sitelinks = item.sitelinks
#         wikipedia_title = sitelinks.get(site.dbName())
        
#         if wikipedia_title:
#             return wikipedia_title
#         else:
#             return f"No Wikipedia page found for QID {qid}"
    
#     except NoPageError:
#         return f"Error: The QID {qid} does not exist on Wikidata."
#     except InvalidTitleError:
#         return f"Error: The QID {qid} is invalid."
#     except SiteDefinitionError:
#         return "Error: Site configuration is incorrect."
#     except Exception as e:
#         return f"An unexpected error occurred: {e}"

# # Example usage
# qid = "Q42"  # Replace with the desired QID
# title = get_wikipedia_title(qid)

# print(title)
# print(type(title))


# def get_wikipedia_title(wikidata_id, language='en'):
#     try:
#         # Connect to Wikidata site
#         wikidata_site = pywikibot.Site('wikidata', 'wikidata')
        
#         # Get the Wikidata item using the Wikidata ID
#         item = pywikibot.ItemPage(wikidata_site, wikidata_id)
#         # item.get()  # Fetch the item data
        
#         # Get the sitelink for the specified language Wikipedia
#         sitelinks = item.sitelinks
#         wiki_site = f'{language}wiki'
        
#         if wiki_site in sitelinks:
#             return sitelinks[wiki_site].title
#         else:
#             return f"No Wikipedia page found for Wikidata ID {wikidata_id} in {language} Wikipedia"
    
#     except NoPageError:
#         return f"Error: The Wikidata ID {wikidata_id} does not exist."
#     except InvalidTitleError:
#         return f"Error: The Wikidata ID {wikidata_id} is invalid."
#     except SiteDefinitionError:
#         return "Error: Site configuration is incorrect."
#     except Exception as e:
#         return f"An unexpected error occurred: {e}"

# # Example usage
# wikidata_id = "Q16001327"  # Wikidata ID for Python (programming language)
# language = "en"  # English Wikipedia
# wikipedia_title = get_wikipedia_title(wikidata_id, language)

# print(f"Wikipedia title for Wikidata ID '{wikidata_id}' on {language} Wikipedia: {wikipedia_title}")


# # Function to get Wikipedia title from Wikidata QID
# def get_wikipedia_title_from_qid(qid):
#     try:
#         site = pywikibot.Site("wikidata", "wikidata")
#         repo = site.data_repository()
#         item = pywikibot.ItemPage(repo, qid)
#         item.get()
        
#         # Check for the sitelinks
#         sitelinks = item.sitelinks
#         if 'enwiki' in sitelinks:
#             return sitelinks['enwiki'].title()
#         else:
#             return "No English Wikipedia link found."
#     except KeyError as e:
#         return f"KeyError: {e}"
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Example usage
# qid = 'Q16001327'
# title = get_wikipedia_title_from_qid(qid)
# print(f"Title: {title}")


# def get_wikipedia_title(wikidata_id):
#     try:
#         site = pywikibot.Site("wikidata", "wikidata")
#         item = pywikibot.ItemPage(site, wikidata_id)
#         sitelinks = item.sitelinks
#         if "enwiki" in sitelinks:
#             return sitelinks['enwiki'].title
#         else:
#             return None
#     except pywikibot.exceptions.NoPageError:
#         return None
#     except pywikibot.exceptions.IsRedirectPageError:
#         if not item.exists():
#             return None
#         sitelinks = item.sitelinks
#         if "enwiki" in sitelinks:
#             return sitelinks['enwiki'].title
#         else:
#             return None
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None
# print(get_wikipedia_title("Q16001327"))


# def get_wikipedia_title_2(wikidata_id, language='en'):
#     wikidata_site = pywikibot.Site('wikidata', 'wikidata')
#     item = pywikibot.ItemPage(wikidata_site, wikidata_id)
#     if not item.exists():
#         return None
#     sitelinks = item.sitelinks
#     wiki_site = f'{language}wiki'
#     if wiki_site in sitelinks:
#         return sitelinks[wiki_site].title
#     else:
#         return None
# print(get_wikipedia_title_2("Q16001327"))


# # Define the site
# site = pywikibot.Site('en', 'wikipedia')

# # Define the page title
# title = "Python (programming language)"

# # Create a page object
# page = pywikibot.Page(site, title)

# # Get the page URL
# url = page.full_url()

# # Get the page description
# description = page.text[:500]  # Get the first 500 characters of the page text

# print(f"URL: {url}")
# print(f"Description: {description}")



def get_wikipedia_page_info(title):
    try:
        # Define the site
        site = pywikibot.Site('en', 'wikipedia')

        # Create a page object
        page = pywikibot.Page(site, title)

        # Check if the page exists
        if not page.exists():
            return {"error": "The page does not exist."}

        # Get the page URL
        url = page.full_url()

        # Get the page description (first 500 characters)
        description = page.text[:500] if page.text else "No description available."

        return {
            "title": title,
            "url": url,
            "description": description
        }

    except pywikibot.exceptions.InvalidTitleError:
        return {"error": "The provided title is invalid."}
    except pywikibot.exceptions.NoPageError:
        return {"error": "The page does not exist."}
    except pywikibot.exceptions.PageRelatedError as e:
        return {"error": f"An error related to the page occurred: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# Example usage
title = "Bandar Seri Begawan"
page_info = get_wikipedia_page_info(title)

if "error" in page_info:
    print(f"Error: {page_info['error']}")
else:
    print(f"Title: {page_info['title']}")
    print(f"URL: {page_info['url']}")
    try: 
        print(f"Description: {page_info['description']}")
    except Exception as e:
        print(f"Description: An error occurs as {e}.")


def get_wikidata_info(qid):
    try:
        # Define the site
        site = pywikibot.Site('wikidata', 'wikidata')

        # Create a page object for the QID
        page = pywikibot.ItemPage(site, qid)

        # Check if the page exists
        if not page.exists():
            return {"error": "The page does not exist."}

        # Get the labels and descriptions in English
        labels = page.labels.get('en', 'No label available')
        descriptions = page.descriptions.get('en', 'No description available')

        # Construct the URL for the Wikidata page
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

# Example usage
qid = "Q9279"  # Example QID for Douglas Adams
wikidata_info = get_wikidata_info(qid)

if "error" in wikidata_info:
    print(f"Error: {wikidata_info['error']}")
else:
    print(f"QID: {wikidata_info['qid']}")
    print(f"Label: {wikidata_info['label']}")
    print(f"Description: {wikidata_info['description']}")
    print(f"URL: {wikidata_info['url']}")
