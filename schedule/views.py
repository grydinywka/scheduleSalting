# -*- coding: utf-8 -*-

import datetime, time

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import send_mail

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.bootstrap import FormActions, AppendedText
import sendgrid
from sendgrid import SendGridError, SendGridClientError, SendGridServerError
from smtpapi import SMTPAPIHeader

from django.views.generic import CreateView, UpdateView, ListView
from .models import Salting

# from scheduleSalting.pswSendGrid import password, sendGridUser
# from scheduleSalting.emails import emails
from scheduleSalting.settings import ADMIN_EMAIL

emails = {
    "gmail": 'grydinywka@gmail.com',
    "univ_mail": 'sergeyi@univ.kiev.ua'
}

password = 'swimming16'
sendGridUser = 'sergiyi1'

def send_email(needed_salting, date_today, request=None):
	msg2 = u'Сьогодні, ' + str(date_today) + u'\nВам потрібно витягнути наступні засолки:\n'
	msg2 += '-'.join([i.tank_salting + ', ' + i.name_fish + '\n' for i in needed_salting])
	msg2 = msg2[:-1]
	send_mail('subj', msg2, emails["univ_mail"], [emails["gmail"]])

def send_email_grid(needed_salting, date_today, request):
	sg = sendgrid.SendGridClient(sendGridUser, password, raise_errors=True)
	header = SMTPAPIHeader()

	message = sendgrid.Mail()
	message.add_to([ADMIN_EMAIL])
	message.set_from(emails["univ_mail"])
	message.set_subject('Salting notify')
	msg2 = u'Сьогодні, ' + str(date_today) + u'\nВам потрібно витягнути наступні засолки:\n'
	msg2 += '-'.join([i.tank_salting + ', ' + i.name_fish + '\n' for i in needed_salting])
	msg2 = msg2[:-1]
	message.set_text(msg2)
	# message.set_html('Saltings')

	try:
		sg.send(message)
	except SendGridClientError as e:
		messages.error(request, str(e))
		raise SendGridClientError
	except SendGridServerError as e:
		messages.error(request, str(e))
		raise SendGridServerError
	else:
		messages.success(request, u'Повідомлення успішно надіслане за допомогою SendGrid!')

def checkDataRemoving(queryset, request):
	global date_today, time_now, time_to_send_msg
	date_today = time.strftime("%Y-%m-%d")
	time_to_send_msg = time.strftime("20:11")
	time_now = time.strftime("%H:%M")
	needed_salting = queryset.filter(date_removing=date_today)

	if needed_salting and time_now == time_to_send_msg:
		try:
			send_email(needed_salting, date_today, request)
		except Exception as e:
			messages.error(request, u'Під час відправки листа виникла непередбачувана ' \
			u'помилка. Спробуйте скористатись даною формою пізніше. ' \
			+ str(e))
		else:
			messages.success(request, u'Повідомлення успішно надіслане!')

