# experimental 



from Bio import Entrez
import datetime
import os
import time
import sys
import re
from http.client import IncompleteRead

email = input('What is your email address?')
# Email address is required by NCBI
Entrez.email = email

# Choose which txt files to search over
choice = input('Do you want to search over all plant genera (enter 1) \n \
                | all phytochemicals (enter 2) | or both (enter 3) | \n \
                If you do not want to search over plants or phytochemicals, \n \
                try searching over human genes first (not as good as MESH term search) (enter 4) : ')
choice = int(choice)

# Load correct text file
if choice == 1:
    with open('plant_search_text_files/genus_names2.txt', 'r') as f:
        genus_names = f.read().split('@')
if choice == 2:
    with open('plant_search_text_files/phytochem3.txt', 'r') as f:
        genus_names = f.read().split('\t')
       
if choice == 3:
    with open('plant_search_text_files/genus_names2.txt', 'r') as f:
        genus_names = f.read().split('@')
    with open('plant_search_text_files/phytochem3.txt', 'r') as f:
        phyt_names = f.read().split('\t')

if choice == 4:
    with open('plant_search_text_files/gene1.txt', 'r') as f:
        genus_names = f.read().split('@')


# User-defined search term
user_query = input('Enter additional non-plant search terms: ')

# Set counter in case choice == 3. This allows first 38 searches to include "plant" as a key word
gen_phyt_counter = 1

# Create directory for input files if it doesn't exist
if not os.path.exists('input_files'):
    os.makedirs('input_files')

# Split the genus names into groups of 1000 or less, to stay under the PubMed search limit
genus_groups = [genus_names[i:i+1000] for i in range(0, len(genus_names), 1000)]

if choice == 3:
    genus_groups = [genus_names[i:i+1000] for i in range(0, len(genus_names), 1000)]
    phyt_groups = [phyt_names[i:i+1000] for i in range(0, len(phyt_names), 1000)]

    genus_groups = genus_groups + phyt_groups
   



# List to store abstracts and their associated date information
abstracts_with_info = []
article_title = []

# Set to keep track of seen Pubmed IDs
seen_pmids = set()

