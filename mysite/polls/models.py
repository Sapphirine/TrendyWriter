from django.db import models

# Create your models here.
'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
'''

class WordDigest(models.Model):
	word_text = models.CharField(max_length=30)
	word_count = models.IntegerField(default=0)
	retrive_date = models.DateTimeField('date of counting')

	def __str__(self):              # __unicode__ on Python 2
		return self.word_text