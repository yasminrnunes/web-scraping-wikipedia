"""
This module processes and visualizes data related to categories, articles, and sections
in different languages using matplotlib and pandas.
"""
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba

import database as db

db.load("es")
db.load("en")

# DEFINIENDO VARIABLES
## Languages
language1 = "es"
label_language1 = "spanish"
language2 = "en"
label_language2 = "english"

## Colores
color_language2 = "#F9D448"
color_language1 = "#7CA655"
color_both = "#4495A2"
color_language2_transparency = to_rgba(color_language2, alpha=0.5)
color_language1_transparency = to_rgba(color_language1, alpha=0.5)
color_both_transparency = to_rgba(color_both, alpha=0.5)

# PROCESANDO DATOS
## Contando categories, articles and sections
categories_language1 = [cat for cat in db.read_categories(language1)]

total_categories_language1 = len(categories_language1)
total_articles_language1 = sum(
    len(cat["articles"]) for cat in [cat for cat in categories_language1]
)
total_sections_language1 = sum(
    len(article["sections"])  # Cuenta las sections de cada artículo
    for category in categories_language1  # Itera sobre las categorías
    for article in category["articles"]  # Itera sobre los artículos de cada categoría
)

categories_language2 = [cat for cat in db.read_categories(language2)]

total_categories_language2 = len(categories_language2)
total_articles_language2 = sum(len(cat["articles"]) for cat in categories_language2)
total_sections_language2 = sum(
    len(article["sections"])  # Cuenta las sections de cada artículo
    for category in categories_language2  # Itera sobre las categorías
    for article in category["articles"]  # Itera sobre los artículos de cada categoría
)

## Contando articles unicos
unique_articles_language1 = set()

for category in categories_language1:
    for article in category["articles"]:
        unique_articles_language1.add(article["id"])

total_unique_articles_language1 = len(unique_articles_language1)

unique_articles_language2 = set()

for category in categories_language2:
    for article in category["articles"]:
        unique_articles_language2.add(article["id"])

total_unique_articles_language2 = len(unique_articles_language2)

## Identificando las categorías de los artículos duplicados
set_unique_articles_language1 = set(unique_articles_language1)
all_article_ids_language1 = [article["id"] for article in db.read_categories(language1)]
set_all_articles_language1 = set(all_article_ids_language1)

categories_w_duplicated_articles_language1 = (
    set_all_articles_language1 - set_unique_articles_language1
)

set_unique_articles_language2 = set(unique_articles_language2)
all_article_ids_language2 = [article["id"] for article in db.read_categories(language2)]
set_all_articles_language2 = set(all_article_ids_language2)

categories_w_duplicated_articles_language2 = (
    set_all_articles_language2 - set_unique_articles_language2
)


## Contando categorias que están en los dos idiomas
total_categories_both = len(
    db.filter_matching_ids(db.get_all_category_ids(language2), language1)
)

## Contando categorias que solamente están en cada uno de los idiomas
total_categories_only_language1 = len(
    db.filter_is_not_matching_ids(db.get_all_category_ids(language1), language2)
)  # está en language 1 y no en language 2
total_categories_only_language2 = len(
    db.filter_is_not_matching_ids(db.get_all_category_ids(language2), language1)
)  # está en language 2 y no en language 1

## Contando articulos que están en los dos idiomas
total_unique_articles_both = len(
    set(db.filter_matching_ids(db.get_all_article_ids(language1), language2))
)

## Contando categorias que solamente están en cada uno de los idiomas
total_unique_articles_only_language1 = len(
    set(db.filter_is_not_matching_ids(db.get_all_article_ids(language1), language2))
)  # está en language 1 y no en language 2
total_unique_articles_only_language2 = len(
    set(db.filter_is_not_matching_ids(db.get_all_article_ids(language2), language1))
)  # está en language 1 y no en language 2

## Cantidad de articulos por categorias
categories_language1 = []
articles_count_language1 = []

