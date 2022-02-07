# window 기준

## 1.로컬에서 서버 실행   
0. 경로 설정

    해당 window_venv가 있는 파일 위치와 같은 경로에서 실행한다(bside>)

    

1. 가상환경 설정

     python -m venv inbeom_venv 

     (inbeom 을 각자 이름으로 하시면 될 것 같습니다. 가상환경이 상대경로에서 되기 때문에 각각 컴퓨터에서 따로 하셔야 됩니다.)

   

2. 가상환경 접속

     1.window os 환경 -> inbeom_venv\Scripts\activate

     2.linux os 환경 -> source inbeom_venv\bin\activate  

  

3. 라이브러리 설치

     정상적으로 가상환경에 접속될시 오른쪽과 같이 괄호안에 가상환경 이름이 나오게 됩니다. 그 후 라이브러리를 설치 하면 됩니다.

     (inbeom_venv)bside> cd backend

     (inbeom_venv)bside/backend> pip install -r requirements.txt

     (inbeom_venv)bside/backend> pip install django-cors-headers

   

4. 서버 실행

     (inbeom_venv)bside/backend>cd mysite

     (inbeom_venv)bside/backend/mysite> python manage.py runserver

   

## 2.웹페이지 접속
두개의 프로그램이 정상적으로 돌아가면 인터넷창에    
121.0.0.1 :8000 - django 페이지 입니다.