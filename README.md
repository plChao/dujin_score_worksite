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
## 進入開發環境
```shell
docker-compose up -d
docker exec -it CONTAINER_ID /bin/bash
```
## 架設到 NAS
### 新建
1. 建立專案: 使用 docker-compose_forNASDeploy.yml 作為設定 yml
2. 建立網站入口
3. 如果 django site 的 log 顯示: can not connect to db server
   可能需要重啟 django site 的 docker
### 更新
1. 理論上重啟就會更新(?
2. 沒有更新可能分成
    1. code 沒有更新: 可能是因為 volumn 映射蓋掉
    2. docker 沒有更新: 刪掉 image 再重新 pull 一次
### import data
python manage.py runscript work_cite.import_data -v2
1. article_info 不完正
2. 切割 awards 使其不會不匹配