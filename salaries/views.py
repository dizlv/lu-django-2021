from django.shortcuts import render

from salaries import models


def salaries_list(request):
    salaries = models.SalaryEntry.objects.all()

    return render(
        request=request,
        template_name='salaries/list.html',

        context={
            'salaries': salaries,
        }
    )


def salaries_monthly_report(request):
    pass


def salary_add(request):
    pass
