# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests

# Initialize browser
def init_browser(): 
	# Path to chromedriver
	executable_path = {"executable_path": "chromedriver"}
	return Browser("chrome", **executable_path, headless=False)

# Create dictionary to be imported into Mongo
mars_info = {}

# NASA Mars News
def scrape_mars_news():

		
    # Initialize browser 
    browser = init_browser()

    # Visit the NASA Mars news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Collect the latest News title and paragraph
    news_t = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Dictionary entry from Mars News
    mars_info['news_title'] = news_t
    mars_info['news_paragraph'] = news_p

    return mars_info


    browser.quit()

# Featured Image
def scrape_mars_image():

    # Initialize browser 
    browser = init_browser()

    # Visit the url for JPL Featured Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Scrape page into Soup
    html_image = browser.html
    soup = bs(html_image, "html.parser")

    # Find featured image url
    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Main website url
    web_url = "https://www.jpl.nasa.gov"

    # Concatenate urls from main website and featured image
    featured_image_url = web_url + featured_image_url

    # Display full link
    featured_image_url

    # Dictionary entry from featured image
    mars_info['featured_image_url'] = featured_image_url

    return mars_info

    browser.quit()

# Mars Weather 
def scrape_mars_weather():


	# Initialize browser
	browser = init_browser()

	# Visit the Mars Weather Twitter account
	twitter_url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(twitter_url)

	# Scrape page into Soup
	html_twitter = browser.html
	soup = bs(html_twitter, "html.parser")

	# Find all tweets
	all_tweets = soup.find_all('div', class_='js-tweet-text-container')

	# Retreive all weather related news titles
	for tweet in all_tweets:
		mars_weather = tweet.find('p').text
		if 'Sol' and 'pressure' in mars_weather:
			print(mars_weather)

			break

		else:

			pass

	# Dictionary entry from Mars Weather
	mars_info['mars_weather'] = mars_weather

	return mars_info

	browser.quit()

# Mars Facts
def scrape_mars_facts():

	# Visit the Mars Facts webpage
	mars_facts_url = "https://space-facts.com/mars/"

	# Use Pandas to scrape tables
	mars_facts = pd.read_html(mars_facts_url)

	# Get mars facts dataframe
	mars_df = mars_facts[1]
	mars_df.columns = ['MARS PLANET PROFILE','Value']
	mars_df.set_index('MARS PLANET PROFILE', inplace=True)

	# Convert the data to an HTML table string
	data = mars_df.to_html()

	# Dictionary entry from Mars Facts
	mars_info['mars_facts'] = data

	return mars_info

# Mars Hemispheres

def scrape_mars_hemispheres():


	# Initialize browser 
	browser = init_browser()

	# Visit the USGS Astrogeology site
	USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(USGS_url)

	# Scrape page into Soup
	html_USGS = browser.html
	soup = bs(html_USGS, "html.parser")

	# Find all items that contain mars hemispheres info
	items = soup.find_all('div', class_='item')

	# Create empty list for image urls
	image_urls = []

	# Main website url
	web_url = "https://astrogeology.usgs.gov"

	# Loop through itmes
	for i in items:

		title = i.find('h3').text

		# Store link to image site
		image_site_url = i.find('a', class_='itemLink product-item')['href']

		# Visit full image site
		browser.visit(web_url + image_site_url)

		# Scrape individual image site into Soup
		image_site_html = browser.html
		soup = bs(image_site_html, "html.parser")

		# Retreive full image urls
		img_url = web_url + soup.find('img', class_='wide-image')['src']

		# Append the image urls to list of dictionaries
		image_urls.append({"title" : title, "img_url" : img_url})

		# Dictionary entry form Mars Hemispheres
		mars_info['image_urls'] = image_urls

		return mars_info

	browser.quit()



