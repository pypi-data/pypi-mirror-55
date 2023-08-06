import requests
import os
import re
import json
from bs4 import BeautifulSoup


class AcmTransSpider:
    papers_order = 1

    def __init__(self, url="https://dlnext.acm.org/toc/tompecs/2016/1/1", file_type="json"):
        self.url = url
        self.file_type = file_type

    def get_html(self, url):
        try:
            headers = {"User-Agent": "Safari/12.1.2"}
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            # delete all blank lines
            html = os.linesep.join([s for s in r.text.splitlines() if s])
            return html
        except:
            return ""

    def parse_page(self, html):
        try:
            current_issue_papers = []
            soup = BeautifulSoup(html, 'html.parser')
            vol = soup.title.string
            title_boxes = soup.findAll('h5', attrs={'class': 'issue-item__title'})
            author_boxes = soup.findAll('ul', attrs={'aria-label': 'authors'})
            detail_boxes = soup.findAll('div', attrs={'class': 'issue-item__detail'})
            # abstract_boxes = soup.findAll('div', attrs={'class': 'issue-item__abstract truncate-text trunc-done'})
            for i in range(0, len(title_boxes)):
                title = title_boxes[i].text.strip()
                title = re.sub(' +', ' ', title).strip()
                title = re.sub('\n', ' ', title).strip()
                if title == "List of Reviewers":
                    continue
                doi_num = str(title_boxes[i]).split("/doi/abs", 1)[1].split("\">", 1)[0]
                doi_link = "https://doi.org" + doi_num
                authors = re.sub('\n', ' ', author_boxes[i].text.strip())
                detail = detail_boxes[i].text.strip().split("https:")[0] + " ," + vol
                data = {
                    'paper_id': self.papers_order,
                    'paper_title': title,
                    'authors': authors,
                    'detail': detail,
                    'doi_link': doi_link
                }
                self.papers_order += 1
                current_issue_papers.append(data)
            print(current_issue_papers)
            next_box = soup.find('a', attrs={'class': 'content-navigation__btn--next'})
            next_issue_url = "https://dlnext.acm.org" + next_box['href']
            return current_issue_papers, next_issue_url
        except:
            return ""

    def store_to_txt(self, current_issue_papers, filename):
        try:
            for paper_info in current_issue_papers:
                paper_id = paper_info['paper_id']
                paper_title = paper_info['paper_title']
                doi_link = paper_info['doi_link']
                authors = paper_info['authors']
                detail = paper_info['detail']
                with open(filename, "a") as f:
                    f.write(
                        "paper%s\nTitle：%s\nAuthors：%s\nDetail：%s\nDoi_link：%s\n" % (paper_id,
                                                                                     paper_title, authors,
                                                                                     detail, doi_link))
                    f.write("==========================\n")
        except:
            return ""

    def acmtrans_spider_run_json(self, current_url="https://dlnext.acm.org/toc/tompecs/2016/1/1"):
        try:
            global next_issue_exist
            next_issue_exist = True
            file_name = current_url.split("/toc/")[1].split("/")[0] + ".json"
            global json_data
            json_data = {}
            json_data['papers'] = []
            while next_issue_exist:
                current_html = self.get_html(current_url)
                papers_list, next_url = self.parse_page(current_html)
                for paper_info in papers_list:
                    json_data['papers'].append(paper_info)
                if next_url.__contains__("javascript:void(0)"):
                    print("Goodbye, human!")
                    next_issue_exist = False
                    break
                current_url = next_url
            with open(file_name, "w") as f:
                json.dump(json_data, f)
        except:
            return ""

    def acmtrans_spider_run_txt(self, current_url="https://dlnext.acm.org/toc/tompecs/2016/1/1"):
        try:
            global next_issue_exist
            next_issue_exist = True
            file_name = current_url.split("/toc/")[1].split("/")[0] + ".txt"
            while next_issue_exist:
                current_html = self.get_html(current_url)
                papers_list, next_url = self.parse_page(current_html)
                self.store_to_txt(papers_list, file_name)
                if next_url.__contains__("javascript:void(0)"):
                    print("Goodbye, human!")
                    next_issue_exist = False
                    break
                current_url = next_url
        except:
            return ""

    def acmtrans_spider_run(self):
        if self.file_type == "txt":
            self.acmtrans_spider_run_txt(self.url)
        else:
            self.acmtrans_spider_run_json(self.url)


# Testing
if __name__ == '__main__':
    start_url = "https://dlnext.acm.org/toc/tompecs/2016/1/1"
    # start_url = "https://dlnext.acm.org/toc/tist/2010/1/1"
    filetype = "json"
    acmtrans_Spider = AcmTransSpider(start_url, filetype)
    acmtrans_Spider.acmtrans_spider_run()
