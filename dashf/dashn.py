import dash
from markupsafe import Markup
from flask import render_template


class Dash (dash.Dash):
    def interpolate_index(
        self,
        metas="",
        title="",
        css="",
        config="",
        scripts="",
        app_entry="",
        favicon="",
        renderer="",
    ):

        return render_template(
            "dash.html",
            metas=Markup(metas),
            css=Markup(css),

            dash_config=Markup(config),
            scripts=Markup(scripts),
            app_entry=Markup(app_entry),
            renderer=Markup(renderer),
        )
