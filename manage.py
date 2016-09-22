import os
from manage.py import app

# if name == "__main__":
if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 3609))