for i, genus_group in enumerate(genus_groups):
    # Construct query string
    if choice == 1: 
        query_terms = '(' + ' OR '.join(genus_group) + ') + AND "plant" AND ' + user_query
    if choice == 3: 
        if gen_phyt_counter <= 38:
            query_terms = '(' + ' OR '.join(genus_group) + ') + AND "plant" AND ' + user_query
        if gen_phyt_counter > 38:
            query_terms = '(' + ' OR '.join(genus_group) + ') + AND ' + user_query 
    if choice == 2: 
        query_terms = '(' + ' OR '.join(genus_group) + ') + AND ' + user_query 
    if choice == 4: 
        query_terms = '(' + ' OR '.join(genus_group) + ') + AND "gene" AND ' + user_query
    
    gen_phyt_counter += 1
    
    # # # testing line, remove
    # if gen_phyt_counter == 38:
    #     print(query_terms)
    # if gen_phyt_counter == 39:
    #     print(query_terms)
    # if gen_phyt_counter == 40:
    #     print(query_terms)


    # Print search query
    print(f'Searching group {i+1}/{len(genus_groups)}')

    
    # Perform search
    herror = 0
    error_number = 0
    while herror == 0:
      try:
          handle = Entrez.esearch(db='pubmed', term=query_terms, retmax=100000)
          record = Entrez.read(handle)
          handle.close()
          herror = 1
      except Exception as err:
          error_number += 1
          if error_number == 5:
            raise err
          print(f"Error: {str(err)}. Retrying in 5 seconds...")
          time.sleep(5)
          herror = 0
        

    # Fetch abstracts for all search results
    id_list = record['IdList']
    
    query_numb = 1
    exc = 1
    
    if id_list:
      while exc == 1:
        try:
          print(f'Fetching {len(id_list)} abstracts...')
          handle = Entrez.efetch(db='pubmed', id=id_list, retmode='xml')
          records = Entrez.read(handle)
          handle.close()
          exc = 0

        # commented out lines below still allow for http error
        # except IncompleteRead: 
        #   query_numb += 1
        #   if query_numb == 5:
        #     raise Exception('Failed to fetch abstracts after 5 attempts.')
        #   print(f'Error fetching abstracts, retrying ({query_numb}/5)...')
        #   time.sleep(5) # Wait 5 seconds before retrying
        #   exc = 1
        
        except Exception as err:
          query_numb += 1
          if query_numb == 5:
            raise err
          print(f"Error: {str(err)}. Retrying in 5 seconds...")
          time.sleep(5)
          exc = 1
          
          
          

    # def fetch_abstracts(id_list):
    #   for i in range(5): # Try up to 5 times
    #       try:
    #           print(f'Fetching {len(id_list)} abstracts...')
    #           handle = Entrez.efetch(db='pubmed', id=id_list, retmode='xml')
    #           records = Entrez.read(handle)
    #           handle.close()
    #           return records
    #       except IncompleteRead:
    #           print(f'Error fetching abstracts, retrying ({i+1}/5)...')
    #           time.sleep(5) # Wait 5 seconds before retrying
    #           raise Exception('Failed to fetch abstracts after 5 attempts.')

    # fetch_abstracts(id_list)

        # Extract abstracts and date information for each record
        for record in records['PubmedArticle']:
            try:
                abstract = record['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            except (KeyError, IndexError):
                abstract = 'Not available'
            #EntrezDate
            try:
                pub_date = record['MedlineCitation']['DateRevised']
                pub_date_str = f"{pub_date.get('Year', 'Not available')}-{pub_date.get('Month', 'Not available')}-{pub_date.get('Day', 'Not available')}"
            except KeyError:
                pub_date_str = 'Not available'
            #PubDate
            try:
                pub_date1 = record['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
                pub_date_str1 = f"{pub_date1.get('Year', 'Not available')} {pub_date1.get('Month', 'Not available')}"
            except KeyError:
                pub_date_str1 = 'Not available'
            try:
                journal = record['MedlineCitation']['Article']['Journal']['Title']
            except KeyError:
                journal = 'Not available'
            try:
                authors = record['MedlineCitation']['Article']['AuthorList']
                author_names = [f"{author.get('LastName', 'Not available')}, {author.get('ForeName', '')}" for author in authors]
                authors_str = ', '.join(author_names)
            except KeyError:
                authors_str = 'Not available'
            try:
                pmid = record['MedlineCitation']['PMID']
            except KeyError:
                pmid = 'Not available'
            
            #Add new PubMed ID to set
            skipme=1
            if pmid not in seen_pmids:
                seen_pmids.add(pmid)
                skipme=0

            

            Date1 = pub_date_str1[0:4]
            Date0 = pub_date_str[0:4]

            

            if Date1 != Date0:
                if "Not" in Date1:
                    out_string = f"{pub_date_str}  -DateCatalogued\n{pub_date_str1} -DatePublished\nAuthors: {authors_str}\nJournal: {journal}\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}\nPMID: {pmid}\nAbstract: {abstract}\n\n"
                    out_string2 = f"{pub_date_str}  -DateCatalogued\n{pub_date_str1} -DatePublished\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}"
                else:
                    if Date1 < Date0:
                        out_string = f"{pub_date_str1} -DatePublished\n{pub_date_str}  -DateCatalogued\nAuthors: {authors_str}\nJournal: {journal}\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}\nPMID: {pmid}\nAbstract: {abstract}\n\n"    
                        out_string2 = f"{pub_date_str1} -DatePublished\n{pub_date_str}  -DateCatalogued\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}"
                    if Date1 > Date0:
                        out_string = f"{pub_date_str}  -DateCatalogued\n{pub_date_str1} -DatePublished\nAuthors: {authors_str}\nJournal: {journal}\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}\nPMID: {pmid}\nAbstract: {abstract}\n\n"
                        out_string2 = f"{pub_date_str}  -DateCatalogued\n{pub_date_str1} -DatePublished\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}"
            else:
                out_string = f"{pub_date_str}  -DateCatalogued\n{pub_date_str1} -DatePublished\nAuthors: {authors_str}\nJournal: {journal}\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}\nPMID: {pmid}\nAbstract: {abstract}\n\n"
                out_string2 = f"{pub_date_str}  -DateCatalogued\n{pub_date_str1} -DatePublished\nTitle: {record['MedlineCitation']['Article']['ArticleTitle']}"
            if skipme==0:
                abstracts_with_info.append(out_string)
                article_title.append(out_string2)


        time.sleep(1) # Add a delay of 1 second
    else:
        print('No results found for this group.')

# Sort abstracts by date
abstracts_with_info.sort(reverse=True)
article_title.sort(reverse=True)

# Create subfolder if it doesn't exist
#if not os.path.exists("phyto_results"):
    #os.mkdir("phyto_results")

# Get current time to name output file
user_query = re.sub(r'[^a-zA-Z0-9]+', '_', user_query)
now = datetime.datetime.now()

#output_file_name = f"phyto_results/{user_query}_{now.strftime('%Y%m%d_%H%M%S')}.txt"

output_file_name = f"plant_search_text_files/saved_searches/{choice}_{user_query}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
title_file_name = f"plant_search_text_files/titles_only/Titles_only_{choice}_{user_query}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
pubmed_query = f"plant_search_text_files/query_files/query_file_{choice}_{user_query}_{now.strftime('%Y%m%d_%H%M%S')}.txt"

# Merge all abstracts into one file, sorted by date
with open(output_file_name, 'w', encoding='utf-8') as out_file, \
     open(pubmed_query, 'w', encoding='utf-8') as query_file, \
     open(title_file_name, 'w', encoding='utf-8') as title_file:
    query_file.write(query_terms + '\n')
    count_papers = 1
    total_length = len(abstracts_with_info)
    out_file.write(str(total_length) + ' papers are in this text file \n' )
    for abstract in abstracts_with_info:
        out_file.write('Paper #' + str(count_papers) + ' - ')
        count_papers += 1
        out_file.write(abstract)
    count_titles = 1
    title_file.write(str(total_length) + ' papers are in this text file \n' )
    for title in article_title:
        title_file.write('\n\nPaper #' + str(count_titles) + ' - ')
        count_titles += 1
        title_file.write(title)

        

# Empty the input_files folder
for file_name in os.listdir('input_files'):
    file_path = os.path.join('input_files', file_name)
    try:
        os.remove(file_path)
    except:
        print(f'Error deleting {file_path}')

# print search complete message
print('\n\nSearch complete. \n\n Results (abstracts, journal, PMID, authors, etc.) are in the subfolder called saved_searches in the plant_text_search_files folder \n\n To only browse titles, view the file in the titles_only folder. \n\n To see a small sample of your search query terms, view the file in the query_files folder. \n\n Have a nice day!')

# Type exit to close the program
input('Press enter to exit')






