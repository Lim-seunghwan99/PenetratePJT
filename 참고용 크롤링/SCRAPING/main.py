import requests
import bs4

# 현재 백준에 제출 현황을 스크래핑...!

cookies = {}
headers = {
    # 크롬 브라우저라 안내를 해줄 수 있는 메시지
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

response = requests.get('https://www.acmicpc.net/status',
                        cookie=cookies, header=headers)


# HTML파싱을 위해 beautifulsoup4 라이브러리를 사용
soup = bs4.BeautifulSoup(response.text , 'html.parser')

# 테이블을 파싱!
table = soup.select_one('#status-table')

# 테이블의 헤더들 출력
headers = table.find_all('th')
for header in headers:
    print(header.text, end=', ')
print()

rows = table.find_all('tr')
# rows = table.select('tr')  # select를 사용하는 방법 또한 위의 find_all과 같다
for row in rows:
    tds = row.find_all('td')
    for td in tds:
        print(td.text, end=', ')
    print()
