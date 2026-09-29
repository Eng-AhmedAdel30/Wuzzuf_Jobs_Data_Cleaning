import csv
from itertools import zip_longest

import requests
from bs4 import BeautifulSoup


PAGE_NUM = 0

job_titles_list = []
company_names = []
locations = []
time_posted = []
full_part = []
work_sites = []
all_info = []
links = []


while PAGE_NUM <= 15:
    try:
        url = (
            "https://wuzzuf.net/search/jobs/"
            "?a=spbl"
            "&filters%5Broles%5D%5B0%5D=IT%2FSoftware%20Development"
            "&q=data%20engineer"
            f"&start={PAGE_NUM}"
        )

        response = requests.get(url)

        soup = BeautifulSoup(response.content, "lxml")

        job_titles = soup.find_all("h2", {"class": "css-m604qf"})

        locations_found = soup.find_all(
            "span",
            {"class": "css-5wys0k"},
        )

        time_classes = ["css-do6t5g", "css-4c4ojb"]
        time_created = soup.find_all(
            "div",
            {"class": time_classes},
        )

        company_name = soup.find_all(
            "a",
            {"class": "css-17s97q8"},
        )

        info = soup.find_all(
            "div",
            {"class": "css-y4udm8"},
        )

        full_part_found = soup.find_all(
            "a",
            {"class": "css-n2jc4m"},
        )

        sites = soup.find_all(
            "span",
            {"class": "css-o1vzmt eoyjyou0"},
        )

        for index in range(len(job_titles)):
            try:
                job_titles_list.append(
                    job_titles[index].text.strip()
                )

                links.append(
                    job_titles[index]
                    .find("a")
                    .attrs["href"]
                )

                company_names.append(
                    company_name[index].text.strip()
                )

                locations.append(
                    locations_found[index].text.strip()
                )

                time_posted.append(
                    time_created[index].text.strip()
                )

                all_info.append(
                    info[index].text.strip()
                )

                work_sites.append(
                    sites[index].text.strip()
                )

                full_part.append(
                    full_part_found[index].text.strip()
                )

            except Exception as error:
                print(
                    f"Error processing job {index}: {error}"
                )
                continue

        print(f"Processed page {PAGE_NUM + 1}")
        PAGE_NUM += 1

    except Exception as error:
        print(
            f"Error processing page {PAGE_NUM}: {error}"
        )
        break


data = [
    job_titles_list,
    company_names,
    locations,
    time_posted,
    all_info,
    full_part,
    work_sites,
    links,
]

data_list = zip_longest(*data)

output_file = (
    r"E:\.Eng_Ahmed\2 Data Engineer\newwwww.csv"
)

with open(
    output_file,
    "w",
    encoding="utf-8-sig",
    newline="",
) as data_file:
    writer = csv.writer(data_file)

    writer.writerow(
        [
            "job_title",
            "company name",
            "company location",
            "time posted",
            "skills",
            "job type",
            "job place",
            "link",
        ]
    )

    writer.writerows(data_list)
