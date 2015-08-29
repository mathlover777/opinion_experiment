from django.shortcuts import render
from django.http import HttpResponse
from models import opinion_list,student_info
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.utils.dateformat import format

import pprint

ID_FILE = 'idlist.json'
GRAPH_FILE = 'graph.json'


def load_json(filename):
	with open(filename,'rb') as fp:
		return json.load(fp = fp)

def save_json(filename,data):
	with open(filename,'wb') as fp:
		json.dump(data,fp = fp,indent = 4)
	return

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_params(request,param_list):
	# <(param_name,default value if unable to extract)>
	params = {}
	for param in param_list:
		param_name = param[0]
		param_default = param[1]
		if(param_name in request.POST and len(request.POST[param_name])> 0):
			params[param_name] = get_clean_string(request.POST[param_name])
		elif (param_default is not None):
			params[param_name] = get_clean_string(param_default)
		else:
			raise Exception('all fields required NULL given !{' + param_name + '}') 
	return params

def get_error_json(error_text):
	return_object = {}
	return_object['success'] = 'false'
	return_object['msg'] = 'Exception : ' + error_text
	return json.dumps(return_object,indent = 4)

def get_clean_string(dirty_string):
	return str.rstrip(dirty_string.encode('ascii','ignore'))

@csrf_exempt
def add_student(request):
	try:
		param_dict = get_params(request,[('student_id',None),('student_email_id',None),('student_name',None)])
		student_id = param_dict['student_id'].lower()
		student_email_id = param_dict['student_email_id']
		student_name = param_dict['student_name']
		student = student_info(student_id = student_id,student_email_id = student_email_id,student_name = student_name)
		print student
		student.save()
		return_object = {}
		return_object['status'] = 'success'
		return HttpResponse(json.dumps(return_object,indent = 4))
	except Exception as e:
		print str(e)
		return HttpResponse(get_error_json(str(e)))

@csrf_exempt
def add_opinion(request):
	try:
		param_dict = get_params(request,[('text',None),('value',None),('record_time',''),('student_id',None)])
		# pprint.pprint(param_dict)
		text = param_dict['text']
		value = float(param_dict['value'])
		student_id = param_dict['student_id'].lower()
		record_time = timezone.localtime(timezone.now())
		record_time_stamp = int(format(record_time, 'U'))
		opinion = opinion_list(text = text,value = value,student_id = student_id,record_time = record_time,record_time_stamp = record_time_stamp)
		opinion.save()

		return_object = {}
		return_object['status'] = 'success'
		return HttpResponse(json.dumps(return_object,indent = 4))
	except Exception as e:
		return HttpResponse(get_error_json(str(e)))

def get_student_id_set(student_id,student_id_list):
	if student_id == '' and student_id_list == '':
			raise Exception('Both student_id and student_id_list missing !')
	if student_id != '':
		return set(get_neighbor_list(student_id))
	return set(student_id_list.split(';'))	

@csrf_exempt
def get_top_opinion_list(request):
	try:
		param_dict = get_params(request,[('student_id_list',''),('top_count','2'),('student_id','')])
		student_id = param_dict['student_id'].lower()
		student_id_list = param_dict['student_id_list'].lower()
		
		student_id_set = get_student_id_set(student_id,student_id_list)

		top_count = int(param_dict['top_count'])
		opinion_set = filter(lambda x: x.student_id in student_id_set,opinion_list.objects.all())
		sorted_by_time_opinion_list = sorted(opinion_set,reverse = True,key = lambda x:int(format(x.record_time, 'U')))

		opinions_to_return = min(top_count,len(sorted_by_time_opinion_list))

		return_object = {}
		return_object['status'] = 'success'
		if opinions_to_return < 1:
			return_object['msg'] = 'no opinions found'
			return return_object
		top_opinion_list = sorted_by_time_opinion_list[0:opinions_to_return]
		opinion_json = json.dumps([json.dumps(x.get_as_dict()) for x in top_opinion_list])
		return_object['top_opinion_list'] = opinion_json
		return HttpResponse(json.dumps(return_object,indent = 4))
	except Exception as e:
		return HttpResponse(get_error_json(str(e)))

@csrf_exempt
def get_latest_opinion(request):
	try:
		param_dict = get_params(request,[('top_count','2')])
		top_count = int(param_dict['top_count'])
		opinion_set = opinion_list.objects.all()
		sorted_by_time_opinion_list = sorted(opinion_set,reverse = True,key = lambda x:int(format(x.record_time, 'U')))

		opinions_to_return = min(top_count,len(sorted_by_time_opinion_list))

		return_object = {}
		return_object['status'] = 'success'
		if opinions_to_return < 1:
			return_object['msg'] = 'no opinions found'
			return return_object
		top_opinion_list = sorted_by_time_opinion_list[0:opinions_to_return]
		opinion_json = json.dumps([json.dumps(x.get_as_dict()) for x in top_opinion_list])
		return_object['top_opinion_list'] = opinion_json
		return HttpResponse(json.dumps(return_object,indent = 4))
	except Exception as e:
		return HttpResponse(get_error_json(str(e)))

def get_neighbor_list(student_id):
	graph = load_json(GRAPH_FILE)
	if student_id in graph:
		if len(graph[student_id]) > 0:
			node_list = [None] * len(graph[student_id]) 
			i = 0
			for node in graph[student_id]:
				node_list[i] = node
				i += 1
			return node_list
	return []

@csrf_exempt
def get_neighbors_with_influece_values(request):
	try:
		param_dict = get_params(request,[('student_id',None)])
		student_id = param_dict['student_id'].lower()
		neighbor_list = {}
		graph = load_json(GRAPH_FILE)
		if student_id in graph:
			local_adjacency = graph[student_id];
			for node in local_adjacency:
				neighbor_list[node] = local_adjacency[node]
		return_object = {}
		return_object['neighbor_list'] = json.dumps(neighbor_list)
		return_object['success'] = 'true'
		return HttpResponse(json.dumps(return_object,indent = 4))
	except Exception as e:
		return HttpResponse(get_error_json(str(e)))	