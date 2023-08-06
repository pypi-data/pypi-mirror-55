# -*- coding: utf-8 -*-
import jinja2
from sphinx.application import Sphinx
from sphinx_paw.constants import PACKAGE_NAME

from sphinx_paw.builders.constants.latexpdf import FILENAME_FOOTER
from sphinx_paw.builders.constants.latexpdf import FILENAME_PREAMBLE
from sphinx_paw.configurable import ConfigFile
from sphinx_paw.configurable import set_config_value
from sphinx_paw.rewritable import rewritable_file_content


def jinja_for_latex():
    """Make jinja2 env for templating latex"""
    # http://eosrei.net/articles/2015/11/
    # latex-templates-python-and-jinja2-generate-pdfs
    return jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True
    )


def init_latex(app, config):
    """Configure confluence builder options"""
    assert isinstance(app, Sphinx)
    assert isinstance(config, ConfigFile)
    config.assert_has_section('metadata')

    # Use xalatex
    set_config_value(app, 'latex_engine', 'xelatex')

    # Paper spec
    set_config_value(app, 'latex_paper_size', 'a4')

    # Show urls in footnotes
    set_config_value(app, 'latex_show_urls', 'footnotes')

    # Use international build
    set_config_value(app, 'latex_use_xindy', True)

    # Add specific indicies
    set_config_value(app, 'latex_domain_indices', True)

    latex_preamble = rewritable_file_content(app, FILENAME_PREAMBLE)
    latex_attend_of_body = rewritable_file_content(app, FILENAME_FOOTER)

    # Force use template for attendofbody
    if True:
        from sphinx.locale import get_translation
        _ = get_translation(PACKAGE_NAME)
        template = jinja_for_latex().from_string(latex_attend_of_body)
        latex_attend_of_body = template.render(
            list_of_images_title=_("List of images"),
            list_of_tables_title=_("List of tables"),
            list_of_listings_title=_("List of listings")
        )

    set_config_value(app, 'latex_elements', {
        'preamble': latex_preamble,
        'atendofbody': latex_attend_of_body,
        'pointsize': '10pt',
        'fncychap': '',
        'extraclassoptions': 'openany,oneside',
        'sphinxsetup': 'hmargin={1in,1in}, vmargin={1in,1in}, marginpar=0.1in',
    })

    latex_document = (
        app.config['master_doc'],  # source start file
        app.config['package'] + '.tex',  # result file name
        app.config['project'],  # title
        app.config['author'],  # author
        'manual',  # documentclass [howto/manual]
        False
    )

    set_config_value(
        app,
        'latex_documents',
        [latex_document]
    )
