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
    gene = list(metadata_rows.gene),
    samples = { k:list(sample_rows[k]) for k in sorted(sample_rows.columns) }
  )

@app.route('/')
def index_html():
  return render_template('index.html')

@app.route('/data/count')
def count():
  return jsonify(count=len(metadata.chr))

@app.route('/data/sample_ids')
def sample_ids():
  return jsonify(sample_ids=list(samples.columns))

@app.route('/data/ordered')
def ordered():
  def maybe_int(x):
    try:
      return int(x)
    except:
      return x

  order = request.args.get('o', None)
  xform = request.args.get('x', None)
  start = maybe_int(request.args.get('s', None))
  count = maybe_int(request.args.get('c', None))
  sample_ids = request.args.get('i', '').split(',')

  if len(sample_ids):
    sample_ids = set(sample_ids) & set(samples.columns)
  else:
    sample_ids = set(samples.columns)

  if order == 'asc':
    sort_order = list(samples.mean(axis=1).argsort())
  elif order == 'desc':
    sort_order = list(reversed(samples.mean(axis=1).argsort()))
  else:
    sort_order = range(len(metadata.chr))

  if start is not None:
    sort_order = sort_order[start:]
  if count is not None:
    sort_order = sort_order[:count]


  if xform == 'zscore':
    sample_data = samples.sub(samples.mean(axis=1),axis=0).div(samples.std(axis=1),axis=0)
  else:
    sample_data = samples

  return jsonify(build_data(metadata.ix[sort_order], samples.ix[sort_order, sample_ids]))

@app.route('/normalized_data.json')
def return_data():
  return jsonify(data)

if __name__ == '__main__':
  app.debug=True
  app.run('0.0.0.0', 5001)
