# [BACKEND] BANGSAM_Buy and get special room 


<img src="https://user-images.githubusercontent.com/125422608/229361378-60550e62-01e7-4032-8908-4256ea45a3ce.png" width="20%"/>


  **개발기간: 2022.03 ~ 2022.03**

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fizunaaaaa%2F&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## SUMMARY

Django와 Django Rest Framework를 이용하여 부동산 앱에 대한 처리를 수행하는 API 를 제공

## DISTRIBUTION

<img src="https://user-images.githubusercontent.com/125422608/229361962-1a3170fd-debf-4fab-985a-c131656d1a40.png" width="50%"/>

> **Backend** : [https://backend.bangsam.site](https://backend.bangsam.site)<br>
> **Frontend** : [https://bangsam.site](https://bangsam.site)<br>

## 개발 인원


|      김두홍       |         송가연         |                                                                                                                 
| :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: |
|   <img width="160px" src="https://user-images.githubusercontent.com/125422608/229362247-12393ef8-a52c-4835-a933-3dc81c6b5f62.png" />    |<img width="160px" src="https://user-images.githubusercontent.com/125422608/229362286-d467819b-098b-40ab-9941-c0376ad61f94.png" />    |      
|   [@KimDuHong](https://github.com/KimDuHong)   |    [@SongGaYeon](https://github.com/goeasyonng)  | 

## STACKS

### Environment

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)     

### Hosting

![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=Render&logoColor=white)

### Dev Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=Poetry&logoColor=white)

### Library

![DjanoRestFramework](https://img.shields.io/badge/DRF-F44336?style=for-the-badge&logo=DRF&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=Gunicorn&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-46E3B7?style=for-the-badge&logo=Uvicorn&logoColor=white)
![DJANGOCHANNELS](https://img.shields.io/badge/DJANGOCHANNELS-092E20?style=for-the-badge&logo=DJANGOCHANNELS&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)
![Sentry](https://img.shields.io/badge/Sentry-362D59?style=for-the-badge&logo=Sentry&logoColor=white)


### Communication
![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white)

## INSTALLATION
``` bash
$ git clone https://github.com/izunaaaaa/Bangsam
$ cd Bangsam
$ poetry install
$ python manage.py collectstatic --no-input
$ python manage.py makemigrations
$ python manage.py migrate
$ gunicorn config.asgi:application  --worker-class uvicorn.workers.UvicornWorker
```

## DB DIAGRAM

![DB](https://user-images.githubusercontent.com/125422608/229363458-002cfa1f-8bc0-41e1-9475-46a8c1e064aa.png)

## API

[API문서](https://backend.bangsam.site/redoc)

## ARCHITECTURE 

![Service](https://user-images.githubusercontent.com/125422608/229364197-ae61c499-fb22-420c-9674-36d843cafcc2.png)

## MAIN FUNCTION 

### 부동산 매물 조회, 삭제, 수정, 생성
- 조회 시 Param 값으로 filtering 가능

### python manage.py seed_data (--total 10) 옵션으로 더미 데이터 생성 가능
``` bash
$  python manage.py seed_data --total 10
$ # 각 동 별로 10개씩 방 생성, 구와 동의 데이터가 DB 에 없다면 새로 생성 ( 서울시내 모든 구 / 동 데이터 )
```

### 조회수별, 좋아요별 Top10 조회
- 로그인 한 유저만 지원

### 채팅
- 유저와 공인중개사의 다이렉트 채팅 가능
- websocket ( django channels 활용 )
- 1:1 채팅 시 읽지않은 메세지 수, 채팅방의 마지막 메세지 업데이트
- 채팅방의 유효기간 3개월, 3개월 이후 자동삭제
- 각 채팅방의 채팅로그는 100개만 저장


