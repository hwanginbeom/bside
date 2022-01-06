# window 기준

## 1.서버 실행   
cmd 창을 두개 켜신후에   
1번 cmd 창 - \bside>django-react-venv\Scripts\activate - 가상환경 접속   
1번 cmd 창 - \bside>cd backend   
1번 cmd 창 - \bside\backend>  python manage.py runserver   
2번 cmd 창 - \bside>django-react-venv\Scripts\activate - 가상환경 접속   
2번 cmd 창 - \bside>cd frontend   
2번 cmd 창 - \bside\frontend>yarn start   

- 리눅스는 아마도 가상환경 접속할때 source django-react-venv\Scripts\activate 이런 방식인걸로 알고 있슴다.   

## 2.웹페이지 접속
두개의 프로그램이 정상적으로 돌아가면 인터넷창에    
121.0.0.1 :8000 - django 페이지 입니다.   
121.0.0.1 :3000 - react 페이지 입니다.   
이렇게 창을 두개 키시고 테스트 해보시면 됩니다   
