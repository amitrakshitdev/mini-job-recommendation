import asyncio
from bs4 import BeautifulSoup
from patchright.async_api import async_playwright
import sys
import json
import os
import csv
from pathlib import Path
from nanoid import generate
# from utils.string_utils import parse_experience_string
curr_dir = Path(__file__).resolve().parent.parent / "user_data"

sys.path.append("../")
# from log.logger import logger

async def __get_job_description__(browser, job_data, index):
    page = await browser.new_page()
    link = job_data[index]["link"]
    await page.goto(link, timeout=60000)
    await page.wait_for_selector("section[class^=styles_job-desc-container]")
    job_description_element = page.locator('section[class^=styles_job-desc-container]').first
    key_skills_elements = await job_description_element.locator('div[class^="styles_key-skill"] > div > a > span').all()
    key_skills = []
    for key_skill_element in key_skills_elements:
        key_skill = await key_skill_element.text_content()
        key_skills.append(key_skill.strip())
    job_data[index]["key_skills"] = key_skills
    jd_inner_html = await job_description_element.locator("div[class^='styles_JDC__dang-inner-html']").first.inner_html()
    job_data[index]["job_description"] = jd_inner_html.strip()
    await page.close()
    return (job_data[index], index)

async def scrape_naukri(url, page_number=1):
    async with async_playwright() as p:
        # Launch a browser (e.g., Chromium, Firefox, or WebKit)
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=curr_dir,
            headless=False, 
            channel="chrome", 
            no_viewport=True)
        page = await browser.new_page()

        try:
            if (page_number != 1):
                url = f"{url}-{page_number}"
            
            await page.goto(url, timeout=60000) # Increased timeout

            await page.wait_for_selector('div.srp-jobtuple-wrapper') # Example selector, needs 
            job_listings = await page.locator('div.srp-jobtuple-wrapper').all() # Example selector
            job_data = []

            # Get details from the listings
            for index, job in enumerate(job_listings):
                try:
                    title_element = job.locator('h2 a.title').first
                    title = await title_element.text_content() if title_element else "N/A"
                    
                    link = await title_element.get_attribute("href") if title_element else "N/A"

                    company_element = job.locator('a.comp-name').first
                    company = await company_element.text_content() if company_element else "N/A"

                    location_element = job.locator('span.locWdth').first
                    location = await location_element.text_content() if location_element else "N/A"

                    experience_element = job.locator('span.expwdth').first
                    experience = await experience_element.text_content() if experience_element else "N/A"
                    parsed_experence = parse_experience_string(experience)
                    exp_str = parsed_experence["experience_raw"]
                    exp_min_yrs = parsed_experence["experience_min_years"]
                    exp_max_yrs = parsed_experence["experience_max_years"]
                    experience_level_keywords = parsed_experence["experience_level_keywords"]
                    level_keywords = experience_level_keywords
                    job_post_date = await job.locator('span.job-post-day').inner_text() if job.locator('span.job-post-day') else "N/A"

                    
                    job_details = {
                        "id": generate(size=15),
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location.strip(),
                        "experience": exp_str,
                        "experience_min_years": exp_min_yrs,
                        "experience_max_years": exp_max_yrs,
                        "post_date": job_post_date.strip(),
                        "link": link,
                    }

                    job_data.append(job_details)

                except Exception as e:
                    print(f"Error scraping job: {e}")
                    # You might want to log the HTML of the failed job for debugging
                    # print(await job.inner_html())

            # Open each link and get job description inner html
            get_job_des_coroutines = [__get_job_description__(browser, job_data, index) for index, job in enumerate(job_data)]
            
            new_job_data = await asyncio.gather(*get_job_des_coroutines)
            job_data = [job for job, _ in new_job_data]

            # Save to JSON
            file_path = "data/naukri_output.json"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file_path = f"data/naukri_output_{page_number}.json"
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(job_data, json_file, indent=4)


        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

def merge_jsons_into_one(directory, file_prefix, range_start, range_end):
    merged_data = []
    for i in range(range_start, range_end + 1):
        file_path = f"{directory}/{file_prefix}_{i}.json"
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            merged_data.extend(data)

    # Save merged data to a new JSON file
    output_file_path = f"{directory}/{file_prefix}_merged.json"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(merged_data, output_file, indent=4)
    
    # for i in range(range_start, range_end + 1):
    #     os.remove(f"{directory}/{file_prefix}_{i}.json")






def clean_and_format_job_description(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_output = []

    # 1. Main Job Description
    job_description_div = soup.find('div', class_='styles_JDC__dang-inner-html__h0K4t')
    if job_description_div:
        markdown_output.append("## Job Description\n")
        # Replace <br> tags with newlines for better readability
        description_text = job_description_div.get_text(separator='\n').strip()
        markdown_output.append(description_text)
        markdown_output.append("\n")

    # 2. Other Details (Role, Industry Type, etc.)
    other_details_div = soup.find('div', class_='styles_other-details__oEN4O')
    if other_details_div:
        markdown_output.append("## Other Details\n")
        for detail_div in other_details_div.find_all('div', class_='styles_details__Y424J'):
            label = detail_div.find('label')
            if label:
                label_text = label.get_text().strip().replace(':', '')
                spans = detail_div.find_all('span')
                values = []
                for span in spans:
                    # Get text from span, and also from <a> tags inside
                    span_text = span.get_text(separator=', ').strip()
                    values.append(span_text)
                markdown_output.append(f"- **{label_text}:** {', '.join(values).strip(',')}\n")
        markdown_output.append("\n")

    # 3. Education
    education_div = soup.find('div', class_='styles_education__KXFkO')
    if education_div:
        markdown_output.append("## Education\n")
        for edu_detail_div in education_div.find_all('div', class_='styles_details__Y424J'):
            label = edu_detail_div.find('label')
            if label:
                label_text = label.get_text().strip().replace(':', '')
                value = edu_detail_div.find('span')
                if value:
                    markdown_output.append(f"- **{label_text}:** {value.get_text().strip()}\n")
        markdown_output.append("\n")


    # 4. Key Skills
    key_skills_div = soup.find('div', class_='styles_key-skill__GIPn_')
    if key_skills_div:
        markdown_output.append("## Key Skills\n")
        skills = []
        for skill_tag in key_skills_div.find_all('a', class_='styles_chip__7YCfG'):
            skill_text = skill_tag.find('span')
            if skill_text:
                skills.append(skill_text.get_text().strip())
        if skills:
            markdown_output.append(", ".join(skills) + "\n")
        markdown_output.append("\n")

    # Remove any extra elements like footer, modal, etc.
    # These are usually not part of the core job description
    footer = soup.find('div', class_='styles_JDC__footer__ZJnPe')
    if footer:
        footer.decompose() # Remove from soup

    modal_container = soup.find('div', class_='styles_modal-container__Ks9eE')
    if modal_container:
        modal_container.decompose()

    backdrop = soup.find('div', class_='styles_mc__backdrop__GNySo')
    if backdrop:
        backdrop.decompose()


    return "".join(markdown_output).strip()

async def main(search_query="Software Engineering Jobs", start_page=1, end_page=5):
    query_string = search_query.replace(" ", "-").lower().strip()
    url = f"https://www.naukri.com/{query_string}"
    
    for i in range(start_page, end_page + 1):
        await scrape_naukri(url, i)
        print(f"Scraped page {i}")
    merge_jsons_into_one("data", "naukri_output", start_page, end_page)

if __name__ == '__main__':
    merge_jsons_into_one("data", "naukri_output", 1, 20)