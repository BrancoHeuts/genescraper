# Gene Card Scroller
A Flask application that lets you scroll through GeneCard's gene summaries, granted you provide a list of genes.


## Installation
Install genescraper with pip
```bash
  pip install git+https://github.com/branco-heuts/genescraper
```
## Usage
Make sure you provide a comma separated file (.csv), without headers or row-names. You can find an example file [here](https://github.com/branco-heuts/genescraper/blob/master/gene_list.csv)

Run the command in the terminal:
> $ python genescraper.py -c gene_list.csv


And click: http://127.0.0.1:5000 or http://10.252.0.13:5000
<br></br>
Warning: a large list of genes is not recommended, the webscraping can be slow.

When your done, close the server using CTRL+C.
