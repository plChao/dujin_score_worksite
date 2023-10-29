ALTER DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
use mydb;

-- actual_exam_situation
-- all_examinee_info
-- article_info
-- exams
-- tan_info

load data local infile '../2024_table/tan_info.csv'
into table tan_info
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines
(@tan_id,@area,@group,@tan_name)
set `tan_id`=@tan_id, `area`=@area, `group`=@group, `tan_name`=@tan_name;

load data local infile '../2024_table/article_info.csv'
into table article_info
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '../2024_table/all_examinee_info.csv'
into table all_examinee_info
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '../2024_table/actual_exam_situation.csv'
into table actual_exam_situation
fields terminated by ','
lines terminated by '\n'
ignore 1 lines
(@article_id,@name,@correctness_minus,@fluency_minus,@final_score,@final_examiner,@score_id,@exam_id)
set `article_id`=@article_id, `name`=@name, `exam_id`=@exam_id;
-- set `article_id`=@article_id, `name`=@name, `exam_id`=@exam_id, `correctness_minus`=@correctness_minus, `fluency_minus`=0, `final_score`=100-@correctness_minus;

load data local infile '../2024_table/exams.csv'
into table exams
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines
(@exam_date,@exam_group,@exam_id)
set `exam_id`=@exam_id,`exam_date`=@exam_date,`exam_group`=@exam_group;