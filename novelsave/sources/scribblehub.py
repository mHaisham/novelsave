from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from .source import Source
from ..models import Chapter, Novel


class ScribbleHub(Source):
    base = 'https://www.scribblehub.com/'

    @staticmethod
    def of(url: str) -> bool:
        return url[:len(ScribbleHub.base)] == ScribbleHub.base

    def novel(self, url: str) -> Tuple[Novel, List[Chapter]]:
        soup = self.soup(url)

        synopsis_paragraphs = [element.text for element in soup.find('div', {'class': 'wi_fic_desc'}).find_all('p')]

        novel = Novel(
            title=soup.find('div', {'class': 'fic_title'}).text.strip(),
            author=soup.find('span', {'class': 'auth_name_fic'}).text.strip(),
            synopsis='\n'.join(synopsis_paragraphs),
            thumbnail=soup.find('div', {'class': 'fic_image'}).find('img')['src'],
            url=url
        )

        id = int(url.split('/')[4])
        max_page = int(soup.find('ul', id='pagination-mesh-toc').find_all('li')[-2].text)

        chapters = []
        for page in range(1, max_page + 1):
            chapters.extend(self.toc(id, page))

        return novel, chapters

    def toc(self, id: int, page: int) -> List[Chapter]:

        response = requests.post(
            'https://www.scribblehub.com/wp-admin/admin-ajax.php',
            data={
                'action': 'wi_getreleases_pagination',
                'pagenum': page,
                'mypostid': id
            }
        )

        soup = BeautifulSoup(response.content, 'lxml')
        chapter_elements = soup.find('ol', {'class': 'toc_ol'}).children

        chapters = []
        for element in chapter_elements:
            a = element.find('a')

            chapter = Chapter(
                no=element['order'],
                title=a.text.strip(),
                url=a['href']
            )

            chapters.append(chapter)

        return chapters