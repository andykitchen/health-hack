from flask import *

import sys
import os
import pandas

data = json.load(open('data/normalized_data.json', 'r'))

metadata = pandas.DataFrame(data, columns = [ 'chr', 'start', 'end', 'gene' ])
samples = pandas.DataFrame(data['samples'], columns = sorted(data['samples'].keys()))



class MyFlask(Flask):
  def get_send_file_max_age(self, name):
    return 0



app = MyFlask(__name__)
app.config.from_object(__name__)


def build_data(metadata_rows, sample_rows):
  return dict(
    chr = list(metadata_rows.chr),
    start = list(metadata_rows.start),
    end = list(metadata_rows.end),
    gene = list(metadata_rows.end),
    samples = { k:list(sample_rows[k]) for k in sorted(sample_rows.columns) }
  )

@app.route('/')
def index_html():
  return render_template('index.html')

@app.route('/data/ordered')
def ordered():
  sort_order = samples.mean(axis=1).argsort()
  return jsonify(build_data(metadata.ix[sort_order], samples.ix[sort_order]))

@app.route('/normalized_data.json')
def return_data():
  return jsonify(data)

if __name__ == '__main__':
  app.debug=True
  app.run('0.0.0.0', 5001)
