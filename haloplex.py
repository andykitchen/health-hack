from flask import *

import sys
import os
import pandas
import re
import sys


if len(sys.argv) > 1:
  data_path = sys.argv[1]
else:
  data_path = 'data/normalized_data.json'

data = json.load(open(data_path, 'r'))

all_metadata = pandas.DataFrame(data, columns = [ 'chr', 'start', 'end', 'gene' ])
all_samples = pandas.DataFrame(data['samples'], columns = sorted(data['samples'].keys()))



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
  return jsonify(count=len(all_samples.index))

@app.route('/data/sample_ids')
def sample_ids():
  return jsonify(sample_ids=list(all_samples.columns))

@app.route('/data/genes')
def genes():
  return jsonify(genes=list(all_metadata["gene"]))

@app.route('/data/ordered')
def ordered():
  def maybe_int(x):
    try:
      return int(x)
    except:
      return x

  def chr_range(x):
    patt = re.compile(r'^(\w+)(?::([0-9]+)-([0-9]+))?$')
    m = patt.match(x)
    if m is None:
      return None
    if m.group(2) is None:
      return m.group(1), None, None
    return m.group(1), int(m.group(2)), int(m.group(3))

  order = request.args.get('o', None)
  xform = request.args.get('x', None)
  start = maybe_int(request.args.get('s', None))
  count = maybe_int(request.args.get('c', None))
  sample_ids = [ x for x in request.args.get('i', '').split(',') if len(x) ]
  chr_range = chr_range(request.args.get('r', ''))

  samples = all_samples
  metadata = all_metadata

  if chr_range is not None:
    filt = metadata.chr == chr_range[0]
    if chr_range[1] is not None:
      filt = filt & ~((metadata.end < chr_range[1]) | (metadata.start > chr_range[2]))

    samples = samples.ix[filt]
    metadata = metadata.ix[filt]

  if len(sample_ids):
    sample_ids = set(sample_ids) & set(samples.columns)
  else:
    sample_ids = set(samples.columns)

  if order == 'asc':
    sort_order = samples.index[samples.mean(axis=1).argsort()]
  elif order == 'desc':
    sort_order = samples.index[list(reversed(samples.mean(axis=1).argsort()))]
  else:
    sort_order = metadata.index

  if start is not None:
    sort_order = sort_order[start:]
  if count is not None:
    sort_order = sort_order[:count]

  if xform == 'zscore':
    samples = samples.sub(samples.mean(axis=1),axis=0).div(samples.std(axis=1),axis=0)

  return jsonify(build_data(metadata.ix[sort_order], samples.ix[sort_order, sample_ids]))

@app.route('/normalized_data.json')
def return_data():
  return jsonify(data)

if __name__ == '__main__':
  try:
    app.run('0.0.0.0', int(os.environ['PORT']))
  except KeyError:
    app.debug=True
    app.run('0.0.0.0', 5001)
