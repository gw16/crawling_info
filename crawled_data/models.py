from django.db import models

# Create your models here.
class Thinkyou(models.Model):
    title = models.TextField(db_column='제목', max_length=300, primary_key = True)
    start = models.TextField(db_column='공지일', max_length=20)
    end = models.TextField(db_column='마감일', max_length=20)
    dday = models.TextField(db_column='날짜', max_length=20)
    specific_id = models.TextField(db_column='기관', max_length=15)
    link = models.TextField(db_column='링크')
    '''
    category = models.TextField(db_column='분류')
    qualification = models.TextField(db_column='대학(원)생')
    '''

    class Meta:
        db_table = 'Thinkyou'

    def __str__(self):
        return self.title

