from app import create_app

app = create_app() # Instance of Flask from the create_app() subroutine.

if __name__ == '__main__': # App will only run if this file is run.
    app.run(debug=True) # Enables debug mode. Whenever a change is made, code is rerun.