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
1. 安裝 docker
```
$ docker -v
// 測試安裝成功
// Docker version 20.10.14, build a224086
```
3. 下載 [docker images](https://drive.google.com/file/d/18qb9hOHK8lb4DNeoTxx-tQfXRx7NPJVy/view?usp=drive_link)
4. 執行以下 command
```cpp
$ docker load -i .\website.tar
$ docker images
// REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
// <none>       <none>    af16f511733c   19 hours ago   2.09GB
$  docker run -d -p 34567:22 -p 8000:8000 -v D:\Documents\1_讀經會考\unix:/home/unix af16f511733c
// docker run -it -p 34567:22 -p 8000:8000 -v D:\Documents\1_讀經會考\unix:/home/unix af16f511733c
```
## 跑 django server
1. 將此 repository clone 到分享的資料夾中 ( git clone ... )
2. ssh 進入 docker container
```cpp
$ ssh unix@127.0.0.1 -p 34567
```
3. 在 docker container 開始 mysql
```
$ sudo service mysql start
```
4. 在 docker container 進入目標資料夾
```cpp
$ cd dujin_score_worksite/score_site/
$ python3 manage.py runserver 0.0.0.0:8000
```
4. 在本機瀏覽器測試 127.0.0.1:8000
