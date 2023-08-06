import requests
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
            html = r.text
            return html
        except ConnectionRefusedError:
            return ""

    def parse_page(self, html):
        try:
            current_issue_papers = []
            soup = BeautifulSoup(html, 'html.parser')
            vol = soup.title.string
            results = soup.findAll("div", {"class": "issue-item__content"})
            for result in results:
                title = result.find("h5", {'class': 'issue-item__title'})
                authors = result.find("ul", {'aria-label': 'authors'})
                detail = result.find("div", {'class': 'issue-item__detail'})
                doi = result.find("div", {'class': 'issue-item__detail'}).find("a")["href"]
                abstract = result.find("div", {'class': 'issue-item__abstract truncate-text trunc-done'})

                title = re.sub(' +', ' ', re.sub('\n', ' ', title.text.strip()))
                if title == "List of Reviewers":
                    continue
                authors = re.sub('\n', ' ', authors.text.strip())
                detail = detail.text.strip().split("https:")[0] + ", " + vol
                abstract = re.sub(' +', ' ', re.sub('\n', ' ', abstract.text.strip()))
                data = {
                    'paper_id': self.papers_order,
                    'paper_title': title,
                    'authors': authors,
                    'detail': detail,
                    'doi_link': doi,
                    'abstract': abstract
                }
                self.papers_order += 1
                current_issue_papers.append(data)
            print(current_issue_papers)
            next_box = soup.find('a', attrs={'class': 'content-navigation__btn--next'})
            next_issue_url = "https://dlnext.acm.org" + next_box['href']
            return current_issue_papers, next_issue_url
        except IOError:
            return ""

    def store_to_txt(self, current_issue_papers, filename):
        try:
            for paper_info in current_issue_papers:
                paper_id = paper_info['paper_id']
                paper_title = paper_info['paper_title']
                doi_link = paper_info['doi_link']
                authors = paper_info['authors']
                detail = paper_info['detail']
                abstract = paper_info['abstract']
                with open(filename, "a") as f:
                    f.write(
                        "paper%s\nTitle：%s\nAuthors：%s\nDetail：%s\nDoi_link：%s\nAbstract: %s\n"
                        % (paper_id, paper_title, authors, detail, doi_link, abstract))
                    f.write("==========================\n")
        except IOError:
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
        except IOError:
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
        except IOError:
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