def salting_list(request):
	allSalt = Salting.objects.all().filter(status=True)

	# try to order salting list
	order_by = request.GET.get('order_by', '')
	if order_by in ('date_salting', 'date_removing', 'id'):
		allSalt = allSalt.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			allSalt = allSalt.reverse()
	elif order_by == '':
		allSalt = allSalt.order_by('date_removing')

	checkDataRemoving(allSalt, request)

	paginator = Paginator(allSalt, 5)
	page = request.GET.get('page')
	try:
		allSalt = paginator.page(page)
	except PageNotAnInteger:
		allSalt = paginator.page(1)
	except EmptyPage:
		allSalt = paginator.page(paginator.num_pages)

	return render(request, "schedule/salting.html", {'allSalt': allSalt, 'title': u'Засолка триває', 'status': True,
													 'date_today': date_today, 'time_now': time_now,
													 'time_to_send_msg': time_to_send_msg,
													 'date': datetime.datetime.now()})

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
		label=u'Дата посолу',
		# initial="2015-08-25",
		help_text=u"Н-д. 2015-08-29",
		error_messages={'required': u"Поле дати засолки є обов’язковим",
						'invalid': u'Ведіть правильний формат Дати'}
	)
	tank_salting = forms.CharField(
		label='Ємність посолу і місце',
		help_text="Н-д., Бочка № 2, холодильник",
		error_messages={'required': u"Поле ємності є обов’язкове!"}
	)
	name_fish = forms.ChoiceField(
		label='Назва риби',
		help_text="Виберіть потрібне із списку.",
		error_messages={'required': u"Назва риби є обов’язковою!"},
        choices=(
            (u'Тарань', u'Тарань'),
            (u'Лящ різаний', u'Лящ різаний'),
            (u'Лящ цілий', u'Лящ цілий'),
            (u'Сом філе', u'Сом філе'),
            (u'Товстолоб філе', u'Товстолоб філе'),
            (u'Судак', u'Судак'),
            (u'Густирь', u'Густирь'),
            (u'Сало, м’ясо', u'Сало, м’ясо'),
            (u'Карась різаний', u'Карась різаний'),
            (u'Карась цілий', u'Карась цілий'),
            (u'Короп різаний', u'Короп різаний'),
        )
	)
	required_salting = forms.IntegerField(
		label=u"Час на соління(днів)",
		help_text=u"Введіть кількість днів",
		error_messages={'required': u"Ввведіть час засолки!"},
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

	def form_invalid(self, form):
		messages.error(self.request, u'Помилка Валідації!')
		return self.render_to_response(self.get_context_data(form=form))

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

	def form_invalid(self, form):
		messages.error(self.request, u'Помилка Валідації!')
		return self.render_to_response(self.get_context_data(form=form))

class SaltingChangeStatusForm(forms.ModelForm):
	""" Form for change salting's status """

	class Meta:
		model = Salting
		fields = ['status']

	def __init__(self, *args, **kwargs):
		super(SaltingChangeStatusForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('salting_change_status',
										  kwargs={'sid': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-6'

		# add buttons
		self.helper.layout = FormActions(
			'status',
			Submit('edit_button', u'ОК', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link")
		)


class SaltingChangeStatus(UpdateView):
	model = Salting
	template_name = 'schedule/salting_change_status.html'
	pk_url_kwarg = 'sid'
	form_class = SaltingChangeStatusForm

	def get_success_url(self):
		if self.object.status:
			status = u'"ЗАСОЛКА ТРИВАЄ"'
		else:
			status = u'"ЗАСОЛКА ВИТЯГНУТА"'
		messages.success(self.request, (u'Статус Засолки %s успішно Змінено на %s!' % (self.object,
																					   status)))
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Зміна Статусу Засолки %s відмінена!' % self.get_object())
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(SaltingChangeStatus, self).post(request, *args, **kwargs)

class SaltingHistory(ListView):
	"""Salting list, status - False"""

	model = Salting
	template_name = "schedule/salting.html"
	queryset = Salting.objects.all().filter(status=False).order_by('date_removing')
	context_object_name = 'allSalt'

	def get_context_data(self, **kwargs):
		context = super(SaltingHistory, self).get_context_data(**kwargs)

		context['title'] = u'Витягнуті Засолки'
		context['status'] = False

		return context

	def get_queryset(self):
		qs = super(SaltingHistory, self).get_queryset()

		order_by = self.request.GET.get('order_by', '')
		if order_by in ('date_salting', 'date_removing', 'id'):
			qs = qs.order_by(order_by)
			if self.request.GET.get('reverse', '') == '1':
				qs = qs.reverse()

		paginator = Paginator(qs, 3)
		page = self.request.GET.get('page')
		try:
			qs = paginator.page(page)
		except PageNotAnInteger:
			qs = paginator.page(1)
		except EmptyPage:
			qs = paginator.page(paginator.num_pages)

		return qs
