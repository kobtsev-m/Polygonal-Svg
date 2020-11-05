from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import TemplateView
import os

from parser_svg.main import ParserSvg
from main.forms import ExamplesForm, UserForm


PATH_TO_EXAMPLES = os.path.join(
    settings.BASE_DIR,
    'main/static/img/svg_examples/{}.svg'
)
PATH_TO_SVG = os.path.join(
    settings.BASE_DIR,
    'main/templates/svg/parsed_{}.html'
)
PATH_TO_JSON = os.path.join(
    settings.BASE_DIR,
    'main/static/img_data/parsed_{}.json'
)


class HomePage(TemplateView):

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'e_form': ExamplesForm, 'u_form': UserForm}
        )

    def post(self, request):
        if 'submitExamples' in request.POST:
            e_form = ExamplesForm(request.POST)
            if e_form.is_valid():
                file1 = e_form.cleaned_data['file1']
                file2 = e_form.cleaned_data['file2']

                file1_ps = ParserSvg()
                file2_ps = ParserSvg()

                file1_ps.IN_FILE_PATH = PATH_TO_EXAMPLES.format(file1)
                file2_ps.IN_FILE_PATH = PATH_TO_EXAMPLES.format(file2)
                file1_ps.OUT_FILE_SVG_PATH = PATH_TO_SVG.format('examples')
                file2_ps.OUT_FILE_JSON_PATH = PATH_TO_JSON.format('examples')

                file1_ps.generate_img('examples')
                file2_ps.generate_img('examples')

                return HttpResponseRedirect(reverse_lazy('main:home'))

            return self.render_to_response(
                {'e_form': e_form, 'u_form': UserForm}
            )

        elif 'submitUser' in request.POST:
            u_form = UserForm(request.POST, request.FILES)
            if u_form.is_valid():
                file1 = u_form.cleaned_data['file1']
                file2 = u_form.cleaned_data['file2']

                file1_ps = ParserSvg()
                file2_ps = ParserSvg()

                file1_ps.OUT_FILE_SVG_PATH = PATH_TO_SVG.format('user')
                file2_ps.OUT_FILE_JSON_PATH = PATH_TO_JSON.format('user')

                file1_ps.generate_img('user', file1)
                file2_ps.generate_img('user', file2)

                return HttpResponseRedirect(reverse_lazy('main:home'))

            return self.render_to_response(
                {'e_form': ExamplesForm, 'u_form': u_form}
            )

        return HttpResponseNotFound()
