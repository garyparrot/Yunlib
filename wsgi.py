import os
from application import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":
    setting = {
            "host" : os.environ.get("host","0.0.0.0"),
            "port" : os.environ.get("port",443),
            "ssl_context": ( 
                os.environ.get('certification_pam'),
                os.environ.get('certification_key'),
            ),
            "use_reloader": False
    }

    app.run(**setting)
