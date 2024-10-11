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

# Function to scrape job data on each page
def scrape_job_listings(soup):
    job_listings = soup.find_all('a', class_='css-17aghwz')  # Adjust this based on the actual class names
    
    job_titles = []
    locations = []
    salaries = []
    job_links = []
    
    for job in job_listings:
        # Extract job title
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

    return job_titles, locations, salaries, job_links

# Function to scrape experience data from each job's detail page
def scrape_experience(job_url):
    driver.get(job_url)
    time.sleep(2)  # Give the page time to load
    
    job_html = driver.page_source
    job_soup = BeautifulSoup(job_html, 'html.parser')
    
    # Scrape the experience information (adjust the class as needed)
    experience = job_soup.find('p', class_='css-1y84bo9').text if job_soup.find('p', class_='css-1y84bo9') else 'N/A'
    
    return experience

# Function to scrape a fixed number of pages
def scrape_pages(start_page, end_page):
    all_job_titles = []
    all_locations = []
    all_salaries = []
    all_job_links = []
    all_experiences = []

    for page in range(start_page, end_page + 1):
        # Build the URL for the current page
        url = f'https://my.hiredly.com/jobs?page={page}'
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Get the page content and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Scrape job listings from the current page
        job_titles, locations, salaries, job_links = scrape_job_listings(soup)
        all_job_titles.extend(job_titles)
        all_locations.extend(locations)
        all_salaries.extend(salaries)
        all_job_links.extend(job_links)

        # Scrape experience for each job on this page
        for job_url in job_links:
            experience = scrape_experience(job_url)
            all_experiences.append(experience)
            time.sleep(3)  # Wait for 3 seconds between requests
        
        print(f"Scraped page {page}")

    # Create a DataFrame with the collected data
    job_data = pd.DataFrame({
        'Job Title': all_job_titles,
        'Location': all_locations,
        'Salary': all_salaries,
        'Experience': all_experiences,
        'Job URL': all_job_links
    })

    # Save the DataFrame to a CSV file
    job_data.to_csv('job_vacancies_with_experience_and_salary.csv', index=False)
    print("Job data with experience and salary has been saved to job_vacancies_with_experience_and_salary.csv")

# Step 1: Scrape from page 1 to page 15
scrape_pages(1, 15)

# Close the WebDriver
driver.quit()
