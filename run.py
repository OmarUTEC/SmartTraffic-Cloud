from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/avatars/')
def avatars():
    return render_template('components/avatars.html')
@app.route('/buttons/')
def buttons():
    return render_template('components/buttons.html')
@app.route('/gridsystem/')
def gridsystem():
    return render_template('components/gridsystem.html')
@app.route('/panels/')
def panels():
    return render_template('components/panels.html')
@app.route('/notifications/')
def notifications():
    return render_template('components/notifications.html')
@app.route('/sweetalert/')
def sweetalert():
    return render_template('components/sweetalert.html')
@app.route('/font_awesome_icons/')
def font_awesome_icons():
    return render_template('components/font-awesome-icons.html')
@app.route('/simple_line_icons/')
def simple_line_icons():
    return render_template('components/simple-line-icons.html')
@app.route('/typography/')
def typography():
    return render_template('components/typography.html')



@app.route('/sidebar/')
def sidebar():
    return render_template('sidebar-style-2.html')
@app.route('/icon_menu/')
def icon_menu():
    return render_template('icon-menu.html')



@app.route('/forms/')
def forms():
    return render_template('forms/forms.html')



@app.route('/tables/')
def tables():
    return render_template('tables/tables.html')
@app.route('/datatables/')
def datatables():
    return render_template('tables/datatables.html')



@app.route('/googlemaps/')
def googlemaps():
    return render_template('maps/googlemaps.html')
@app.route('/jsvectormap/')
def jsvectormap():
    return render_template('maps/jsvectormap.html')



@app.route('/charts/')
def charts():
    return render_template('charts/charts.html')
@app.route('/sparkline/')
def sparkline():
    return render_template('charts/sparkline.html')

@app.route('/widgets/')
def widgets():
    return render_template('widgets.html')






if __name__ == '__main__':
    app.run(debug=True)
