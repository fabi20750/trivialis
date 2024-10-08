from config import Config
from app import create_app

app_config = Config()
app = create_app(app_config)
#Run the app
if __name__ == "__main__":
    app.run(debug=True)
