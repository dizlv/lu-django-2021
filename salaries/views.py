import csv
import io

from decimal import Decimal
from datetime import datetime

from django.views.generic import (
    View,
    ListView,
)

from django.views.generic.detail import SingleObjectMixin

from django.shortcuts import (
    render,
    reverse,
)

from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)

from salaries import (
    models,
    forms,
)


def salaries_list(request):
    salaries = models.SalaryEntry.objects.all()

    return render(
        request=request,
        template_name='salaries/list.html',

        context={
            'salaries': salaries,
        }
    )


def get_salaries():
    return models.SalaryEntry.objects.all()


def calculate_age(birth_day):
    return (datetime.utcnow().date() - birth_day).days / 365.2425


def calculate_bonus(amount, age):
    bonus = Decimal(0)

    if amount < 1000 and age < 30:
        bonus = Decimal(500)

    return bonus


def calculate_final_salary(salary_entry):
    age = calculate_age(salary_entry.birth_day)
    bonus = calculate_bonus(salary_entry.amount, age)

    return salary_entry.amount + bonus


def calculate_final_salary_budget():
    salary_entries = get_salaries()
    total_amount = Decimal(0)

    for salary_entry in salary_entries:
        total_amount += calculate_final_salary(salary_entry)

    return total_amount


def salaries_monthly_report(request):
    total_amount = calculate_final_salary_budget()

    return render(
        request=request,
        template_name='salaries/monthly.html',

        context={
            'total_amount': total_amount,
        }
    )


def salary_add(request):
    if request.method == 'POST':
        form = forms.SalaryEntryForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(redirect_to=reverse(viewname='salaries-list'))

    else:
        form = forms.SalaryEntryForm()

    return render(
        request=request,
        template_name='salaries/add.html',

        context={
            'form': form,
        }
    )


def save_imported_salaries(loaded_file):
    with loaded_file.open() as data:
        file_data = data.read().decode('utf-8')
        file_string = io.StringIO(file_data)

        reader = csv.reader(file_string)

        for row in reader:
            first_name, second_name, birth_day, amount = row

            models.SalaryEntry.objects.create(
                first_name=first_name,
                second_name=second_name,
                birth_day=birth_day,
                amount=amount,
            )


def import_salary_entries(request):
    if request.method == 'POST':
        form = forms.FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            save_imported_salaries(form.cleaned_data['file'])

    else:
        form = forms.FileUploadForm()

    return render(
        request=request,
        template_name='salaries/import.html',

        context={
            'form': form,
        }
    )


class SalariesAPIView(View):
    def get(self, request):
        salaries = models.SalaryEntry.objects.all()

        data = {
            'entries': [],
        }

        for entry in salaries:
            formatted_entry = {
                'id': entry.id,
                'first_name': entry.first_name,
                'second_name': entry.second_name,
                'birth_day': entry.birth_day,
                'amount': entry.amount,
            }

            data['entries'].append(formatted_entry)

        return JsonResponse(data)


class Salaries(ListView):
    template_name = 'salaries/list.html'
    queryset = models.SalaryEntry.objects.all()


class AppliedBonusesView(SingleObjectMixin, ListView):
    template_name = 'salaries/bonus_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.SalaryEntry.objects.all())

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['salary_entry'] = self.object

        return context

    def get_queryset(self):
        return self.object.bonus_set.all()


def js_view(request):
    return render(
        request,
        'salaries/js_example.html',
    )
