from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import datetime
import time
pages = []
weeks_on_the_list = []
titles = []
authors = []
descriptions = []

books = {'Author':authors,'Title': titles,'Weeks': weeks_on_the_list, 'Description': descriptions}

start_date = datetime.datetime(2017,4, 30)
end_date = datetime.datetime(2017, 9, 17)

#periods = how many weeks to scrape from given date
daterange = pd.date_range(start=start_date,end=end_date, periods=1)

for single_date in daterange:
    single_date = single_date.strftime("%Y/%m/%d")
    url =("https://www.nytimes.com/books/best-sellers/" + single_date + "/combined-print-and-e-book-nonfiction/")
    pages.append(url)
for book in pages:
    page = requests.get(book)
    soup = bs4(page.text, 'html.parser')
    for Title in soup.findAll('h3', class_='css-5pe77f', itemprop='name',recursive=True):
        title = Title.getText()
        titles.append(title)
    for weeks in soup.findAll('p', class_='css-1o26r9v', recursive=True):
        week = weeks.getText()
        weeks_on_the_list.append(week)
    for Author in soup.findAll('p', class_="css-hjukut",itemprop="author", recursive=True):
        author = Author.getText()
        author = author.replace("by","")
        authors.append(author)
    for Description in soup.findAll('p', itemprop="description", class_="css-14lubdp", recursive=True):
        description = Description.getText()
        descriptions.append(description)

        
df = pd.DataFrame(data=books)
#leaving only the biggest value of "Weeks on the list"
df.sort_values(['Weeks','Author'], ascending = True)
df.drop_duplicates(['Title','Author'], keep="last",inplace=True)
#export
# new date format for export
output_start_date = start_date
output_end_date = end_date
output_start_date = output_start_date.strftime("%Y-%m-%d")
output_end_date = output_end_date.strftime("%Y-%m-%d")
df.index += 1
df.to_excel(f"NYtimes {output_start_date} - {output_end_date}.xlsx")
