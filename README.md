# EntrezPlantSearch
## Search PubMed using keywords of 35000+ plant genera
## It is a jupyter notebook for Google Colab.
## In Colab, you have to Mount your Google Drive, and at the top level, create a folder called plant_search_text_files
## In that folder, place the three list text files in this Github, gene1.txt, phytochem3.txt, and genus_names2.txt
## Also create a subfolder called saved_searches. The script will save the abstracts, title, etc of the search results there, in chronological order with duplicates removed. Additionally, folders labeled titles_only and query_files must be created at the same level. If creating the folders is confusing, download the plant_search_text_files folder from this github to your desktop and place it directly in your Google Drive top level. It should be formatted correctly for the searches to work.


## Sample Search:
## email@domain.com
## 3 (Note: This will search the plant genera and also will search other articles with phytochemical names, phytochemical names are Pubmed Title searches only)
## creb neurite
## output file should save to your google drive saved_searches folder, which is a subfolder of plant_search_text_files

## Known bug: If search term is vague, like 'diabetes' it will pull up the max results (9999) for some of the search packets and crash
## One workaround is to first search for genes or signalling pathways involved in a particular diabetic complication and then
## feed those genes/pathways into the plant_search

## This is meant to eventually be a tool for researchers. It is not meant to diagnose or treat disease. Please consult your doctor for those things. Thanks!
