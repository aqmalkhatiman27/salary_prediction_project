from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Function to scrape job listing page (titles, locations, salaries, job types, job URLs)
def scrape_job_listings(soup):
    job_listings = soup.find_all('a', class_='css-17aghwz')  # Adjust this based on the actual class names
    
    job_titles = []
    locations = []
    salaries = []
    job_types = []
    job_links = []
    
    for job in job_listings:
        # Extract job title
        title_div = job.find('h2', class_='css-ihtf6b')
        title = title_div.text if title_div else 'N/A'

        # Extract salary
        salary_div = job.find('div', class_='css-1jco3p8')
        salary = salary_div.find('h4', class_='css-1biyf3w').text if salary_div else 'N/A'

        # Extract job location
        location_div = job.find('div', class_='css-5s06qz')
        location = location_div.find('h4', class_='css-1biyf3w').text if location_div else 'N/A'

        # Extract job type
        job_type_div = job.find('div', class_='css-15mx9cn')
        job_type = job_type_div.text if job_type_div else 'N/A'

        # Extract the href directly from the 'a' tag
        job_href = job['href']
        job_url = 'https://my.hiredly.com' + job_href
        
        # Append the data to the lists
        job_titles.append(title)
        locations.append(location)
        salaries.append(salary)
        job_types.append(job_type)
        job_links.append(job_url)

    return job_titles, locations, salaries, job_types, job_links

# Function to scrape a fixed number of pages
def scrape_pages(start_page, end_page):
    all_job_titles = []
    all_locations = []
    all_salaries = []
    all_job_types = []
    all_job_links = []

    for page in range(start_page, end_page + 1):
        # Build the URL for the current page
        url = f'https://my.hiredly.com/jobs?page={page}'
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Get the page content and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Scrape job listings from the current page
        job_titles, locations, salaries, job_types, job_links = scrape_job_listings(soup)
        all_job_titles.extend(job_titles)
        all_locations.extend(locations)
        all_salaries.extend(salaries)
        all_job_types.extend(job_types)
        all_job_links.extend(job_links)
        
        print(f"Scraped page {page}")

    # Create a DataFrame with the collected data
    job_data = pd.DataFrame({
        'Job Title': all_job_titles,
        'Location': all_locations,
        'Job Type': all_job_types,
        'Salary': all_salaries,
        'Job URL': all_job_links
    })

    # Save the DataFrame to a CSV file
    job_data.to_csv('scraped_job_vacancies_data.csv', index=False)
    print("Job data with salary and job type has been saved to scraped_job_vacancies_data.csv")

# Step 1: Scrape from page 1 to page 40
scrape_pages(1, 40)

# Close the WebDriver
driver.quit()
