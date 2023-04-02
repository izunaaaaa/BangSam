# BANGSAM - Buy and get special room ( Backend )


<img src="https://user-images.githubusercontent.com/125422608/229361378-60550e62-01e7-4032-8908-4256ea45a3ce.png" width="20%"/>


  **개발기간: 2022.03 ~ 2022.03**

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fizunaaaaa%2F&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## Summary

Django와 Django Rest Framework를 이용하여 부동산 앱에 대한 처리를 수행하는 API 를 제공

## distribution

<img src="https://user-images.githubusercontent.com/125422608/229361962-1a3170fd-debf-4fab-985a-c131656d1a40.png" width="50%"/>

> **Backend** : [https://backend.bangsam.site](https://backend.bangsam.site)<br>
> **Frontend** : [https://bangsam.site](https://bangsam.site)<br>

## Backend 개발 인원


|      김두홍       |         송가연         |                                                                                                                 
| :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: |
|   <img width="160px" src="https://user-images.githubusercontent.com/125422608/229362247-12393ef8-a52c-4835-a933-3dc81c6b5f62.png" />    |<img width="160px" src="https://user-images.githubusercontent.com/125422608/229362286-d467819b-098b-40ab-9941-c0376ad61f94.png" />    |      
|   [@KimDuHong](https://github.com/KimDuHong)   |    [@SongGaYeon](https://github.com/goeasyonng)  | 

## Stacks

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

## Installation
``` bash
$ git clone https://github.com/izunaaaaa/Bangsam
$ cd Bangsam
$ poetry install
$ python manage.py collectstatic --no-input
$ python manage.py makemigrations
$ python manage.py migrate
$ gunicorn config.asgi:application  --worker-class uvicorn.workers.UvicornWorker
```

## DB diagram

![DB](https://user-images.githubusercontent.com/125422608/229363458-002cfa1f-8bc0-41e1-9475-46a8c1e064aa.png)

## API

[API문서](https://backend.bangsam.site/redoc)

## Architecture 

![Service](https://user-images.githubusercontent.com/125422608/229364105-875166ca-c8fe-407b-b81a-f5805cd25be7.png)

