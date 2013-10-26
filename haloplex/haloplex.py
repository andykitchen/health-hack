from flask import *

import sys
import os

data = json.load(open('data/normalized_data.json', 'r'))

class MyFlask(Flask):
  def get_send_file_max_age(self, name):
    return 0

app = MyFlask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index_html():
  return render_template('index.html')

@app.route('/normalized_data.json')
def return_data():
  return jsonify(data)

if __name__ == '__main__':
  app.debug=True
  app.run('0.0.0.0', 5001)
