class CarDeal():
	def __init__(self, car_info_dict, car_info_json = None):
		if car_info_dict is None:
			car_info_json = re.sub('(\w+):', '"\g<1>":', car_info_json)
			car_info_json = re.sub(':([^,}]+)(,|})', ':"\g<1>"\g<2>', car_info_json)
			car_info_dict = json.loads(car_info_json)
		if car_info_dict is None:
			return

		self.series_id = long(car_info_dict['series_id'])
		self.sale_name = car_info_dict['sale_name']
		self.card_time = long(car_info_dict['car_time'])
		self.kilometer = long(car_info_dict['kilometer'])
		self.province_id = long(car_info_dict['province_id'])
		self.city_id = None
		if 'city_id' in car_info_dict:
			self.city_id = long(car_info_dict['city_id'])
		self.model_id = None
		if 'model_id' in car_info_dict:
			self.model_id = long(car_info_dict['model_id'])