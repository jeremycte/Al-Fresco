import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()

import pandas as pd


import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
from selenium import webdriver
from bs4 import BeautifulSoup
from parsel import Selector

from selenium.webdriver.common.by import By
import time

from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome()
driver = webdriver.Chrome(ChromeDriverManager().install())

def search_score(location):
    keywords = location
    keywords.replace(" ", "+")

    url = 'https://www.google.com/maps/search/' + keywords + '+singapore'
    driver.get(url)

    def check_exists_by_xpath(xpath):
        try:
            wait = WebDriverWait(driver, 5)
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    for i in range(35, 50):
        xpath = '//*[@id="pane"]/div/div[1]/div/div/div['+str(i)+']/div/button'

        if check_exists_by_xpath(xpath) == True:
            driver.find_element(By.XPATH, xpath).click()
            break
        else:
            continue
    time.sleep(3)

    #Find scroll layout
    scrollable_div = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]')

    #Scroll as many times as necessary to load all reviews
    for i in range(0,10):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(1)



    page_content = driver.page_source
    response = Selector(page_content)

    results = []

    for el in response.xpath('//div/div[@data-review-id]/div[contains(@class, "content")]'):
        results.append({
            'title': el.xpath('.//div[contains(@class, "title")]/span/text()').extract_first(''),
            'rating': el.xpath('.//span[contains(@aria-label, "stars")]/@aria-label').extract_first('').replace('stars' ,'').strip(),
            'body': el.xpath('.//span[contains(@class, "text")]/text()').extract_first(''),
        })


    df = pd.DataFrame(results)
    df.dropna()
    df['rating'] = pd.to_numeric(df['rating'])
    df.head()

    import nltk
    from nltk.corpus import stopwords
    from wordcloud import WordCloud

    stopwords = set(stopwords.words('english'))
    stopwords.update(["campus", "NUS", "MRT", "looks", "food"])
    textt = " ".join(review for review in df['body'])
    # wordcloud = WordCloud(stopwords=stopwords).generate(textt)

    # assign reviews with score > 3 as positive sentiment
    # score < 3 negative sentiment

    df['sentiment'] = df['rating'].apply(lambda score : +1 if score > 3.5 else -1)

    positive = df[df['sentiment'] == 1]
    negative = df[df['sentiment'] == -1]

    #stopwords = set(stopwords.words('english'))
    stopwords.update(['i', 'I', 'The', 'the', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'place', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "...", "-"]) 

    pos = " ".join(review for review in positive['body'])
    # wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)

    pos = pos.split()
    for word in list(pos):  # iterating on a copy since removing will mess things up
        if word in stopwords:
            pos.remove(word)

    from collections import Counter
    counts = Counter(pos)

    top_words = counts.most_common(5)

    neg = " ".join(review for review in negative['body'])
    # wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
    df['sentiment'] = df['sentiment'].replace({-1 : 'negative'})
    df['sentiment'] = df['sentiment'].replace({1 : 'positive'})

    score = df['sentiment'].value_counts()['positive'] / (df['sentiment'].value_counts()['negative'] + df['sentiment'].value_counts()['positive']) 

    score = float(score)
    score = round(score, 2)

    rec = ""

    if score >= 0.8:
        rec = " Must Visit"
    elif score < 0.8 and score >= 0.6:
        rec = " Good To Visit"
    elif score < 0.6 and score >= 0.4:
        rec = " Average Sentiments"
    else:
        rec = " Poor Sentiments"

    final = " "
    score = str(score)
    final = final + score + "," + " " + rec
    return final

# print(search_score("starvista"))


def search_reviews(location):
    keywords = location
    keywords.replace(" ", "+")

    url = 'https://www.google.com/maps/search/' + keywords + '+singapore'
    driver.get(url)

    def check_exists_by_xpath(xpath):
        try:
            wait = WebDriverWait(driver, 5)
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    for i in range(35, 50):
        xpath = '//*[@id="pane"]/div/div[1]/div/div/div['+str(i)+']/div/button'

        if check_exists_by_xpath(xpath) == True:
            driver.find_element(By.XPATH, xpath).click()
            break
        else:
            continue
    time.sleep(3)

    #Find scroll layout
    scrollable_div = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]')

    #Scroll as many times as necessary to load all reviews
    for i in range(0,10):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(1)



    page_content = driver.page_source
    response = Selector(page_content)

    results = []

    for el in response.xpath('//div/div[@data-review-id]/div[contains(@class, "content")]'):
        results.append({
            'title': el.xpath('.//div[contains(@class, "title")]/span/text()').extract_first(''),
            'rating': el.xpath('.//span[contains(@aria-label, "stars")]/@aria-label').extract_first('').replace('stars' ,'').strip(),
            'body': el.xpath('.//span[contains(@class, "text")]/text()').extract_first(''),
        })


    df = pd.DataFrame(results)
    df.dropna()
    df['rating'] = pd.to_numeric(df['rating'])
    df.head()

    import nltk
    from nltk.corpus import stopwords
    from wordcloud import WordCloud

    stopwords = set(stopwords.words('english'))
    stopwords.update(["campus", "NUS", "MRT", "looks", "food"])
    textt = " ".join(review for review in df['body'])
    # wordcloud = WordCloud(stopwords=stopwords).generate(textt)

    # assign reviews with score > 3 as positive sentiment
    # score < 3 negative sentiment

    df['sentiment'] = df['rating'].apply(lambda score : +1 if score > 3.5 else -1)

    positive = df[df['sentiment'] == 1]
    negative = df[df['sentiment'] == -1]

    #stopwords = set(stopwords.words('english'))
    stopwords.update(['i', 'I', 'The', 'the', 'like', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'place', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "...", "-", ".", "..", "NUS", ",,,", ",", "I", ""]) 

    pos = " ".join(review for review in positive['body'])
    # wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)

    pos = pos.split()
    for word in list(pos):  # iterating on a copy since removing will mess things up
        if word in stopwords:
            pos.remove(word)

    from collections import Counter
    counts = Counter(pos)

    top_words = counts.most_common(5)
    top_words2 = []

    for i in top_words:
        top_words2.append(i[0])

    neg = " ".join(review for review in negative['body'])
    # wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
    df['sentiment'] = df['sentiment'].replace({-1 : 'negative'})
    df['sentiment'] = df['sentiment'].replace({1 : 'positive'})

    score = df['sentiment'].value_counts()['positive'] / (df['sentiment'].value_counts()['negative'] + df['sentiment'].value_counts()['positive']) 

    score = float(score)
    score = round(score, 2)

    rec = ""

    if score >= 0.8:
        rec = " Must Visit"
    elif score < 0.8 and score >= 0.6:
        rec = " Good To Visit"
    elif score < 0.6 and score >= 0.4:
        rec = " Average Sentiments"
    else:
        rec = " Poor Sentiments"

    empty = " "

    for word in top_words2:
        empty = empty + word + "," + " "

    return empty


