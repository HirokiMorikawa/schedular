from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from .models import Teacher, Student, Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        # fields = '__all__'
        exclude = (
            "date",
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            Schedule.objects.get(
                time=cleaned_data["time"],
                school=cleaned_data["school"],
                lesson=cleaned_data["lesson"],
                teacher=cleaned_data["teacher"],
                student=cleaned_data["student"],
            )
        except Schedule.DoesNotExist:
            pass
        else:
            raise ValidationError(
                (
                    "この 時間, 校舎, 授業, "
                    "講師 と 生徒 を持った "
                    "スケジュール詳細 が既に存在します。")
            )


ScheduleFormSet = forms.formset_factory(
    ScheduleForm,
    extra=1,
    max_num=100)
ScheduleModelFormSet = forms.modelformset_factory(
    Schedule,
    form=ScheduleForm,
    extra=1,
    exclude=("date",),
)
