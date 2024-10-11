import requests
from bs4 import BeautifulSoup

package_name = []
package = "lodash.set"
j = 1  # 패키지 번호 초기화
for i in range(9):
    res = requests.get('https://www.npmjs.com/browse/depended/%s?offset=%d'%(package,36*i))
    soup = BeautifulSoup(res.content, 'html.parser')

    # 모든 패키지 리스트 아이템을 찾음
    package_items = soup.find_all('li', class_='_2309b204')
    for item in package_items:
        package_num = j  # 현재 패키지 번호 설정
        name = item.find('h3', class_='db7ee1ac').text.strip()
        package_name += name
        publisher = item.find('a', class_='e98ba1cc').text.strip()
        published_info = item.find('span', class_='_66c2abad').text.strip()
        
        # print(f'Package Number: {package_num}')  # 패키지 번호 출력
        # j += 1  # 다음 패키지를 위해 번호 증가
        
        # print(f'Package: {name}')
        # print(f'Publisher: {publisher}')
        # print(f'Published Info: {published_info}')
        # print('-' * 80)
