"""
This module provides functions to manage and query a JSON-based database of categories and articles.

Functions:
    load(key: str):

    read_categories(key: str) -> List[dict]:

    get_all_ids(key: str) -> List[str]:

    get_all_category_ids(key: str) -> List[str]:

    get_all_article_ids(key: str) -> List[str]:

    filter_matching_ids(ids: List[str], key: str) -> List[str]:

    filter_is_not_matching_ids(ids: List[str], key: str) -> List[str]:

    get_article_word_count(key: str, article_id: str) -> int:
"""
from typing import List
import json

database = {}
index = {}


def load(key: str):
    """
    Loads data from a JSON file into the database and creates an index.

    Args:
        key (str): The key used to identify the data and index.

    Raises:
        FileNotFoundError: If the JSON file corresponding to the key does not exist.
        json.JSONDecodeError: If the JSON file is not properly formatted.

    Side Effects:
        - Updates the global `database` dictionary with the loaded data.
        - Updates the global `index` dictionary with the created index.

    The function performs the following steps:
        1. Reads data from a JSON file named `data_<key>.json`.
        2. Loads the data into the `database` dictionary under the given key.
        3. Creates an index for the data and stores it in the `index` dictionary.
        4. Prints error messages if there are duplicate languages in the index.

    Example:
        load("example_key")
    """

    data = []
    with open(f"data_{key}.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # load database
    database[key] = data
    index[key] = {}

    # indexing
    for category in data:
        for language in category["languages"]:
            if index[key].get(language, None) is None:
                index[key][language] = category["id"]
            else:
                print(f"Error: {language} already exists in index for key {key}")
        for article in category["articles"]:
            for language in article["languages"]:
                if index[key].get(language, None) is None:
                    index[key][language] = article["id"]

    # Save index to a JSON file - debugging purposes
    # with open("index.json", "w", encoding="utf-8") as file:
    #     json.dump(index, file, ensure_ascii=False, indent=2)

def read_categories(key: str) -> List[dict]:
    """
    Retrieve categories from the database using the provided key.

    Args:
        key (str): The key to access the categories in the database.

    Returns:
        List[dict]: A list of dictionaries representing the categories.
    """
    return database[key]

def get_all_ids(key: str) -> List[str]:
    """
    Retrieve all IDs associated with a given key from the database.

    Args:
        key (str): The key to search for in the database.

    Returns:
        List[str]: A list of IDs found under the specified key. This includes IDs from both categories and articles within those categories.
    """
    ids = []
    if key in database:
        for category in database[key]:
            ids.append(category["id"])
            for article in category["articles"]:
                ids.append(article["id"])
    return ids

def get_all_category_ids(key: str) -> List[str]:
    """
    Retrieve all category IDs associated with a given key from the database.

    Args:
        key (str): The key to look up in the database.

    Returns:
        List[str]: A list of category IDs associated with the given key.
    """
    ids = []
    if key in database:
        for category in database[key]:
            ids.append(category["id"])
    return ids

def get_all_article_ids(key: str) -> List[str]:
    """
    Retrieve all article IDs for a given key from the database.

    Args:
        key (str): The key to search for in the database.

    Returns:
        List[str]: A list of article IDs associated with the given key.
    """
    ids = []
    if key in database:
        for category in database[key]:
            for article in category["articles"]:
                ids.append(article["id"])
    return ids

def filter_matching_ids(ids: List[str], key: str) -> List[str]:
    """
    Filters a list of IDs, returning only those that match a given key in the index.

    Args:
        ids (List[str]): A list of IDs to be filtered.
        key (str): The key to be used for filtering the IDs in the index.

    Returns:
        List[str]: A list of IDs that match the given key in the index.
    """
    matching_ids = []
    for id in ids:
        if index[key].get(id) is not None:
            matching_ids.append(id)
    return matching_ids

def filter_is_not_matching_ids(ids: List[str], key: str) -> List[str]:
    """
    Filter out IDs that do not match any entry in the index for the given key.

    Parameters:
    ids (List[str]): The list of IDs to filter.
    key (str): The key to identify the index.

    Returns:
    List[str]: A list of IDs that do not match any entry in the index.
    """
    filtered_ids = []
    for id in ids:
        if index[key].get(id) is None:
            filtered_ids.append(id)
    return filtered_ids

def get_article_word_count(key: str, article_id: str) -> int:
    """
    Get the total word count for a specific article by its ID.

    Parameters:
    key (str): The key to identify the database.
    article_id (str): The ID of the article to get the word count for.

    Returns:
    int: The total word count of the article.
    """
    word_count = 0
    if key in database:
        for category in database[key]:
            for article in category["articles"]:
                if article["id"] == article_id:
                    for section in article["sections"]:
                        word_count += section["word_count"]
                    break
    return word_count
