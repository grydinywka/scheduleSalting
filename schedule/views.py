# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Salting

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.bootstrap import FormActions

from django.views.generic import CreateView


def salting_list(request):
	allSalt = Salting.objects.all()

	# try to order salting list
	order_by = request.GET.get('order_by', '')
	if order_by in ('date_salting', 'date_removing', 'id'):
		allSalt = allSalt.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			allSalt = allSalt.reverse()
	elif order_by == '':
		allSalt = allSalt.order_by('date_removing')

	paginator = Paginator(allSalt, 3)
	page = request.GET.get('page')
	try:
		allSalt = paginator.page(page)
	except PageNotAnInteger:
		allSalt = paginator.page(1)
	except EmptyPage:
		allSalt = paginator.page(paginator.num_pages)
	return render(request, "schedule/salting.html", {'allSalt': allSalt})


# Class form for add/edit salting
class SaltingAddEditForm(forms.ModelForm):
	""" Form for add and edit salting """

	class Meta:
		model = Salting
		fields = ['date_salting', 'tank_salting', 'name_fish', 'required_salting', 'weight', 'notes']

	def __init__(self, *args, **kwargs):
		super(SaltingAddEditForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('salting_add')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-6'

		# add buttons
		length = len(self.Meta.fields)
		self.helper.layout = FormActions(
			'date_salting',
			'tank_salting',
			'name_fish',
			'required_salting',
			'weight',
			'notes',
			Submit('add_button', u'Додати', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link")
		)

	date_salting = forms.DateField(
		label=u'Дата посолу',
		initial="2015-08-25",
		help_text=u"Н-д. 2015-08-29",
		error_messages={'required': u"Поле дати засолки є обов’язковим",
						'invalid': u'Ведіть правильний формат Дати'}
	)


def salting_add(request):
	if request.method == 'POST':
		form = SaltingAddEditForm(request.POST)

		if request.POST.get('add_button') is not None:
			data = {}

			if form.is_valid():
				data['date_salting'] = form.cleaned_data['date_salting']
				data['tank_salting'] = form.cleaned_data['tank_salting']
				data['name_fish'] = form.cleaned_data['name_fish']
				data['required_salting'] = form.cleaned_data['required_salting']
				data['weight'] = form.cleaned_data['weight']
				data['notes'] = form.cleaned_data['notes']

				try:
					salting = Salting(**data)
					salting.save()
				except Exception as e:
					messages.error(request, (u"Невдале створення %s! " % salting) + str(e))
				else:
					messages.error(request, (u"Засолка %s була створена успішно!" % salting))

				return HttpResponseRedirect(reverse('home'))
			else:
				messages.info(request, u"Помилка Валідації")
				return render(request, 'schedule/salting_add2.html', {'form': form})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Дожавання Засолки скасовано!")
			return HttpResponseRedirect(reverse('home'))
	else:
		form = SaltingAddEditForm()
	return render(request, "schedule/salting_add2.html", {'form': form})


class SaltingAddView(CreateView):
	model = Salting
	template_name = 'schedule/salting_add2.html'
	form_class = SaltingAddEditForm

	def get_success_url(self):
		messages.success(self.request, u'Засолку %s успішно збережено!' % self.object)
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Створення Засолки відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(SaltingAddView, self).post(request, *args, **kwargs)
