from django.db import models
import json

# Create your models here.

class opinion_list(models.Model):
	text = models.TextField()
	value = models.FloatField()
	record_time = models.DateTimeField()
	student_id = models.CharField(max_length = 100)
	record_time_stamp = models.CharField(max_length = 20)

	def __str__(self):
		return json.dumps({'text':self.text,'value':self.value,'record_time':self.record_time.strftime('%Y-%m-%d %H:%M'),'student_id':self.student_id,'record_time_stamp':self.record_time_stamp})
	def get_as_dict(self):
		return {'text':self.text,'value':self.value,'record_time':self.record_time.strftime('%Y-%m-%d %H:%M'),'student_id':self.student_id,'record_time_stamp':self.record_time_stamp}
	
class student_info(models.Model):
	student_id = models.CharField(max_length = 100)
	student_email_id = models.EmailField()
	student_name = models.CharField(max_length = 100)

	def __str__(self):
		return json.dumps({'student_id':self.student_id,'student_email_id':self.student_email_id,'student_name':self.student_name})
