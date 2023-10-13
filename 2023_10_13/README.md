### A단계
A단계는 기초적인 base.html 공통 부모 템플릿을 상속받아 사용하는 문제로 어려움이 없었습니다.

### B단계
키워드를 추가 및 삭제 하는 문제로 폼을 사용해서 해결했습니다.

### C단계
def get_google_data(keywords):
        # 가져올 웹 페이지 url
        url = f'https://www.google.com/search?q={keywords}&tbs=qdr:y'

        driver = webdriver.Chrome()
        driver.get(url)

        # 열린 페이지 소스를 받아옴
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 검색 결과 가져오기
        # div 태그 안의 id 가 result-stats 라는 요소
        result_stats = soup.select_one("div#result-stats")
        # print(result_stats.text)
        temp = result_stats.text[7:-10].replace(',','')
        return int(temp)
위의 함수를 이용하여 크롬 검색 결과 페이지 크롤링을 수행했습니다. return 으로 검색 결과 개수를 return 하는데 Trend.objects.get_or_create를 사용하는 점에 어려움을 겪었습니다. 부가적으로 이미 저장되어 있는 키워드라면 새로 생성하지 않고 검색 결과 개수를 변경하는 것 또한 시간이 걸렸습니다.

### D단계
히스토그램은 지난 관통 pjt에서 배운 
import base64
from io import BytesIO
라이브러리를 이용하여 작성하였습니다.


### E단계
지난 1년을 기준으로 필터링하여 크롤링을 수행합니다.
&tbs=qdr:y'
검색 기간을 설정하여, 크롤링 조건을 설정하여 1년을 기준으로 크롤링 했습니다.





