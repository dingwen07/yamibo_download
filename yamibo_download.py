import requests
from bs4 import BeautifulSoup
import os

class NovelDownloader:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.chapter_list = []

    def fetch_chapter_list(self):
        response = self.session.get(self.url)
        # response.encoding = 'gbk'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        chapter_list_a = soup.find_all('div', class_='list-view-inline')[0].find_all('a')
        for a in chapter_list_a:
            url = a.get('href')
            title = a.get_text()
            self.chapter_list.append(url)
    
    def fetch_all(self, save=False, save_path=None):
        novel_content = []
        do_save = False
        if save != None and save_path != None:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            do_save = True
        for url in self.chapter_list:
            chapter = NovelDownloader.fetch_chapter(url)
            print(chapter[0])
            novel_content.append((chapter[0], chapter[1]))
            if do_save:
                with open(os.path.join(save_path, chapter[0] + '.txt'), 'w', encoding='utf-8') as f:
                    f.write(chapter[1])
        return novel_content

    def fetch_all_md(self, file='novel.md', title='Novel'):
        basename = os.path.basename(file)
        if not os.path.exists(basename):
            os.makedirs(basename)
        novel_content = self.fetch_all(save=False)
        markdown = '# ' + title + '\n'
        for title, content in novel_content:
            markdown += '## {}\n'.format(title)
            markdown += content + '\n\n'
        with open(file, 'w', encoding='utf-8') as f:
            f.write(markdown)

    @staticmethod
    def fetch_chapter(url, hostname='www.yamibo.com'):
        if not hostname in url:
            url = 'https://' + hostname + '/' + url
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find(id='w0-collapse1').find_all('div', class_='panel-body')[0].find_all('p')
        content = ''
        for paragraph in paragraphs:
            content += paragraph.get_text().strip() + '\n'
        title = soup.find_all('li', class_='active')[0].get_text()
        return title, content


if __name__ == '__main__':
    url = 'https://www.yamibo.com/novel/264730'
    novel_downloader = NovelDownloader(url)
    novel_downloader.fetch_chapter_list()
    # print(novel_downloader.chapter_list)
    # print(NovelDownloader.fetch_chapter('https://www.yamibo.com/novel/view-chapter?id=38793297')[0])
    # print(NovelDownloader.fetch_novel_content(novel_downloader.chapter_list[0][1]))
    # novel_downloader.fetch_all(save=True, save_path='novels/264730/')
    novel_downloader.fetch_all_md(file='novels/264730.md', title='Novel')
