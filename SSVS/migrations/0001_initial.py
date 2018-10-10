# Generated by Django 2.1.dev20171229175031 on 2018-01-22 04:59

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '担当教科',
                'verbose_name_plural': '講師の担当教科リスト',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lessonName', models.CharField(max_length=50, verbose_name='授業種類')),
            ],
            options={
                'verbose_name': '授業名',
                'verbose_name_plural': '授業リスト',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('update_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SSVS.Lesson', verbose_name='授業')),
            ],
            options={
                'verbose_name': 'スケジュール詳細',
                'verbose_name_plural': 'スケジュール',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=255, verbose_name='校舎名')),
            ],
            options={
                'verbose_name': '校舎名',
                'verbose_name_plural': '校舎リスト',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='姓')),
                ('last_name', models.CharField(max_length=255, verbose_name='名')),
            ],
            options={
                'verbose_name': '生徒データ',
                'verbose_name_plural': '生徒リスト',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_list', models.CharField(choices=[('その他', 'その他'), ('演習', '演習'), ('専門', '専門'), ('テスト対策', 'テスト対策'), ('テスト対策（中間）', 'テスト対策（中間）'), ('テスト対策（期末）', 'テスト対策(期末)'), ('受験対策', '受験対策'), ('受験対策（小学生）', '受験対策（小学生）'), ('受験対策（中学生）', '受験対策（中学生）'), ('受験対策（高校生）', '受験対策（高校生）'), ('国語', '国語'), ('現代文', '現代文'), ('古文', '古文'), ('漢文', '漢文'), ('数学', '数学'), ('数学A', '数学A'), ('数学B', '数学B'), ('数学I', '数学I'), ('数学II', '数学II'), ('数学III', '数学III'), ('数学演習', '数学演習'), ('英語', '英語'), ('リーディング', 'リーディング'), ('ライティング', 'ライティング'), ('理科', '理科'), ('物理', '物理'), ('物理基礎', '物理基礎'), ('生物', '生物'), ('生物基礎', '生物基礎'), ('化学', '化学'), ('化学基礎', '化学基礎'), ('社会', '社会'), ('歴史', '歴史'), ('日本史', '日本史'), ('世界史', '世界史'), ('現代史', '現代史'), ('公民', '公民'), ('地理', '地理'), ('P', 'Progmaming'), ('Web開発入門', 'Web開発入門'), ('プログラム開発手法', 'プログラム開発手法')], max_length=200, verbose_name='科目')),
            ],
            options={
                'verbose_name': '科目',
                'verbose_name_plural': '科目リスト',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='氏名')),
            ],
            options={
                'verbose_name': '講師データ',
                'verbose_name_plural': '講師リスト',
            },
        ),
        migrations.CreateModel(
            name='TimeInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(default=datetime.time(7, 0), verbose_name='開始時間')),
                ('end_time', models.TimeField(default=datetime.time(7, 0), verbose_name='終了時間')),
            ],
            options={
                'verbose_name': '時刻',
                'verbose_name_plural': '時刻リスト',
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SSVS.School', verbose_name='校舎'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SSVS.Student', verbose_name='生徒'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SSVS.Teacher', verbose_name='講師'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SSVS.TimeInterval', verbose_name='時間'),
        ),
        migrations.AddField(
            model_name='chargesubject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SSVS.Subject', verbose_name='科目'),
        ),
        migrations.AddField(
            model_name='chargesubject',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SSVS.Teacher', verbose_name='担当講師'),
        ),
    ]
