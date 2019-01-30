# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'option', max_length=10, verbose_name='type', choices=[(b'option', 'Selection'), (b'options', 'Multi Selection')])),
                ('value', models.FloatField(default=0.0, verbose_name='value')),
                ('text_value', models.CharField(max_length=255, null=True, verbose_name='Text value', blank=True)),
                ('resolved', models.BooleanField(default=False, verbose_name='resolved')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='create date', null=True)),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
            },
        ),
        migrations.CreateModel(
            name='Demographics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_birth', models.DateField(verbose_name='date birth')),
                ('gender', models.CharField(default=b'F', max_length=1, verbose_name='gender', choices=[(b'F', 'Femenino'), (b'M', 'Masculino')])),
                ('health_insurance', models.BooleanField(default=False, verbose_name='health insurance')),
                ('EPS', models.CharField(max_length=200, null=True, verbose_name='EPS', blank=True)),
                ('country', django_countries.fields.CountryField(default=b'CO', max_length=2, verbose_name='country')),
                ('neighborhood', models.CharField(max_length=200, verbose_name='neighborhood')),
                ('sector', models.CharField(max_length=200, verbose_name='sector')),
                ('child_vaccination_card', models.BooleanField(default=False, verbose_name='child vaccination card')),
                ('child_name', models.CharField(max_length=200, verbose_name='child name')),
                ('education_level', models.CharField(default=b'1', max_length=1, verbose_name='education level', choices=[(b'1', 'Primaria'), (b'2', 'Secundaria'), (b'3', 'Tecnica'), (b'4', 'Tecnologa')])),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='create date', null=True)),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
            ],
            options={
                'verbose_name': 'demographics',
                'verbose_name_plural': 'demographics',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option_text', models.CharField(max_length=200, verbose_name='option text', blank=True)),
                ('value', models.FloatField(default=0.0, verbose_name='value', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='create date', null=True)),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
            ],
            options={
                'ordering': ['option_text'],
                'verbose_name': 'option',
                'verbose_name_plural': 'options',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='create date', null=True)),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
                ('Group', models.ForeignKey(verbose_name='group', to='auth.Group')),
            ],
            options={
                'verbose_name': 'poll',
                'verbose_name_plural': 'polls',
            },
        ),
        migrations.CreateModel(
            name='PollDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(verbose_name='start date')),
                ('end_date', models.DateField(verbose_name='end date')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('poll', models.ForeignKey(verbose_name='poll', to='poll.Poll')),
            ],
            options={
                'ordering': ['start_date'],
                'verbose_name': 'poll date',
                'verbose_name_plural': 'poll dates',
            },
        ),
        migrations.CreateModel(
            name='PollDatePracticeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0.0, verbose_name='average score')),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
                ('poll_date', models.ForeignKey(verbose_name='poll date', to='poll.PollDate')),
            ],
        ),
        migrations.CreateModel(
            name='PollDateQuestionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0.0, verbose_name='average score')),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
                ('poll_date', models.ForeignKey(verbose_name='poll date', to='poll.PollDate')),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('short_name', models.CharField(max_length=10, null=True, verbose_name='short name')),
                ('description', models.TextField(verbose_name='description')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='create date', null=True)),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
            ],
            options={
                'verbose_name': 'practice',
                'verbose_name_plural': 'practices',
            },
        ),
        migrations.CreateModel(
            name='PracticeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(verbose_name='score')),
                ('poll', models.ForeignKey(verbose_name='poll', to='poll.PollDate')),
                ('practice', models.ForeignKey(verbose_name='practice', to='poll.Practice')),
            ],
            options={
                'verbose_name': 'practice score',
                'verbose_name_plural': 'practice scores',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_question_text', models.TextField(verbose_name='original question text')),
                ('question_text', models.TextField(verbose_name='question text')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('type', models.CharField(default=b'option', max_length=10, verbose_name='type', choices=[(b'option', 'Selection'), (b'options', 'Multi Selection')])),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='create date', null=True)),
                ('last_modified', models.DateField(auto_now=True, verbose_name='last-modified', null=True)),
                ('practice', models.ForeignKey(verbose_name='practice', to='poll.Practice', null=True)),
            ],
            options={
                'ordering': ['question_text'],
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identification_number', models.IntegerField(unique=True, null=True, verbose_name='identification number', db_index=True)),
                ('user', models.OneToOneField(verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'respondent',
                'verbose_name_plural': 'respondents',
            },
        ),
        migrations.CreateModel(
            name='RespondentPollDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('completed', models.FloatField(default=0.0, verbose_name='completed', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('poll_score', models.FloatField(default=0.0, verbose_name='poll score')),
                ('poll', models.ForeignKey(verbose_name='poll', to='poll.PollDate')),
                ('respondent', models.ForeignKey(verbose_name='respondent', to='poll.Respondent')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'poll date',
                'verbose_name_plural': 'poll dates',
            },
        ),
        migrations.AddField(
            model_name='practicescore',
            name='respondent',
            field=models.ForeignKey(verbose_name='respondent', to='poll.Respondent'),
        ),
        migrations.AddField(
            model_name='polldatequestionscore',
            name='question',
            field=models.ForeignKey(verbose_name='question', to='poll.Question'),
        ),
        migrations.AddField(
            model_name='polldatepracticescore',
            name='practice',
            field=models.ForeignKey(verbose_name='practice', to='poll.Practice'),
        ),
        migrations.AddField(
            model_name='poll',
            name='questions',
            field=models.ManyToManyField(to='poll.Question', verbose_name='questions'),
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(verbose_name='question', to='poll.Question'),
        ),
        migrations.AddField(
            model_name='demographics',
            name='respondent',
            field=models.OneToOneField(null=True, verbose_name='respondent', to='poll.Respondent'),
        ),
        migrations.AddField(
            model_name='answer',
            name='option',
            field=models.ForeignKey(verbose_name='option', to='poll.Option', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='options',
            field=models.ManyToManyField(related_name='options', verbose_name='options', to='poll.Option'),
        ),
        migrations.AddField(
            model_name='answer',
            name='poll',
            field=models.ForeignKey(verbose_name='poll', to='poll.PollDate', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='practice',
            field=models.ForeignKey(verbose_name='practice', to='poll.Practice', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(verbose_name='question', to='poll.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='respondent',
            field=models.ForeignKey(verbose_name='respondent', to='poll.Respondent'),
        ),
        migrations.AlterUniqueTogether(
            name='polldatequestionscore',
            unique_together=set([('question', 'poll_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='polldatepracticescore',
            unique_together=set([('practice', 'poll_date')]),
        ),
    ]