for category in db.read_categories(language1):
    categories_language1.append(category["name"])
    articles_count_language1.append(len(category["articles"]))

df_category_articles_language1 = pd.DataFrame(
    {"categories": categories_language1, "articles_count": articles_count_language1}
)

categories_language2 = []
articles_count_language2 = []

for category in db.read_categories(language2):
    categories_language2.append(category["name"])
    articles_count_language2.append(len(category["articles"]))

df_category_articles_language2 = pd.DataFrame(
    {"categories": categories_language2, "articles_count": articles_count_language2}
)

## Cantidad de secciones y palabras por articulos unicos
result_data_language1 = []
processed_articles_language1 = set()

for category in db.read_categories(language1):
    for article in category["articles"]:
        if (
            article["id"] in unique_articles_language1
            and article["id"] not in processed_articles_language1
        ):
            # Contar la cantidad de secciones
            num_sections = len(article["sections"])
            # Calcular la suma de word_count
            total_word_count = sum(
                section["word_count"] for section in article["sections"]
            )
            # Añadir al resultado
            result_data_language1.append(
                {
                    "article": article["id"],
                    "sections_count": num_sections,
                    "total_word_count": total_word_count,
                }
            )
            # Marcar el artículo como procesado
            processed_articles_language1.add(article["id"])

df_unique_articles_language1 = pd.DataFrame(result_data_language1)

result_data_language2 = []
processed_articles_language2 = set()

for category in db.read_categories(language2):
    for article in category["articles"]:
        if (
            article["id"] in unique_articles_language2
            and article["id"] not in processed_articles_language2
        ):
            # Contar la cantidad de secciones
            num_sections = len(article["sections"])
            # Calcular la suma de word_count
            total_word_count = sum(
                section["word_count"] for section in article["sections"]
            )
            # Añadir al resultado
            result_data_language2.append(
                {
                    "article": article["id"],
                    "sections_count": num_sections,
                    "total_word_count": total_word_count,
                }
            )
            # Marcar el artículo como procesado
            processed_articles_language2.add(article["id"])

df_unique_articles_language2 = pd.DataFrame(result_data_language2)

## Articles traducidos con la cantidad de palabras
unique_article_url_both_language1 = list(
    set(db.filter_matching_ids(db.get_all_article_ids(language1), language2))
)

unique_article_desc_both_language1 = []

# Iterar sobre cada URL de unique_article_url_both_language1
for url in unique_article_url_both_language1:
    # Llamar a la función db.get_article_word_count con cada URL
    word_count = db.get_article_word_count(language1, url)

    # Agregar el resultado como un diccionario con 'url' y 'word_count'
    unique_article_desc_both_language1.append({"url": url, "word_count": word_count})


unique_article_url_both_language2 = list(
    set(db.filter_matching_ids(db.get_all_article_ids(language2), language1))
)

unique_article_desc_both_language2 = []

# Iterar sobre cada URL de unique_article_url_both_language1
for url in unique_article_url_both_language2:
    # Llamar a la función db.get_article_word_count con cada URL
    word_count = db.get_article_word_count(language2, url)

    # Agregar el resultado como un diccionario con 'url' y 'word_count'
    unique_article_desc_both_language2.append({"url": url, "word_count": word_count})

## Quick Win Articles a traducir
unique_articles_only_language1 = list(
    set(db.filter_is_not_matching_ids(db.get_all_article_ids(language1), language2))
)  # está en language 1 y no en language 2

unique_article_desc_only_language1 = []

### Iterar sobre cada URL de unique_article_url_both_language1
for url in unique_articles_only_language1:
    # Llamar a la función db.get_article_word_count con cada URL
    word_count = db.get_article_word_count(language1, url)

    # Agregar el resultado como un diccionario con 'url' y 'word_count'
    unique_article_desc_only_language1.append(
        {
            "url": url,
            "available language": language1,
            "word_count_to_translate": word_count,
        }
    )

unique_articles_only_language2 = list(
    set(db.filter_is_not_matching_ids(db.get_all_article_ids(language2), language1))
)  # está en language 1 y no en language 2

