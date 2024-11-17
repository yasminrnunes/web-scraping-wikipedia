"""
This module scrapes Wikipedia categories and articles, extracting relevant data.
"""

import time
import logging
import random
from urllib.parse import unquote, urlparse
from typing import List, Dict, Any, Tuple

import requests
from bs4 import BeautifulSoup
from tenacity import retry, wait_exponential_jitter, stop_after_attempt

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
USER_AGENT = "WikipediaEduBot/1.0 (User:test; mailto:test@gmail.com)"


def _get_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


@retry(wait=wait_exponential_jitter(max=10, jitter=1), stop=stop_after_attempt(3))
def _fetch_and_parse_url_content(url: str) -> BeautifulSoup:
    """
    Fetches the URL and returns the BeautifulSoup object.
    """

    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching %s: %s", url, e)
        raise
    finally:
        wait_time = random.uniform(1, 2)
        time.sleep(wait_time)


def _process_sections_and_count_words(headings, termination_node):
    """
    Processes the headings and extracts word counts for their sections.
    Combines the logic of extracting text content and counting words.
    """
    sections = []

    for i, current_heading in enumerate(headings):
        next_heading = headings[i + 1] if i + 1 < len(headings) else None

        # Extract text content between headings (and skip style or termination node)
        siblings = current_heading.find_next_siblings()
        content = [
            sibling.get_text()
            for sibling in siblings
            if sibling != next_heading
            and sibling != termination_node
            and sibling.name != "style"
        ]

        # Combine the content and count words
        section_text = " ".join(content)
        sections.append(
            {
                "name": current_heading.find("h2").get_text(strip=True),
                "word_count": len(section_text.split()),
            }
        )

    return sections


def _fetch_article_data(article_url: str) -> Dict[str, Any]:
    """
    Fetches and processes data from a Wikipedia article.
    Args:
        article_url (str): The URL of the Wikipedia article to fetch.
    Returns:
        Dict[str, Any]: A dictionary containing the article's data, including:
            - id (str): The URL of the article.
            - name (str): The title of the article.
            - languages (List[str]): A list of URLs to the article in different languages.
            - sections (Dict[str, Any]): A dictionary containing the sections of the article and word counts.
    """
    soup = _fetch_and_parse_url_content(article_url)

    name = soup.find("span", class_="mw-page-title-main").text
    languages = [
        unquote(link["href"])
        for link in soup.find_all("a", class_="interlanguage-link-target", href=True)
    ]

    # process sections
    headings = soup.find_all(class_="mw-heading2")
    termination_node = soup.find(class_="mw-authority-control")
    sections = _process_sections_and_count_words(headings, termination_node)

    return {
        "id": unquote(article_url),
        "name": name,
        "languages": languages,
        "sections": sections,
    }


def _fetch_category_data(
    category_url: str,
    data: List[Dict[str, Any]],
    stats: Dict[str, int],
    parent_id: str = None,
    depth: int = 0,
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Fetches the category data and its articles recursively.
    """
    logging.info(f"{' ' * depth}Fetching category URL: %s", category_url)

    # Check that the category is not repeated
    for category in data:
        if category["id"] == category_url:
            logging.warning(f"{' ' * depth}Category already fetched: %s", category_url)
            return

    stats["categories"] += 1

    # Fetch the category URL
    soup = _fetch_and_parse_url_content(category_url)

    # Retrieve category information
    category_id = category_url
    category_name = soup.find("span", class_="mw-page-title-main").text
    category_languages = [
        unquote(link["href"])
        for link in soup.find_all("a", class_="interlanguage-link-target", href=True)
    ]

    # Process articles
    articles_urls = [
        unquote(_get_base_url(category_url) + link["href"])
        for link in soup.select("#mw-pages .mw-category a[href][title]")
    ]

    # Fetch each article with its sections
    articles = []
    for article_url in articles_urls:
        logging.info(f"{' ' * depth}-Fetching article URL: %s", article_url)
        article = _fetch_article_data(article_url)
        stats["sections"] += len(article["sections"])
        articles.append(article)

    stats["articles"] += len(articles)

    # Complete structure of the category
    data.append(
        {
            "id": category_url,
            "parent_id": parent_id,
            "name": category_name,
            "languages": category_languages,
            "articles": articles,
        }
    )

    # Informative messages
    logging.info(
        f"{' ' * depth}Category saved: %s with %d articles",
        category_name,
        len(articles),
    )

    # Fetch subcategories recursively
    for subcategory_link in soup.select(".CategoryTreeItem a[href][title]"):
        subcategory_href = subcategory_link.get("href")
        subcategory_url = unquote(_get_base_url(category_url) + subcategory_href)
        _fetch_category_data(
            subcategory_url,
            data,
            stats,
            category_id,  # parent_id
            depth + 1,  # Increase depth for subcategories
        )

    return data, stats


def scrape_category(url: str) -> List[Dict[str, Any]]:
    """
    Scrapes the given category URL and returns the data.
    """
    margin = len(url) + 20

    logging.info("%s", "=" * margin)
    logging.info("  Start Execution ".center(margin, "="))
    logging.info(f"  URL: {url} ".center(margin, "="))
    logging.info("%s", "=" * margin)

    data = []
    stats = {
        "categories": 0,
        "articles": 0,
        "sections": 0,
        "start_time": time.time(),
    }

    data, stats = _fetch_category_data(unquote(url), data, stats)

    # Format the output nicely in the console
    execution_time = round(time.time() - stats["start_time"], 2)

    # Imprimir resultados con formato
    logging.info("%s", "=" * margin)
    logging.info("  Finished Execution Summary ".center(margin, "="))
    logging.info(f"  URL: {url} ".center(margin, "="))
    logging.info("%s", "=" * margin)
    logging.info("%s %s", "Categories:".ljust(20), stats["categories"])
    logging.info("%s %s", "Articles:".ljust(20), stats["articles"])
    logging.info("%s %s", "Sections:".ljust(20), stats["sections"])
    logging.info("%s %ss", "Execution Time:".ljust(20), execution_time)
    logging.info(
        "%s %s articles/second",
        "Throughput:".ljust(20),
        round(stats["articles"] / execution_time, 2),
    )
    logging.info("%s", "=" * margin)
    return data
