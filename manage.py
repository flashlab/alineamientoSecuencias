import os
from manage.py import app

# if name == "__main__":
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 3609))