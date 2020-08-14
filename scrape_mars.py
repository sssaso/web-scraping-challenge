from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():

    #For windows users
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    ### NASA Mars News website to scrape ####################################
    news_url='https://mars.nasa.gov/news/'
    

    # Scrape page into Soup
    browser.visit(news_url)
    news_html = browser.html
    time.sleep(2)
    news_soup = bs(news_html, 'html.parser')
    
    # Get the news title and paragraph
    news_title = news_soup.find_all('div', class_="content_title")[1].text
    news_paragraph = news_soup.find('div', class_="article_teaser_body").text


    ### JPL Mars Space Images to scrape ######################################
    img_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    # to get the full size jpg img of the FEATURED IMAGE on the first page by Clicking "FULL IMAGE" button
    # and click "more info" button  to get to the full image
    full_img = browser.find_by_id('full_image').first.click()
    time.sleep(1)
    browser.click_link_by_partial_text('more info')

    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')
    time.sleep(1)
    
    partial_img_url = img_soup.find('img', class_="main_image")['src']
    featured_img_url = "https://www.jpl.nasa.gov" + partial_img_url 

    ### Mars weather from Twitter  ########################################
    twitter_mars_url = 'https://twitter.com/marswxreport?lang=en'

    # visit the url
    browser.visit(twitter_mars_url)
    time.sleep(1)

    twtr_html = browser.html
    twtr_soup = bs(twtr_html, 'html.parser')

    # latest weaather tweet
    latest_weather_tweet = twtr_soup.find_all('div', lang="en")[0].text

    ### Mars facts #########################################################
    mars_fact_url= "https://space-facts.com/mars/"
    browser.visit(mars_fact_url)

    # Use Pandas to read_html
    tables = pd.read_html(mars_fact_url)
    df = tables[0]
    #add columns name
    df.columns = ['Items', 'Value']
    html_facts_table = df.to_html()
    #remove "\n"
    html_facts_table = html_facts_table.replace('\n', '')

    ### Mars Hemispheres ###################################################
    usgs_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # visit the site with Google Chrome
    browser.visit(usgs_url)
    hemi_html = browser.html
    mars_hemi_soup = bs(hemi_html, 'html.parser')

    # get info that contains the 4 image links
    items = mars_hemi_soup.find_all('div', class_='item')
    # Create empty list 
    hemisphere_image_urls = []
    #for loop to get the img title and img link from the list items
    for i in items:
        #title
        title = i.find('h3').text
        title = title.replace(" Enhanced", "")
        # partial image url
        partial_img_url = i.find('a').find('img')['src']
        # getting full image url 
        img_url = 'https://astrogeology.usgs.gov' + partial_img_url
        
        # Adding to dictionary
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})


    # Store data in a dictionary
    mars_data = {
        "Mars_News_Title": news_title,
        "Mars_News_Paragraph": news_paragraph,
        "Mars_Featured_Image": featured_img_url,
        "Mars_Weather_Data": latest_weather_tweet,
        "Mars_Facts": html_facts_table,
        "Mars_Hemisphere_Images": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
