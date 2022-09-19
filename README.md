# Gene Card Scroller
A Flask application that lets you scroll through GeneCard's gene summaries, granted you provide a list of genes.
<hr>

## Installation
Install genescraper with pip
```bash
  pip install git+https://github.com/branco-heuts/genescraper
```
## Usage
Make sure you provide a comma separated file (.csv), without headers or row-names. You can find an example file in this repository.

Run the command in the terminal:
> $ python genescraper.py -c gene_list.csv
> 
<br></br>
Warning: a large list of genes is not recommended, the webscraping can be slow.
