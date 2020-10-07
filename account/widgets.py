from django.forms import DateInput, DateTimeInput


class XDSoftDatePickerInput(DateInput):
    template_name = 'widgets/xdsoft_datepicker.html'


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker.html'
