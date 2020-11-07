from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.contrib.staticfiles.finders import find
import os

from parser_svg.main import ParserSvg
from main.forms import ExamplesForm, UserForm


class HomePage(TemplateView):

    template_name = 'index.html'
    svg_dir = find('svg')

    def get(self, request, *args, **kwargs):

        if not find('svg/parsed/examples.svg'):
            self.generate_img(
                'examples',
                'elephant',
                'narwhal',
                find_files=True
            )
            self.generate_img(
                'user',
                'user_tab/moose',
                'user_tab/snake',
                find_files=True
            )

        return self.render_to_response({
            'e_form': ExamplesForm,
            'u_form': UserForm
        })

    def post(self, request):

        if 'submitExamples' in request.POST:
            e_form = ExamplesForm(request.POST)
            if e_form.is_valid():
                file1 = e_form.cleaned_data['file1']
                file2 = e_form.cleaned_data['file2']
                self.generate_img('examples', file1, file2, find_files=True)
                return HttpResponseRedirect(reverse_lazy('main:home'))

            return self.render_to_response({
                'e_form': e_form,
                'u_form': UserForm
            })

        elif 'submitUser' in request.POST:
            u_form = UserForm(request.POST, request.FILES)
            if u_form.is_valid():
                file1 = u_form.cleaned_data['file1']
                file2 = u_form.cleaned_data['file2']
                try:
                    self.generate_img('user', file1, file2)
                    return HttpResponseRedirect(reverse_lazy('main:home'))

                except (IndexError, ValueError):
                    u_form.add_error(None, 'Can\'t parse SVG image')

            return self.render_to_response({
                'e_form': ExamplesForm,
                'u_form': u_form
            })

        return HttpResponseNotFound()

    def generate_img(self, tab, file1, file2, find_files=None):

        ps1 = ParserSvg()
        ps2 = ParserSvg()

        if find_files:
            ps1.IN_FILE = find('svg/examples/{}.svg'.format(file1))
            ps2.IN_FILE = find('svg/examples/{}.svg'.format(file2))
        else:
            ps1.IN_FILE = file1
            ps2.IN_FILE = file2

        ps1.OUT_FILE_SVG = os.path.join(
            self.svg_dir, 'parsed/{}.svg'.format(tab)
        )
        ps2.OUT_FILE_JSON = os.path.join(
            self.svg_dir, 'parsed/{}.json'.format(tab)
        )

        ps1.generate_img(tab, find_files)
        ps2.generate_img(tab, find_files)