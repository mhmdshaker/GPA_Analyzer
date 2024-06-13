from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# #to remove opening the webpage:
# Set up Firefox options
# options = FirefoxOptions()
# options.add_argument("--headless")

# Set up the WebDriver for Firefox
service = Service(executable_path='/usr/local/bin/geckodriver')  # Replace with the actual path to geckodriver
driver = webdriver.Firefox(service=service)

# Open the webpage
driver.get('https://www-banner.aub.edu.lb/pls/weba/bwckschd.p_disp_dyn_sched')

# Give the page some time to load
wait = WebDriverWait(driver, 0)

# Set to store the courses:
s = set()

# Get all semesters from the dropdown
semester_dict = {option.get_attribute('value'): option.text for option in Select(driver.find_element(By.NAME, 'p_term')).options}

for semester in semester_dict:
    if semester == "":
        continue
    
    #go back to the webpage of the semester choosing:
    driver.get('https://www-banner.aub.edu.lb/pls/weba/bwckschd.p_disp_dyn_sched')

    # Select the semester you want (replace the value with the desired term's value)
    select_term = Select(driver.find_element(By.NAME, 'p_term'))
    select_term.select_by_value(semester)

    # Submit the form: Click the Submit button
    driver.find_element(By.ID, 'id____UID0').click()

    # Wait for the subject dropdown to load
    wait.until(EC.presence_of_element_located((By.ID, 'subj_id')))

    # Get all categories of courses from the dropdown: ex : EECE department
    select_subject = Select(driver.find_element(By.ID, 'subj_id'))
    option_values = [option.get_attribute('value') for option in select_subject.options]

    # Iterate through all subject values in the subject dropdown
    for subject in option_values:
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary
        element = wait.until(EC.element_to_be_clickable((By.ID, 'subj_id')))

        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # Re-find the dropdown and select the option by its value
        Select(element).select_by_value(subject)
        
        #Submit the form: Click the Submit button
        driver.find_element(By.ID, 'id____UID0').click()
        
        # Extract the page source in html format in orcer to search through the links of the form 'a' <a> tag
        html = driver.page_source
        # Parse the page with BeautifulSoup to navigate easier
        soup = BeautifulSoup(html, 'html.parser')

        # Find all <a> tags with href containing 'bwckschd.p_disp_detail_sched'
        course_links = soup.find_all('a', href=True)
        # Iterate over each <a> tag
        for course in course_links:
            if 'bwckschd.p_disp_detail_sched' in course['href']:
                # Extract the text
                course_name = course.text.strip()
                parts = course_name.split(' ')
                course_name = parts[-4] + ' ' + parts[-3]
                s.add(course_name)
                
        # Return to the previous page to select another subject by clicking the 'Return to Previous' link
        return_link = driver.find_element(By.LINK_TEXT, 'Return to Previous')
        return_link.click()

# Close the browser
driver.quit()
