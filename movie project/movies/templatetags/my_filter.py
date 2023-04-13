from django import template

# {{ | ~ }} 수정하기

register =template.Library()      #함수명 변경시 사용
# 탬플릿에서
# {{ variable|filter_name }}

@register.filter
def myupper(val):  #위의 variable부분을 val로 받아온다. 장고가 제공해준다
    return val+'필터 함수가 실행됨'         # filter_name의 기능이 정의 된다.
