import json
import wikipedia_scrapping as ws
import graphics as gr

# Small category
# urls = {
#     "en": "https://en.wikipedia.org/wiki/Category:Volleyball_venues_in_Brazil",
#     "es": "https://es.wikipedia.org/wiki/Categoría:Pabellones_de_voleibol_de_Brasil"
# }

# Main category
# urls = {
#     "en": "https://en.wikipedia.org/wiki/Category:Volleyball_in_Brazil",
#     "es": "https://es.wikipedia.org/wiki/Categoría:Voleibol_en_Brasil"
# }

# Save data into json files
# for lang, url in urls.items():
#     data = ws.scrape_category(url)
#     with open(f"data_{lang}.json", "w", encoding="utf-8") as file:
#         json.dump(data, file, ensure_ascii=False, indent=2)

# CHART1 - BAR CHART - Quantity of Subcategories and Articles
gr.plot_quantity_of_subcategories_and_articles()

# CHART2 - PIE CHART - Distribution of Categories in English and Spanish
gr.plot_distribution_of_categories()

# CHART 3 - PIE CHART - Distribution of Articles in English and Spanish
gr.plot_distribution_of_articles()

# CHART 4 - PIE CHART - Distribution of Sections in English and Spanish
gr.plot_distribution_of_sections()

# CHART 5 - PIE CHART - Distribution of Duplicated Articles per language
gr.plot_distribution_of_duplicated_articles()

# CHART 6 - BAR CHART - Number of Categories in both languages and in each one
gr.plot_number_of_categories()

# CHART 7 - BAR CHART - Number of Unique Articles in both languages and in each one
gr.plot_number_of_unique_articles()

# CHART 8 - BOXPLOT - Articles Distribution per Category
gr.plot_articles_distribution_per_category()

# CHART 9 - BOXPLOT - Sections Distribution per Articles
gr.plot_sections_distribution_per_article()

# CHART 10 - BOXPLOT - Word Count Distribution per Articles
gr.plot_word_count_distribution_per_article()

# CHART 11 - BOXPLOT - Word Count Distribution per Articles in both languages and Quick Win
gr.plot_word_count_distribution_and_quick_win()