unique_article_desc_only_language2 = []

### Iterar sobre cada URL de unique_article_url_both_language1
for url in unique_articles_only_language2:
    # Llamar a la función db.get_article_word_count con cada URL
    word_count = db.get_article_word_count(language2, url)

    # Agregar el resultado como un diccionario con 'url' y 'word_count'
    unique_article_desc_only_language2.append(
        {
            "url": url,
            "available language": language2,
            "word_count_to_translate": word_count,
        }
    )


# VISUALIZAR DATOS
def plot_quantity_of_subcategories_and_articles():
    ### Datos para el gráfico
    labels_chart1 = ["Categories", "Articles"]
    categories_values_chart1 = [total_categories_language1, total_categories_language2]
    articles_values_chart1 = [total_articles_language1, total_articles_language2]

    ### Configuración del gráfico
    x = np.arange(
        len(labels_chart1)
    )  # Posición de las etiquetas (Categories y Articles)
    width = 0.35  # Ancho de las barras

    ### Crear el gráfico
    _, ax = plt.subplots(figsize=(8, 5))
    bars1 = ax.bar(
        x - width / 2,
        [categories_values_chart1[0], articles_values_chart1[0]],
        width,
        label=label_language1,
        color=color_language1,
    )
    bars2 = ax.bar(
        x + width / 2,
        [categories_values_chart1[1], articles_values_chart1[1]],
        width,
        label=label_language2,
        color=color_language2,
    )

    ### Añadir texto a las barras
    def add_labels(bars):
        for bar in bars:
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # Posición x
                yval + 1,  # Posición y ligeramente por encima
                f"{int(yval)}",  # Texto con el valor
                ha="center",
                va="bottom",
                color="black",
                fontsize=10,
            )

    add_labels(bars1)
    add_labels(bars2)

    ### Configuración de las etiquetas y título
    ax.set_ylabel("Quantity")
    ax.set_title("Quantity of categories and articles", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels_chart1)
    ax.legend()

    ### Ajustar el diseño
    plt.tight_layout()
    plt.show()


def plot_distribution_of_categories():
    ### Datos para el gráfico
    labels_chart2 = [label_language1, label_language2]
    categories_values_chart2 = [total_categories_language1, total_categories_language2]

    ### Calcular porcentajes
    total_chart2 = sum(categories_values_chart2)
    percentages_chart2 = [
        value / total_chart2 * 100 for value in categories_values_chart2
    ]

    ### Crear etiquetas que incluyan valores absolutos y relativos
    labels = [
        f"{cat}\n{val} ({perc:.1f}%)"
        for cat, val, perc in zip(
            labels_chart2, categories_values_chart2, percentages_chart2
        )
    ]

    ### Crear el gráfico de queso
    _, ax = plt.subplots(figsize=(6, 6))  # Tamaño del gráfico
    ax.pie(
        categories_values_chart2,
        labels=labels,  # Usar las etiquetas formateadas
        autopct=None,  # No usar el formato automático
        startangle=90,  # Rotar para que el inicio sea en la parte superior
        colors=[color_language1, color_language2],  # Colores personalizados
    )

    ### Estilo de texto
    ax.set_title(
        f"Distribution of categories in {label_language1} and {label_language2}",
        fontsize=14,
    )

    ### Mostrar el gráfico
    plt.tight_layout()
    plt.show()


