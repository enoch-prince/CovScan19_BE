from app import create_app

myApp = create_app()

if __name__ == "__main__":
    myApp.run(host='0.0.0.0')