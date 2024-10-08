from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)

# Initialize the WebDriver (you no longer need to specify the path if chromedriver is in /usr/local/bin)
driver = webdriver.Chrome(options=chrome_options)

# Step 2: Open the Job Listing Page
url = 'https://my.hiredly.com/jobs'
driver.get(url)

# Wait for the page to fully load
time.sleep(5)

# Step 3: Extract the page's HTML content after JavaScript has loaded the jobs
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Step 4: Scrape Job Listings
job_listings = soup.find_all('a', class_='css-17aghwz')  # Adjust this based on the actual class names
print(len(job_listings))

job_titles = []
locations = []
salaries = []
job_links = []

for job in job_listings:
    # Extract job title (adjust based on the correct HTML structure)
    title = job.find('h2', class_='css-ihtf6b').text if job.find('h2', class_='css-ihtf6b') else 'N/A'
    
    # Extract job location
    location_div = job.find('div', class_='css-5s06qz')
    location = location_div.find('h4', class_='css-1biyf3w').text if location_div else 'N/A'
    
    # Extract salary if available
    salary_div = job.find('div', class_='css-1jco3p8')
    salary = salary_div.find('h4', class_='css-1biyf3w').text if salary_div else 'N/A'
    
    # Extract the href directly from the 'a' tag
    job_href = job['href']
    job_url = 'https://my.hiredly.com' + job_href
    
    # Append the data to the lists
    job_titles.append(title)
    locations.append(location)
    salaries.append(salary)
    job_links.append(job_url)

# Step 5: Scrape Experience Data from Each Job's Detail Page
def scrape_experience(job_url):
    driver.get(job_url)
    time.sleep(2)  # Give the page time to load
    
    job_html = driver.page_source
    job_soup = BeautifulSoup(job_html, 'html.parser')
    
    # Scrape the experience information (adjust the class as needed)
    experience = job_soup.find('p', class_='css-1y84bo9').text if job_soup.find('p', class_='css-1y84bo9') else 'N/A'
    
    return experience

experience_data = []

for job_url in job_links:
    experience = scrape_experience(job_url)
    experience_data.append(experience)
    time.sleep(3)  # Wait for 3 seconds between requests to avoid overwhelming the server

# Step 6: Save the Data to a CSV File
job_data = pd.DataFrame({
    'Job Title': job_titles,
    'Location': locations,
    'Salary': salaries,
    'Experience': experience_data,
    'Job URL': job_links
})

# Save the DataFrame to a CSV file
job_data.to_csv('job_vacancies_with_experience_and_salary.csv', index=False)
print("Job data with experience and salary has been saved to job_vacancies_with_experience_and_salary.csv")

# Close the WebDriver
driver.quit()
