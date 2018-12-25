'''
--> A project for scraping the questions link and their statements form a coding website
    using web scraping with beautiful soup
'''  

#importing important libraries
import requests
import xlrd
from xlsxwriter  import Workbook
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# Ur of the java section and python sections of the websites
url = 'http://codingbat.com/java'
url1 = 'https://codingbat.com/python'

# Creating the object of fake user_agent
ua = UserAgent()
header = {'user-agent':ua.chrome}

# server returns an object of the HTML page which is requested
page = requests.get(url,headers = header)

# parser to parse the HTML code
soup = BeautifulSoup(page.content,'lxml')

# Base url for the different sections
basic_url = "https://codingbat.com"
all_divs = soup.find_all('div',class_ = 'summ')

# finding  the links for java sections
java_section_links = [basic_url+div.a['href'] for div in all_divs]
print(java_section_links)

page = requests.get(url1,headers = header)
soup = BeautifulSoup(page.content,'lxml')

all_divs = soup.find_all('div',class_ = 'summ')


# finding the links for python sections
python_section_links = [basic_url+div.a['href'] for div in all_divs]
print(python_section_links)


# Extracting all java questions from different java sections
java_questions = []
for links in java_section_links:
    inner_page = requests.get(links,headers = header)
    inner_soup = BeautifulSoup(inner_page.content,'lxml')
    div =inner_soup.find('div',class_ = 'indent')
    j_q_links = [basic_url+td.a['href'] for td in div.table.find_all('td')]
    java_questions.append(j_q_links)


# Extracting all python questions from different python sections    
python_questions = []    
for links in python_section_links:
    inner_page = requests.get(links,headers = header)
    inner_soup = BeautifulSoup(inner_page.content,'lxml')
    div = inner_soup.find('div',class_='indent')
    p_q_links = [basic_url+td.a['href'] for td in div.table.find_all('td')]
    python_questions.append(p_q_links)
    
java_questions_statements = []
java_questions_test_cases = []

print(java_questions[0][0])


# Extracting the statements of all java questions
for i in range(len(java_questions)):
    for j in range(len(java_questions[i])):
        inner_page = requests.get(java_questions[i][j],headers = header)
        inner_soup = BeautifulSoup(inner_page.content,'lxml')
        div = inner_soup.find('div',class_='indent') 
        java_questions_statements.append(div.table.div.string)
        sibling_of_statement = div.table.div.next_siblings
        examples = [sibling for sibling in sibling_of_statement if sibling.string is not None ]
        java_questions_test_cases.append(examples)
        print(div.table.div.string)
        
python_questions_statements = []
python_questions_test_cases = []


# Extracting the statements of all python questions
for i in range(len(python_questions)):
    for j in range(len(python_questions[i])):
        inner_page = requests.get(python_questions[i][j],headers = header)
        inner_soup = BeautifulSoup(inner_page.content,'lxml')
        div = inner_soup.find('div',class_ = 'indent')
        python_questions_statements.append(div.table.div.string)
        siblings_of_statements = div.table.div.next_siblings
        examples = [sibling for sibling in siblings_of_statements if sibling is not None]
        python_questions_test_cases.append(examples)
        print(div.table.div.string)
        
        
# Creating a workbook or excel file with two worsheets
# One for java another for python
workbook = Workbook('Scraped_questions.xlsx')
worksheet_java = workbook.add_worksheet()
worksheet_python = workbook.add_worksheet()


# ------> FOR WORKSHEET 1  <---------
# heading for 1st oth column will section links
# Java Section links
worksheet_java.write(0,0,'section_links')


# heading the first row of columns from 1 to 17 with section no.
for i in range(len(java_questions)):
    worksheet_java.write(0,i+1,'section '+str(i+1))


# fill 0th column with java_section_links
for i in range(len(java_section_links)):
    worksheet_java.write(i+1,0,java_section_links[i])


# heading the first row of columns from 18 to 34 with section question statement
for i in range(len(java_questions)):
    worksheet_java.write(0,i+18,'section '+str(i+1)+' question statements')
    

# from 1 to 17 columns filled with different java sections's question links
for i in range(len(java_questions)):
    for j in range(len(java_questions[i])):
        worksheet_java.write(j+1,i+1,java_questions[i][j])
    

# from 18 to 34 columns filled with different java sections's question links
count = 0
for i in range(len(java_questions)):
    for j in range(len(java_questions[i])):
        worksheet_java.write(j+1,18+i,java_questions_statements[count])
        count += 1
        
        
# ----------> FOR WORKSHEET 2   <------------
worksheet_python.write(0,0,'section_links')


# heading for 1st oth column will section links
# python Section links 
for i in range(len(python_questions)):
    worksheet_python.write(0,i+1,'section '+str(i+1))


# heading the first row of columns from 1 to 8 with section no.
for i in range(len(python_section_links)):
    worksheet_python.write(i+1,0,python_section_links[i])


# heading the first row of columns from 9 to 16 with section no. question statement
for i in range(len(python_questions)):
    worksheet_python.write(0,i+18,'section '+str(i+1)+' question statements')
    

# filling the all row of columns from 1 to 17 with respective section question links
for i in range(len(python_questions)):
    for j in range(len(python_questions[i])):
        worksheet_python.write(j+1,i+1,python_questions[i][j])
 
 
# filling the all row of columns from 18 to 34 with respective section question statements   
count = 0
for i in range(len(python_questions)):
    for j in range(len(python_questions[i])):
        worksheet_python.write(j+1,8+i,python_questions_statements[count])
        count += 1
        

workbook.close()
         
        
         

    
    




