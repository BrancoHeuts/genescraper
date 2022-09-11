from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

url = "https://www.genecards.org/cgi-bin/carddisp.pl?gene="

gene_list = [  # TODO: Import csv
    "HMX3",
    "BRE",
    "SPI1"
]


def remove_redundant_strings(li):
    """
    Remove redundant "\r\n" characters at the start of each first list item. Also, removes last list item.
    :param li: List of scraped items (stripped)
    :return: List
    """
    li[0] = li[0].replace("\r\n", "")
    li = li[:-1]
    return li


data = []
for gene in gene_list:

    req = Request(
        url=url + gene,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()

    # Load html code from a url
    soup = bs(webpage, "html.parser")

    # ----- Aliases -----
    # Description
    descriptions = soup.body.find_all(itemprop='description')
    description_list_stripped = [item.get_text() for item in descriptions]

    # Alternate names
    alternate_names = soup.body.find_all(itemprop='alternateName')
    alternate_name_list_stripped = [item.get_text() for item in alternate_names]

    # ----- Summaries -----
    summaries = soup.body.find_all("div", class_="gc-subsection-header")

    for i in summaries:
        stripped_string = i.get_text()

        # Entrez Gene Summary
        if f"Entrez Gene Summary for {gene} Gene" in stripped_string:
            entrez_summary = i.find_next("p").get_text()

        # UniProtKB/Swiss-Prot Summary
        if f"UniProtKB/Swiss-Prot Summary for {gene} Gene" in stripped_string:
            uniprot_summary = i.find_next("p").get_text()

    # ----- Molecular function -----
    function = soup.body.find_all("div", class_="gc-subsection-inner-wrap")

    for i in function:
        stripped_string = i.get_text()
        if "Function:" in stripped_string:
            function_string = i.find_next("li").get_text()
            function_list = function_string.split(".")
            function_list = remove_redundant_strings(function_list)

    data_item = {
        'gene_name': gene,  # TODO: Get GeneCard Symbol instead
        'alias_description': description_list_stripped,
        'alias_alternate_name': alternate_name_list_stripped,
        'entrez_summary': entrez_summary,
        'uniport_summary': uniprot_summary,
        'molecular_function': function_list
    }
    data.append(data_item)

print(data)
