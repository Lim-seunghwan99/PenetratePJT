from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django import forms

# model 선택 3가지 방법
# 1. 직접 가져오기  --> 권장 x
# from .models import User 

# 2. settings에 설정된 모델 가져오기
# from django.conf import settings

# -> 문자열, models.py에 작성할 때는 문자열이 좋다,
# 3.get_user_model 메서드 활용
from django.contrib.auth import get_user_model


class CustomuserCreationForm(UserCreationForm):
    VIPCode = forms.CharField(max_length=8)
    
    # VIP 코드 검증 로직을 clean_VIPCode 메서드에 추가
    def clean_VIPCode(self):
        vip_code = self.cleaned_data.get('VIPCode')
        if vip_code != '01150731':
            raise forms.ValidationError("올바른 VIP 코드를 입력해주세요.")
        return vip_code
    
    # class Meta:
    #     model = get_user_model()
    #     fields = UserCreationForm.Meta.fields

    class Meta(UserCreationForm.Meta):
        model = get_user_model()