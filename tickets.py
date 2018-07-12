#-*- coding:utf-8 -*-
"""Train tickets query via CLI

Usage:
    tickets [-dgktz] <from> <to> <date>

Options:
    -h,--help       Show this screen.
    -d              动 车
    -g              高 铁
    -k              快 速
    -t              特 快
    -z              直 达

"""

import requests
import stations
from docopt import docopt
from prettytable import PrettyTable

def cli():
	arguments = docopt(__doc__, version='tickets 1.0')
	from_station = stations.get_telecode(arguments.get('<from>'))
	to_station = stations.get_telecode(arguments.get('<to>'))
	date = arguments.get('<date>')
	options = ''.join([key for key,value in arguments.items() if value is True])
	url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
	       'leftTicketDTO.train_date={}&'
		   'leftTicketDTO.from_station={}&'
		   'leftTicketDTO.to_station={}&'
		   'purpose_codes=ADULT').format(date, from_station, to_station)

	r = requests.get(url, verify=False)
    #print(arguments)
	#print(r.text)
	raw_trains = r.json()['data']['result']
	#print(trains)
	pt = PrettyTable()
	pt._set_field_names('车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split())
	for raw_trains in raw_trains:
		data_list = raw_trains.split('|')
		#print(data_list[2])
		train_no = data_list[3]
		initial = train_no[0].lower()
		if not options or initial in options:
			from_station_code = data_list[6]
			to_station_code = data_list[7]
			from_station_name = ''
			to_station_name = ''
			start_time = data_list[8]
			arrive_time = data_list[9]
			time_duration = data_list[10]
			first_class_seat = data_list[31] or "--"
			secong_class_seat = data_list[30] or "--"
			soft_sleep = data_list[23] or "--"
			hard_sleep = data_list[28] or "--"
			hard_seat = data_list[29] or "--"
			no_seat = data_list[33] or "--"
			pt.add_row([
				train_no, 
				'\n'.join([stations.get_name(from_station_code), stations.get_name(to_station_code)]),
				'\n'.join([start_time, arrive_time]),
				time_duration,
				first_class_seat,
				secong_class_seat,
				soft_sleep,
				hard_sleep,
				hard_seat,
				no_seat
			])
			
	print(pt)
			


if __name__ == '__main__':
    cli()
