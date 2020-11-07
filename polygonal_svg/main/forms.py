from django.urls import reverse
from django import forms

from django.contrib.staticfiles.finders import find
import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit


EXAMPLES_DIR = find('svg/examples')

SVG_EXAMPLES_1 = list(map(
    lambda file: (file.split('.svg')[0], file.split('.svg')[0].title()),
    [
        file for file in os.listdir(EXAMPLES_DIR)
        if os.path.isfile(os.path.join(EXAMPLES_DIR, file))
    ]
))
SVG_EXAMPLES_1.insert(0, ('', 'Choose animal...'))
SVG_EXAMPLES_2 = SVG_EXAMPLES_1.copy()


class JasnyImageField(Field):
    template = 'forms/image_field.html'


class SubmitOutline(Submit):
    def __init__(self, *args, **kwargs):
        super(SubmitOutline, self).__init__(*args, **kwargs)
        self.field_classes = 'col col-md-3 btn btn-outline-success ml-md-auto'


class ExamplesForm(forms.Form):

    file1 = forms.ChoiceField(choices=SVG_EXAMPLES_1, label='Animal 1')
    file2 = forms.ChoiceField(choices=SVG_EXAMPLES_2, label='Animal 2')

    def __init__(self, *args, **kwargs):
        super(ExamplesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('main:home')

        self.helper.layout = Layout(
            Field('file1'),
            Field('file2'),
            ButtonHolder(
                SubmitOutline(
                    'submitExamples', 'Show animation', formnovalidate=''
                ),
                css_class='d-flex my-4'
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        file1 = cleaned_data.get('file1')
        file2 = cleaned_data.get('file2')

        if file1 and file2 and file1 == file2:
            raise forms.ValidationError('Animals need to be different')

        return cleaned_data


class UserForm(forms.Form):

    file1 = forms.FileField()
    file2 = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('main:home')
        self.helper.form_enctype = 'multipart/form-data'

        self.helper.layout = Layout(
            JasnyImageField('file1'),
            JasnyImageField('file2'),
            ButtonHolder(
                SubmitOutline(
                    'submitUser', 'Build animation', formnovalidate=''
                ),
                css_class='d-flex my-4'
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        file1 = cleaned_data.get('file1')
        file2 = cleaned_data.get('file2')

        if not (file1 and file2):
            raise forms.ValidationError('Fields can\'t be empty')

        if not (str(file1).endswith('.svg') and str(file1).endswith('.svg')):
            raise forms.ValidationError('Please, choose SVG files')

        cleaned_data['file1'] = file1.read().decode('utf-8')
        cleaned_data['file2'] = file2.read().decode('utf-8')

        return cleaned_data