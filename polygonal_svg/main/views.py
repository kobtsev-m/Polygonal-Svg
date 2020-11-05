from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.contrib.staticfiles.finders import find
from parser_svg.main import ParserSvg
from main.forms import ExamplesForm, UserForm


EXAMPLES_OUT_SVG = find('svg/rendered/parsed_examples.svg')
EXAMPLES_OUT_JSON = find('svg/data/parsed_examples.json')

USER_OUT_SVG = find('svg/rendered/parsed_user.svg')
USER_OUT_JSON = find('svg/data/parsed_user.json')


class HomePage(TemplateView):

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'e_form': ExamplesForm,
            'u_form': UserForm,
            'e_svg': EXAMPLES_OUT_SVG,
            'u_svg': USER_OUT_SVG
        })

    def post(self, request):
        if 'submitExamples' in request.POST:
            e_form = ExamplesForm(request.POST)
            if e_form.is_valid():
                file1 = e_form.cleaned_data['file1']
                file2 = e_form.cleaned_data['file2']

                file1_ps = ParserSvg()
                file2_ps = ParserSvg()

                file1_ps.IN_FILE_PATH = find(
                    'svg/examples/{}.svg'.format(file1)
                )
                file2_ps.IN_FILE_PATH = find(
                    'svg/examples/{}.svg'.format(file2)
                )
                file1_ps.OUT_FILE_SVG_PATH = EXAMPLES_OUT_SVG
                file2_ps.OUT_FILE_JSON_PATH = EXAMPLES_OUT_JSON

                file1_ps.generate_img('examples')
                file2_ps.generate_img('examples')

                return HttpResponseRedirect(reverse_lazy('main:home'))

            return self.render_to_response({
                'e_form': e_form,
                'u_form': UserForm,
                'e_svg': EXAMPLES_OUT_SVG,
                'u_svg': USER_OUT_SVG
            })

        elif 'submitUser' in request.POST:
            u_form = UserForm(request.POST, request.FILES)
            if u_form.is_valid():
                file1 = u_form.cleaned_data['file1']
                file2 = u_form.cleaned_data['file2']

                file1_ps = ParserSvg()
                file2_ps = ParserSvg()

                file1_ps.OUT_FILE_SVG_PATH = USER_OUT_SVG
                file2_ps.OUT_FILE_JSON_PATH = USER_OUT_JSON

                try:
                    file1_ps.generate_img('user', file1)
                    file2_ps.generate_img('user', file2)
                except (IndexError, ValueError):
                    u_form.add_error(None, 'Can\'t parse SVG image')

                return HttpResponseRedirect(reverse_lazy('main:home'))

            return self.render_to_response({
                'e_form': ExamplesForm,
                'u_form': u_form,
                'e_svg': EXAMPLES_OUT_SVG,
                'u_svg': USER_OUT_SVG
            })

        return HttpResponseNotFound()
