회원제 게시판을 구현하면서 django를 배웟던 것을 복습할 수 있어 좋았습니다. 
Board, Comment, User를 Admin site에 등록하고, Model 폼 만들기, 프로필 페이지, 유저 팔로우 기능, 게시글 좋아요 기능을 추가 하는 것을 복습했습니다. 또한 부가적으로 웹 페이지에 배경 사진 꾸미기, button ui 변경, 특정 코드를 알고 있는 사람만 회원 가입할 수 있게 회원 가입 모델 또한 변경했습니다
    
VIP 코드 검증 로직을 clean_VIPCode 메서드에 추가
VIPCode = forms.CharField(max_length=8)
def clean_VIPCode(self):
    vip_code = self.cleaned_data.get('VIPCode')
    if vip_code != '01150731':
    raise forms.ValidationError("올바른 VIP 코드를 입력해주세요.")
    return vip_code

Creation Form 또한 클래스이기 때문에 위와 같이 Creation Form내에 함수를 정의하면 메서드로써 활용할 수 있다는 사실을 알게 되었고 이를 통해서 특정 코드를 검사하고 에러 문구를 저희가 지정해서 보여줄 수 있다는 사실 또한 알게 되었습니다.

follow기능을 내 프로필 보기가 아닌 게시글에서 바로 팔로우를 구현했습니다 이 경우, detail에 필요한 board_pk를 url, view에서 설정해서 넘겨야 한다는 사실을 새로 알게 되었습니다.

