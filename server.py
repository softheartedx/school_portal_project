from flask_app import app
from flask_app.controllers import user_controller
from flask_app.controllers import classroom_controller
from flask_app.controllers import enrollment_controller

if __name__=='__main__':
    app.run(debug=True, port=5001)