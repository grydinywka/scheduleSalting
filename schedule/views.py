# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.bootstrap import FormActions, AppendedText

from django.views.generic import CreateView,UpdateView
from .models import Salting

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
		if 'instance' in kwargs:
			if kwargs['instance']:
				self.helper.form_action = reverse('salting_edit',
					kwargs={'sid': kwargs['instance'].id})
			else:
				self.helper.form_action = reverse('salting_add')
		else:
			self.helper.form_action = reverse('salting_add')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = False
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-6'

		# add buttons
		if 'instance' in kwargs:
			if kwargs['instance']:
				addEditBtn = Submit('edit_button', u'Оновити', css_class="btn btn-primary")
			else:
				addEditBtn = Submit('add_button', u'Додати', css_class="btn btn-primary")
		else:
			addEditBtn = Submit('add_button', u'Додати', css_class="btn btn-primary")
		self.helper.layout = FormActions(
			AppendedText('date_salting', "<span class='glyphicon glyphicon-calendar'></span>",
										  active=True),
			'tank_salting',
			'name_fish',
			'required_salting',
			'weight',
			'notes',
			addEditBtn,
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link")
		)

	date_salting = forms.DateField(
		label=u'Дата посолу*',
		# initial="2015-08-25",
		help_text=u"Н-д. 2015-08-29",
		error_messages={'required': u"Поле дати засолки є обов’язковим",
						'invalid': u'Ведіть правильний формат Дати'}
	)
	tank_salting = forms.CharField(
		label='Ємність посолу і місце*',
		help_text="Н-д., Бочка № 2, холодильник",
		error_messages={'required': u"Поле ємності є обов’язкове!"}
	)
	name_fish = forms.ChoiceField(
		label='Назва риби*',
		help_text="Виберіть потрібне із списку.",
		error_messages={'required': u"Назва риби є обов’язковою!"},
        choices=(
            ('Taran', 'Taran'),
            ('Lyasch', 'Lyasch'),
        )
	)
	required_salting = forms.IntegerField(
		label=u"Час на соління(днів)*",
		help_text=u"Введіть кількість днів",
		error_messages={'required': u"ВВведіть час засолки!"},
		min_value=1,
		max_value=60
	)
	weight = forms.CharField(
		label=u"Кількість риби",
		required=False,
		help_text=u"В кілограмах або ящиках"
	)
	notes = forms.CharField(
		label=u'Нотатки',
		help_text=u'Додаткова інформація',
		max_length=2000,
		required=False,
		widget=forms.Textarea
	)

def salting_edit(request, sid):
	salting = Salting.objects.filter(pk=sid)[0]
	if request.method == 'POST':
		form = SaltingAddEditForm(request.POST)

		if request.POST.get('edit_button') is not None:
			if form.is_valid():
				salting.date_salting = form.cleaned_data['date_salting']
				salting.tank_salting = form.cleaned_data['tank_salting']
				salting.name_fish = form.cleaned_data['name_fish']
				salting.required_salting = form.cleaned_data['required_salting']
				salting.weight = form.cleaned_data['weight']
				salting.notes = form.cleaned_data['notes']

				# check data_removing
				deltaSalting = datetime.timedelta(days=int(salting.required_salting))
				salting.date_removing = salting.date_salting + deltaSalting

				try:
					salting.save()
				except Exception as e:
					messages.error(request, (u"Невдале Редагування %s! " % salting) + str(e))
				else:
					messages.success(request, (u"Засолка %s була оновлена успішно!" % salting))

				return HttpResponseRedirect(reverse('home'))
			else:
				messages.info(request, u"Помилка Валідації")
				return render(request, 'schedule/salting_add2.html', {'form': form, 'title': "edit", 'sid': sid})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Оновлення Засолки %s скасовано!" % salting)
			return HttpResponseRedirect(reverse('home'))
	else:
		default = {
			'date_salting': salting.date_salting,
			'tank_salting': salting.tank_salting,
			'name_fish': salting.name_fish,
			'required_salting': salting.required_salting,
			'weight': salting.weight,
			'notes': salting.notes
		}
		form = SaltingAddEditForm(default)
		return render(request, 'schedule/salting_add2.html', {'form': form,
															  'sid': sid,
															  'title': 'edit'})

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
					messages.success(request, (u"Засолка %s була створена успішно!" % salting))

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
	template_name = 'schedule/salting_add_with_crispy.html'
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

	def get_context_data(self, **kwargs):
		context = super(SaltingAddView, self).get_context_data(**kwargs)
		context['title'] = u'Додавання Засолки'

		return context

class SaltingEditView(UpdateView):
	model = Salting
	template_name = 'schedule/salting_add_with_crispy.html'
	pk_url_kwarg = 'sid'
	form_class = SaltingAddEditForm

	def get_success_url(self):
		messages.success(self.request, u'Засолку %s успішно оновлено!' % self.object)
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Оновлення Засолки %s відмінено!' % self.get_object())
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(SaltingEditView, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(SaltingEditView, self).get_context_data(**kwargs)
		context['title'] = u'Оновлення Засолки'

		return context

