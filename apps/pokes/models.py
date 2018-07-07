from django.db import models

class User(models.Model):
	name = models.TextField(blank=False, max_length=20, null=True)
	alias = models.TextField(blank=False, max_length=20,null=True)
	email = models.TextField(blank=False, max_length=20,null=True)
	password = models.TextField(blank=False, max_length=20,null=True)
	confirm = models.TextField(blank=False, max_length=20,null=True)
	dob = models.DateField(auto_now_add=True)
	created_at = models.DateField(null=True)
	updated_at = models.DateField(null=True)
	class Meta:
		db_table = 'user'

class Poke(models.Model):
	poker = models.ForeignKey(User, related_name="poker_pks")
	poked = models.ForeignKey(User, related_name="poked_pks")
	created_at = models.DateField(null=True)
	counter = models.IntegerField(blank=False, default=0, null=True)
	total = models.IntegerField(blank=False, default=0, null=True)
	class Meta:
		db_table = 'poke'