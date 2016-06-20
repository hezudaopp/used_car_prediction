select count(*), site from car_allnet_source group by site;
-- +----------+---------+
-- | count(*) | site    |
-- +----------+---------+
-- |  4655531 | 58      |
-- |   801207 | baixing |
-- |   328123 | che168  |
-- |  1815301 | ganji   |
-- |   886643 | huaxia  |
-- |   199939 | taoche  |
-- +----------+---------+

SELECT (@rowNum:=@rowNum+1) as rowNum, `id`, `series`, `series_id`, `title`, `model`, `model_id`
FROM `car_allnet_source` a, (Select (@rowNum :=-1) ) b
WHERE 1 AND `series_id` > 0
LIMIT 0, 100;


select * from car_allnet_source where site = '58';

UPDATE wcar.car_allnet_source a, car_type.car_brand b
SET a.brand_id = b.id
WHERE a.brand = b.name;

UPDATE wcar.car_allnet_source a, car_type.car_series b
SET a.series_id = b.id
WHERE a.brand_id = b.brand_id AND a.series = b.name;


UPDATE wcar.car_allnet_source a
			INNER JOIN
				(SELECT a.id,b.id AS brand_id
				FROM wcar.car_allnet_source a, car_type.car_brand b
				WHERE a.create_time < 1443060120 AND (a.brand = b.name OR a.brand = b.liyang_name) 
				LIMIT 0, 100000) b
			ON a.id = b.id
			SET a.brand_id = b.brand_id;