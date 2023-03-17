# EntrezPlantSearch
## Search PubMed using keywords of 35000+ plant genera
## the plant_search.ipynb file in this github is a jupyter notebook for Google Colab.
## In Colab, you have to Mount your Google Drive


## Create the necessary folders in your Google Drive, according to the Github file structure on this page, as follows:

On the top level of your Google Drive, you should have 1 folder:

plant_search_text_files 

In that folder, you should have 3 files:

genus_names2.txt

gene1.txt

phytochem3.txt


and 3 folders:

saved_searches

titles_only

query_files

Now run the plant_search.ipynb jupyter notebook in this Github in your Google Colab.

If the folder structure is confusing. Just download/copy the folder structure from this Github into the top level of your Google Drive. The script should then work.

## The jupyter notebook contains 4 types of searches:

### choice 1: plant genera - will search your terms against a list of over 35,000 plant genera.
This choice is the only one that functions very well as of now.

### choice 2: phytochemicals - will search your terms using a titles only search of a list of  25,000+ phytochemicals.

### choice 3: Both - Does search choice 1 and 2 in a single search. Very slow.

### If you are not ready to do a plant or phytochemical search, you can do a human protein coding gene search for fun using choice 4. This is not a very efficient search, as using MESH  terms are probably for genes.

## This jupyter notebook was mostly created using the GPT 3 version of ChatGPT. Feel free to add and improve the Github project. Thanks!


## Sample Search:
## email@domain.com
## 3 (Note: This will search the plant genera and also will search other articles with phytochemical names, phytochemical names are Pubmed Title searches only)
## creb neurite
## output file with abstracts/title/journal/etc should save to your google drive saved_searches folder, which is a subfolder of plant_search_text_files
   
   A file with only the titles (for browsing) will be saved to the titles_only folder. 
   
   A partial sample of how your query was sent will be saved to the query_files folder.

## Known bug: If search term is vague, like 'diabetes' it will pull up the max results (9999) for some of the search packets and crash
## One workaround is to first search for genes or signalling pathways involved in a particular diabetic complication and then
## feed those genes/pathways into the plant_search

## This is meant to eventually be a tool for researchers. It is not meant to diagnose or treat disease. Please consult your doctor for those things. Thanks!
