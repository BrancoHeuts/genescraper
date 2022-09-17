import argparse
import pandas as pd
from flask import Flask, render_template
from tqdm import tqdm
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt


# ----- Argparse -----
parser = argparse.ArgumentParser()
parser.add_argument(
        "-c",
        "--csv",
        help="Gene list as input file. Comma separated file (.csv) without headers.")
args = parser.parse_args()

if args.csv is None or not args.csv.endswith('.csv'):
    raise ValueError(
        "Please use the '-c' or '--csv' flag."
        "Needs a Comma Separated File (.csv) as input. "
    )

# Import csv
gene_list = pd.read_csv(args.csv, header=None).iloc[0].unique()


app = Flask(__name__)


# ----- Webscrape -----
url = "https://www.genecards.org/cgi-bin/carddisp.pl?gene="
data = []
for gene in tqdm(gene_list):

    try:
        req = Request(
            url=url + gene,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read()

        # Load html code from a url
        soup = bs(webpage, "html.parser")

        # ----- Aliases -----
        # Main name
        main_name = soup.body.find("span", class_='aliasMainName').get_text()

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
                uniprot_summary = uniprot_summary.split("\r\n")[1]

        # ----- Molecular function -----
        function = soup.body.find_all("div", class_="gc-subsection-inner-wrap")

        for i in function:
            stripped_string = i.get_text()
            if "Function:" in stripped_string:
                function_string = i.find_next("li").get_text()
                function_list = function_string.split(".")

                # Remove redundant strings and list items
                function_list[0] = function_list[0].replace("\r\n", "")
                function_list = function_list[:-1]

        data_item = {
            'gene_name': main_name,
            'alias_description': description_list_stripped,
            'alias_alternate_name': alternate_name_list_stripped,
            'entrez_summary': entrez_summary,
            'uniport_summary': uniprot_summary,
            'molecular_function': function_list
        }
        data.append(data_item)

    except HTTPError as err:  # If gene does not exist
        if err.code == 404:
            print(f"{gene} not found.")
        else:
            raise


@app.route('/')
def get_gene_cards():
    return render_template("index.html", data=data, year=dt.today().year)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
