from bs4 import BeautifulSoup
import requests
import json


searchquery = "backend developer"
searchquery = searchquery.replace(" ", "%20")
url = f"https://www.coursera.org/search?query={searchquery}&sortBy=BEST_MATCH"

page = requests.get(url)
soup = BeautifulSoup(page.text,'html')
ld_json_script = soup.find("script", type="application/ld+json")
data = json.loads(ld_json_script.string)

first_url = data.get("itemListElement", [])[0].get("url", None)
url1 = first_url
page1 = requests.get(url1)
soup1 = BeautifulSoup(page1.text,'html')

ld_json1  = soup1.find("script", type="application/ld+json")
track_skills = 0
if ld_json1:
    data = json.loads(ld_json1.string)

    # Look for the "Course" item in @graph
    for item in data.get("@graph", []):
        if item.get("@type") == "Course":
            skills = item.get("About", {}).get("name", [])
            track_skills = skills
            print("skills saved")

else:
    print("No JSON-LD script found.")


title_div = soup1.find('div', class_='css-1q5srzp')

if title_div:
    course_name = title_div.get_text(strip=True)
    print(course_name)
else:
    print("Title not found.")


track_title = ""
title_div = soup1.find('div', class_='css-1q5srzp')

# Extract text
if title_div:
    specialization_title = title_div.get_text(strip=True)
    track_title = specialization_title
    print("Specialization Title:", track_title)
else:
    print("Title not found.")


link_tags = soup1.find_all('a', href=True)
course_info = []

divs = soup1.find_all('div', class_='css-3odziz')

# Loop through and filter links that contain a course path
for link_tag in link_tags:
    href = link_tag['href']
    if href.startswith('/learn/'):
        course_name = href.replace("-"," ").replace("/learn/","").split("?")[0]
        full_url = 'https://www.coursera.org' + href
        course_info.append({"Name":course_name,"URL":full_url})


divs = soup1.find_all('div', class_='css-3odziz')

durations = []
for div in divs:
    # the third span contains nested span with the hours text
    hours_span = div.find_all('span')[2]
    hours_text = hours_span.text.strip()
    durations.append(hours_text)
    print(hours_text)

# Add duration to each dictionary by index
for i, duration in enumerate(durations):
    course_info[i]['Duration'] = duration

course_info

description_tag = soup1.find('meta', attrs={'name': 'description'})
if description_tag and 'content' in description_tag.attrs:
    description = description_tag['content']
    # If you want just the part after "Offered by Board Infinity . ", you can split:
    desc_text = description.split('Offered by Board Infinity . ')[-1].strip()
    print(description)
else:
    print("Description not found")

page1 = requests.get(url1)
soup1 = BeautifulSoup(page1.text,'html')

subpages3 = page1.text.split('<h4 class=\"css-6ecy9b">Skills you')
course_skills = []
soups1 = str(soup1).split('<h4 class=\"css-6ecy9b">Skills you\'ll gain</h4>')
for page3 in subpages3:
    soup3 = BeautifulSoup(page3,'html')
    skill_spans = soup3.find_all('span', class_='css-o5tswl')

    # Extract the skill text
    skills = [span.get_text(strip=True) for span in skill_spans]
    course_skills.append(skills)

course_skills = course_skills[1:]
print(course_skills)  # Output: ['React (Web Framework)', 'JavaScript']


for i, skills in enumerate(course_skills):
    course_info[i]['Skills'] = skills


course_details = []

# Find all elements with that big class (exact match of all those classes)
containers = soup1.select('.cds-9.css-xalpg1.cds-11.cds-grid-item.cds-56.cds-80')

for container in containers:
    # Inside each container, find all matching text elements
    elements = container.select('.rc-CML p span span')
    for el in elements:
        text = el.get_text(strip=True)
        course_details.append(text)
    else:
        # Continue outer loop only if inner loop was NOT broken
        continue
    # If inner loop was broken, break outer loop too
    break

for i, t in enumerate(course_details, 1):
    print(f"{i}. {t}")


Track = {"name": track_title,
         "URL": first_url,
         "Details": course_details,
         "Skills": track_skills,
         "Courses": course_info
}


print(Track)

