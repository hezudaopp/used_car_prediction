<?php
$evalParams = array(
			array("series_id" => 379, "sale_name" => "1.6 手自一体 Sporty", "model_year" => 2009, "car_time" => 1272643200, "kilometer" => 47200, "province_id" => 12, "city_id" => 1),
			array("series_id" => 650, "sale_name" => "2.4 手自一体 豪华版", "model_year" => 2012, "car_time" => 1359648000, "kilometer" => 46200, "province_id" => 12, "city_id" => 1),
			array("series_id" => 379, "sale_name" => "1.6 手自一体 舒适版", "model_year" => 2014, "car_time" => 1446307200, "kilometer" => 7000, "province_id" => 12, "city_id" => 1),
			array("series_id" => 503, "sale_name" => "2.0 手自一体 时尚型", "model_year" => 2011, "car_time" => 1328025600, "kilometer" => 36900, "province_id" => 12, "city_id" => 1),
			array("series_id" => 923, "sale_name" => "2.2T 手自一体 两驱锋芒进化版智慧型", "model_year" => 2013, "car_time" => 1380556800, "kilometer" => 80800, "province_id" => 12, "city_id" => 1),
			array("series_id" => 242, "sale_name" => "2.4SIDI 手自一体 雅致版", "model_year" => 2012, "car_time" => 1364745600, "kilometer" => 49800, "province_id" => 12, "city_id" => 1),
			array("series_id" => 376, "sale_name" => "1.4TSI 双离合 技术版", "model_year" => 2010, "car_time" => 1264953600, "kilometer" => 107900, "province_id" => 12, "city_id" => 1),
			array("series_id" => 1164, "sale_name" => "1.6T 手自一体 SL舒适版", "model_year" => 2013, "car_time" => 1388505600, "kilometer" => 41200, "province_id" => 12, "city_id" => 1),
			array("series_id" => 504, "sale_name" => "3.0 手自一体 领先型", "model_year" => 2008, "car_time" => 1212249600, "kilometer" => 90400, "province_id" => 12, "city_id" => 1),
			array("series_id" => 420, "sale_name" => "1.5 手动 标准版", "model_year" => 2009, "car_time" => 1259596800, "kilometer" => 104100, "province_id" => 12, "city_id" => 1),
			array("series_id" => 906, "sale_name" => "1.8 手动 基本型", "model_year" => 2012, "car_time" => 1354291200, "kilometer" => 58700, "province_id" => 12, "city_id" => 1),
			array("series_id" => 400, "sale_name" => "3.6 手自一体 V6 4座加长行政版", "model_year" => 2009, "car_time" => 1280592000, "kilometer" => 59000, "province_id" => 12, "city_id" => 1),
			array("series_id" => 2324, "sale_name" => "1.6 手动 豪华版", "model_year" => 2014, "car_time" => 1406822400, "kilometer" => 61500, "province_id" => 12, "city_id" => 1),
			array("series_id" => 248, "sale_name" => "1.6 手自一体 时尚版", "model_year" => 2012, "car_time" => 1341072000, "kilometer" => 50000, "province_id" => 12, "city_id" => 1),
			array("series_id" => 2023, "sale_name" => "2.0T 双离合 旗舰运动型", "model_year" => 2012, "car_time" => 1354291200, "kilometer" => 90000, "province_id" => 12, "city_id" => 1),
			array("series_id" => 643, "sale_name" => "2.4 自动 VTI-S NAVI尊贵导航版", "model_year" => 2013, "car_time" => 1375286400, "kilometer" => 50000, "province_id" => 12, "city_id" => 1),
			array("series_id" => 105, "sale_name" => "2.5 手自一体 S 舒适版", "model_year" => 2009, "car_time" => 1257004800, "kilometer" => 80000, "province_id" => 12, "city_id" => 1),
			array("series_id" => 15, "sale_name" => "1.6 手自一体 限量版II", "model_year" => 2013, "car_time" => 1412092800, "kilometer" => 14000, "province_id" => 12, "city_id" => 1)
        );

foreach ($evalParams as $evalParam) {
	$args = json_encode($evalParam);
	exec("python main.py " . $args, $array, $ret);
	var_dump($array);
	var_dump($ret);
}

// $args = json_encode($evalParams[3]);
// exec('python main.py ' . $args, $array, $ret);
// print $args;
// var_dump($array);
// var_dump($ret);

// $a = $evalParams[-1];
// if (empty($a)) print 1;

// $curl = curl_init();
// curl_setopt($curl,CURLOPT_URL,"http://open.273.cn/evaluate/price/get");
// curl_setopt($curl,CURLOPT_POST,true); 
// curl_setopt($curl,CURLOPT_POSTFIELDS,$evalParams);
// curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
// $return = curl_exec($curl);
// curl_close($curl);
// var_dump(json_decode($return, true));
// var_dump(json_decode(false));
?>