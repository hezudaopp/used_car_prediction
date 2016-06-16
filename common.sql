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


select * from car_allnet_source where site = '58';

UPDATE wcar.car_allnet_source a, car_type.car_brand b
SET a.brand_id = b.id
WHERE a.create_time < 1443060120 AND (a.brand = b.name OR a.brand = b.liyang_name);

UPDATE wcar.car_allnet_source a, car_type.car_series b
SET a.series = b.id
WHERE a.create_time < 1443060120 AND a.brand_id = b.brand_id AND (a.series = b.name OR a.series = b.liyang_name);