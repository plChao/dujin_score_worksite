# dujin_score_worksite
## 成員 email
|名字|gmail|
|-|-|
|石昀翰|yunhans523@gmail.com|
|趙秉濂|plchao0415@gmail.com|
|施雅青|syc891017@gmail.com|
## 主旨
1. 架設 website 供讀經會考評分使用
## 匯入資料
1. 下載道親報名表
```
$ cd data_clean
$ python exam_situation_forT_ching.py
$ python set_article_id_forT_ching.py
```
1. 下載報名表-讀經班報名
```
$ python exam_situation_forR_plchao.py
$ python set_article_id_forR_plchao.py
``` 
## 架設環境步驟
```shell
docker-compose up -d
```
## 製作開發環境
```shell
docker build -t my_django_dev .
docker run -it --rm -v ${pwd}:/codeForDev/ my_django_dev bash # For windows
```