def plot_distribution_of_articles():
    ### Datos para el gráfico
    labels_chart3 = [label_language1, label_language2]
    articles_values_chart3 = [total_articles_language1, total_articles_language2]

    ### Calcular porcentajes
    total_chart3 = sum(articles_values_chart3)
    percentages_chart3 = [
        value / total_chart3 * 100 for value in articles_values_chart3
    ]

    ### Crear etiquetas que incluyan valores absolutos y relativos
    labels = [
        f"{cat}\n{val} ({perc:.1f}%)"
        for cat, val, perc in zip(
            labels_chart3, articles_values_chart3, percentages_chart3
        )
    ]

    ### Crear el gráfico de queso
    fig, ax = plt.subplots(figsize=(6, 6))  # Tamaño del gráfico
    ax.pie(
        articles_values_chart3,
        labels=labels,  # Usar las etiquetas formateadas
        autopct=None,  # No usar el formato automático
        startangle=90,  # Rotar para que el inicio sea en la parte superior
        colors=[color_language1, color_language2],  # Colores personalizados
    )

    ### Estilo de texto
    ax.set_title(
        f"Distribution of articles in {label_language1} and {label_language2}",
        fontsize=14,
    )

    ### Mostrar el gráfico
    plt.tight_layout()
    plt.show()


def plot_distribution_of_sections():
    ### Datos para el gráfico
    labels_chart4 = [label_language1, label_language2]
    sections_values_chart4 = [total_sections_language1, total_sections_language2]

    ### Calcular porcentajes
    total_chart4 = sum(sections_values_chart4)
    percentages_chart4 = [
        value / total_chart4 * 100 for value in sections_values_chart4
    ]

    ### Crear etiquetas que incluyan valores absolutos y relativos
    labels = [
        f"{cat}\n{val} ({perc:.1f}%)"
        for cat, val, perc in zip(
            labels_chart4, sections_values_chart4, percentages_chart4
        )
    ]

    ### Crear el gráfico de queso
    fig, ax = plt.subplots(figsize=(6, 6))  # Tamaño del gráfico
    ax.pie(
        sections_values_chart4,
        labels=labels,  # Usar las etiquetas formateadas
        autopct=None,  # No usar el formato automático
        startangle=90,  # Rotar para que el inicio sea en la parte superior
        colors=[color_language1, color_language2],  # Colores personalizados
    )

    ### Estilo de texto
    ax.set_title(
        f"Distribution of sections in {label_language1} and {label_language2}",
        fontsize=14,
    )

    ### Mostrar el gráfico
    plt.tight_layout()
    plt.show()


def plot_distribution_of_duplicated_articles():
    labels_chart5 = ["Duplicated", "Unique"]
    values_chart5_language1 = [
        total_articles_language1 - total_unique_articles_language1,
        total_unique_articles_language1,
    ]
    values_chart5_language2 = [
        total_articles_language2 - total_unique_articles_language2,
        total_unique_articles_language2,
    ]

    ### Calcular porcentajes
    total_values_chart5_language1 = sum(values_chart5_language1)
    percentages_values_chart5_language1 = [
        values1 / total_values_chart5_language1 * 100
        for values1 in values_chart5_language1
    ]

    total_values_chart5_language2 = sum(values_chart5_language2)
    percentages_values_chart5_language2 = [
        values2 / total_values_chart5_language2 * 100
        for values2 in values_chart5_language2
    ]

    ### Crear etiquetas que incluyan valores absolutos y relativos
    labels1_chart5 = [
        f"{cat}\n{val} ({perc:.1f}%)"
        for cat, val, perc in zip(
            labels_chart5, values_chart5_language1, percentages_values_chart5_language1
        )
    ]

    labels2_chart5 = [
        f"{cat}\n{val} ({perc:.1f}%)"
        for cat, val, perc in zip(
            labels_chart5, values_chart5_language2, percentages_values_chart5_language2
        )
    ]

    ### Crear una figura con dos subgráficos
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 1 fila, 2 columnas

    ### Gráfico 1
    axs[0].pie(
        values_chart5_language1,
        labels=labels1_chart5,
        autopct=None,
        startangle=90,
        colors=[color_language1_transparency, color_language1],
    )
    axs[0].set_title(f"Duplicated articles distribution ({label_language1})")

    ### Gráfico 2
    axs[1].pie(
        values_chart5_language2,
        labels=labels2_chart5,
        autopct=None,
        startangle=90,
        colors=[color_language2_transparency, color_language2],
    )
    axs[1].set_title(f"Duplicated articles distribution ({label_language2})")

    ### Ajustar diseño
    plt.tight_layout()
    plt.show()


