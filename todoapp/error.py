from flask import render_template

# Обработка ошибки 404
# http://127.0.0.1:5000/56ggf
def page_not_found(e):
    return render_template('404.html'), 404

# Обработка ошибки 500
# хуй знает как провреить 
def internal_server_error(e):
    return render_template('500.html'), 500


