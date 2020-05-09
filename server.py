from builtins import print
from flask import Flask, render_template, url_for, request, flash
from flaskwebgui import FlaskUI
from initProcess import mainGUI as initProcess

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
ui = FlaskUI(app)


# do your logic as usual in Flask
@app.route("/")
def index():
    image_file = url_for('static', filename='GeneratedPic1588411917419.png')
    return render_template('mainGUI.html', image_file=image_file, text_area="Akira is a girl with hair that is blue as "
                                                                            "the ocean, and eyes as red as the red sea")


@app.route('/handle_data', methods=['POST'])
def handle_data():
    descriptionOfChar = request.form['mangaDes']
    print("description enter: "+descriptionOfChar)
    genFileName = initProcess(descriptionOfChar)
    if genFileName == "404":
        image_file = url_for('static', filename='GeneratedPic1588411917419.png')
        descriptionOfChar = "!!! Invalid text, couldnt locate enity/features to generate. Please try  again with new " \
                    "description !!! "
        return render_template('mainGUI.html', image_file=image_file, text_area=descriptionOfChar)

    if genFileName == "403":
        image_file = url_for('static', filename='GeneratedPic1588411917419.png')
        descriptionOfChar = "!!! Character has been identified, but features of the character cannot be identified!!! "
        return render_template('mainGUI.html', image_file=image_file, text_area=descriptionOfChar)

    print(genFileName)
    # return a response
    image_file = url_for('static', filename=(genFileName + ".png"))
    return render_template('mainGUI.html', image_file=image_file, text_area=descriptionOfChar)


#


# call the 'run' method
ui.run()