def plot_number_of_categories():
    labels_chart6 = [
        f"Only {label_language1}",
        f"Only {label_language2}",
        "Both languages",
    ]
    values_chart6 = [
        total_categories_only_language1,
        total_categories_only_language2,
        total_categories_both,
    ]

    total_values_chart6 = sum(values_chart6)

    ### Crear el gráfico
    fig, ax = plt.subplots(figsize=(8, 6))

    ### Colores personalizados para cada barra
    colors = [color_language1, color_language2, color_both]

    ### Dibujar las barras
    bars = ax.bar(labels_chart6, values_chart6, color=colors)

    ### Añadir etiquetas encima de las barras
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_values_chart6) * 100  # Calcular el porcentaje
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height} ({percentage:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ### Configuración del gráfico
    ax.set_title(
        f"Number of categories in {label_language1}, {label_language2} and both",
        fontsize=14,
    )
    ax.set_ylabel("Number of categories", fontsize=12)
    ax.set_ylim(0, max(values_chart6) + 10)  # Ajustar el rango del eje Y

    ### Mostrar el gráfico
    plt.tight_layout()
    plt.show()


def plot_number_of_unique_articles():
    labels_chart7 = [
        f"Only {label_language1}",
        f"Only {label_language2}",
        "Both languages",
    ]
    values_chart7 = [
        total_unique_articles_only_language1,
        total_unique_articles_only_language2,
        total_unique_articles_both,
    ]

    total_values_chart7 = sum(values_chart7)

    ### Crear el gráfico
    fig, ax = plt.subplots(figsize=(8, 6))

    ### Colores personalizados para cada barra
    colors = [color_language1, color_language2, color_both]

    ### Dibujar las barras
    bars = ax.bar(labels_chart7, values_chart7, color=colors)

    ### Añadir etiquetas encima de las barras
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_values_chart7) * 100  # Calcular el porcentaje
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height} ({percentage:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ### Configuración del gráfico
    ax.set_title(
        f"Number of unique articles in {label_language1}, {label_language2} and both",
        fontsize=14,
    )
    ax.set_ylabel("Number of unique articles", fontsize=12)
    ax.set_ylim(0, max(values_chart7) * 1.1)  # Ajustar el rango del eje Y

    ### Mostrar el gráfico
    plt.tight_layout()
    plt.show()


def plot_articles_distribution_per_category():
    ### Outlier category
    # outlier_chart8_language1 = df_category_articles_language1[
    #     df_category_articles_language1["articles_count"]
    #     > df_category_articles_language1["articles_count"].quantile(0.75)
    # ].sort_values(by="articles_count", ascending=False)
    # outlier_chart8_language2 = df_category_articles_language2[
    #     df_category_articles_language2["articles_count"]
    #     > df_category_articles_language2["articles_count"].quantile(0.75)
    # ].sort_values(by="articles_count", ascending=False)

    ### Calcular la media y mediana
    mean_chart8_language1 = df_category_articles_language1[
        "articles_count"
    ].mean()  # Média
    median_chart8_language1 = df_category_articles_language1[
        "articles_count"
    ].median()  # Mediana

    mean_chart8_language2 = df_category_articles_language2[
        "articles_count"
    ].mean()  # Média
    median_chart8_language2 = df_category_articles_language2[
        "articles_count"
    ].median()  # Mediana

    ### Crear el boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [
            df_category_articles_language1["articles_count"],
            df_category_articles_language2["articles_count"],
        ],
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor=color_language1_transparency, color="black"),
        medianprops=dict(color="red"),
        meanprops=dict(marker="o", markerfacecolor=color_language1, markersize=8),
        showmeans=True,
    )

    ### Añadir los valores de media y mediana en el gráfico
    mean_values = [mean_chart8_language1, mean_chart8_language2]
    median_values = [median_chart8_language1, median_chart8_language2]

    for i, (mean, median) in enumerate(zip(mean_values, median_values)):
        plt.annotate(
            f"Mean={mean:.1f}\nMedian={median:.1f}",
            xy=(i + 1, mean),
            xytext=(i + 1.2, mean + 1),
            arrowprops=dict(facecolor="gray", arrowstyle="->"),
            fontsize=10,
            color="black",
        )

    ### Configuración del gráfico
    plt.ylabel("Number of Articles per Category")
    plt.title(
        f"Boxplot of articles distribution per category in {label_language1} and {label_language2}"
    )
    plt.xticks([1, 2], [f"{label_language1}", f"{label_language2}"], fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    ### Mostrar el gráfico
    plt.show()


def plot_sections_distribution_per_article():
    ### Outlier category
    # outlier_chart9_language1 = df_unique_articles_language1[
    #     df_unique_articles_language1["sections_count"]
    #     > df_unique_articles_language1["sections_count"].quantile(0.75)
    # ].sort_values(by="sections_count", ascending=False)
    # outlier_chart9_language2 = df_unique_articles_language2[
    #     df_unique_articles_language2["sections_count"]
    #     > df_unique_articles_language2["sections_count"].quantile(0.75)
    # ].sort_values(by="sections_count", ascending=False)

    ### Calcular la media y mediana
    mean_chart9_language1 = df_unique_articles_language1[
        "sections_count"
    ].mean()  # Média
    median_chart9_language1 = df_unique_articles_language1[
        "sections_count"
    ].median()  # Mediana

    mean_chart9_language2 = df_unique_articles_language2[
        "sections_count"
    ].mean()  # Média
    median_chart9_language2 = df_unique_articles_language2[
        "sections_count"
    ].median()  # Mediana

    ### Crear el boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [
            df_unique_articles_language1["sections_count"],
            df_unique_articles_language2["sections_count"],
        ],
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor=color_language1_transparency, color="black"),
        medianprops=dict(color="red"),
        meanprops=dict(marker="o", markerfacecolor=color_language1, markersize=8),
        showmeans=True,
    )

    ### Añadir los valores de media y mediana en el gráfico
    mean_values = [mean_chart9_language1, mean_chart9_language2]
    median_values = [median_chart9_language1, median_chart9_language2]

    for i, (mean, median) in enumerate(zip(mean_values, median_values)):
        plt.annotate(
            f"Mean={mean:.1f}\nMedian={median:.1f}",
            xy=(i + 1, mean),
            xytext=(i + 1.2, mean + 1),
            arrowprops=dict(facecolor="gray", arrowstyle="->"),
            fontsize=10,
            color="black",
        )

    ### Configuración del gráfico
    plt.ylabel("Number of sections per article")
    plt.title(
        f"Boxplot of sections distribution per article in {label_language1} and {label_language2}"
    )
    plt.xticks([1, 2], [f"{label_language1}", f"{label_language2}"], fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    ### Mostrar el gráfico
    plt.show()


def plot_word_count_distribution_per_article():
    ### Outlier category
    # outlier_chart10_language1 = df_unique_articles_language1[
    #     df_unique_articles_language1["total_word_count"]
    #     > df_unique_articles_language1["total_word_count"].quantile(0.75)
    # ].sort_values(by="total_word_count", ascending=False)
    # outlier_chart10_language2 = df_unique_articles_language2[
    #     df_unique_articles_language2["total_word_count"]
    #     > df_unique_articles_language2["total_word_count"].quantile(0.75)
    # ].sort_values(by="total_word_count", ascending=False)

    ### Calcular la media y mediana
    mean_chart10_language1 = df_unique_articles_language1[
        "total_word_count"
    ].mean()  # Média
    median_chart10_language1 = df_unique_articles_language1[
        "total_word_count"
    ].median()  # Mediana

    mean_chart10_language2 = df_unique_articles_language2[
        "total_word_count"
    ].mean()  # Média
    median_chart10_language2 = df_unique_articles_language2[
        "total_word_count"
    ].median()  # Mediana

    ### Crear el boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [
            df_unique_articles_language1["total_word_count"],
            df_unique_articles_language2["total_word_count"],
        ],
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor=color_language1_transparency, color="black"),
        medianprops=dict(color="red"),
        meanprops=dict(marker="o", markerfacecolor=color_language1, markersize=8),
        showmeans=True,
    )

    ### Añadir los valores de media y mediana en el gráfico
    mean_values = [mean_chart10_language1, mean_chart10_language2]
    median_values = [median_chart10_language1, median_chart10_language2]

    for i, (mean, median) in enumerate(zip(mean_values, median_values)):
        plt.annotate(
            f"Mean={mean:.1f}\nMedian={median:.1f}",
            xy=(i + 1, mean),
            xytext=(i + 1.2, mean + 1),
            arrowprops=dict(facecolor="gray", arrowstyle="->"),
            fontsize=10,
            color="black",
        )

    ### Configuración del gráfico
    plt.ylabel("Number of word count per article")
    plt.title(
        f"Boxplot of word count distribution per article in {label_language1} and {label_language2}"
    )
    plt.xticks([1, 2], [f"{label_language1}", f"{label_language2}"], fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    ### Mostrar el gráfico
    plt.show()


def plot_word_count_distribution_and_quick_win():
    word_counts_chart11_language1 = [
        item["word_count"] for item in unique_article_desc_both_language1
    ]
    word_counts_chart11_language2 = [
        item["word_count"] for item in unique_article_desc_both_language2
    ]

    mean_chart11_language1 = sum(word_counts_chart11_language1) / len(
        word_counts_chart11_language1
    )  # Média
    median_chart11_language1 = statistics.median(
        word_counts_chart11_language1
    )  # Mediana

    mean_chart11_language2 = sum(word_counts_chart11_language2) / len(
        word_counts_chart11_language2
    )  # Média
    median_chart11_language2 = statistics.median(
        word_counts_chart11_language2
    )  # Mediana

    ### Crear el boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [word_counts_chart11_language1, word_counts_chart11_language2],
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor=color_language1_transparency, color="black"),
        medianprops=dict(color="red"),
        meanprops=dict(marker="o", markerfacecolor=color_language1, markersize=8),
        showmeans=True,
    )

    ### Añadir los valores de media y mediana en el gráfico
    mean_values = [mean_chart11_language1, mean_chart11_language2]
    median_values = [median_chart11_language1, median_chart11_language2]

    for i, (mean, median) in enumerate(zip(mean_values, median_values)):
        plt.annotate(
            f"Mean={mean:.1f}\nMedian={median:.1f}",
            xy=(i + 1, mean),
            xytext=(i + 1.2, mean + 1),
            arrowprops=dict(facecolor="gray", arrowstyle="->"),
            fontsize=10,
            color="black",
        )

    ### Configuração do gráfico
    plt.ylabel("Number of word count per article translated")
    plt.title(
        f"Boxplot of word count distribution per article translated in {label_language1} and {label_language2}"
    )
    plt.xticks([1, 2], [f"{label_language1}", f"{label_language2}"], fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    ### Mostrar o gráfico
    plt.show()

    ### Quick Win Adding the estimated_effort
    rate_translation = (
        median_chart11_language2 - median_chart11_language1
    ) / median_chart11_language1
    for item in unique_article_desc_only_language1:
        item["estimated_word_count_translated"] = int(
            item["word_count_to_translate"] * rate_translation
            + item["word_count_to_translate"]
        )

    for item in unique_article_desc_only_language2:
        item["estimated_word_count_translated"] = int(
            item["word_count_to_translate"] / (rate_translation + 1)
        )

    quick_win = unique_article_desc_only_language1 + unique_article_desc_only_language2
    sorted_quick_win = sorted(
        quick_win, key=lambda x: x["estimated_word_count_translated"]
    )

    df_sorted_quick_win = pd.DataFrame(sorted_quick_win)

    df_sorted_quick_win.to_csv("quick_win.csv", index=False)
