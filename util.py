from flask import render_template
import datetime


def init_utils(application):
    @application.context_processor
    def inject_vars():
        current_year = datetime.date.today().year
        return dict(
            current_year=current_year,
            periods={
                'A': 'A Period', 'B': 'B Period', 'C': 'C Period', 'D': 'D Period', 'E': 'E Period', 'F': 'F Period',
                'G': 'G Period', 'X': 'After School (3:30-4:30)'
            },
            people={-1: 'Class', 1: 'Solo', 2: 'Duo'}
        )

    @application.errorhandler(403)
    def error_403(error):
        return render_template('errors/403.html', title='403', error_code=403), 404

    @application.errorhandler(404)
    def error_404(error):
        return render_template('errors/404.html', title='404', error_code=404), 404

    @application.errorhandler(500)
    def error_500(error):
        return render_template('errors/500.html', title='500', error_code=500), 500
