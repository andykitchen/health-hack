With virtualenvwrappers installed:

$ mkvirtualenv health-hack
$ cd haloplex/
$ pip install -r Requirements.txt 
...
$ python haloplex.py 
 * Running on http://0.0.0.0:5001/
 * Restarting with reloader


Supported routes:

/                -> index.html

/static/*        -> static data

/normalized_data.json
                 -> the untouched normalized data (for backwards compat)

/data/count      -> dataset row count

returns:
{ count: 1000 }

/data/sample_ids -> dataset sample_ids

returns:
{ sample_ids: [ 'samp_01', 'samp_02' ] }

/data/ordered    -> dataset as json
query params:
  ?o={desc|asc} order data by mean coverage (descending or ascending)
  ?c=num        return only num rows
  ?s=num        offset by num rows (after sorting)
  ?x=zscore     z-score transform data before returning (after sorting)
  ?i=samp,samp  limit result to a subset of samples (full dataset is still used for sorting)

returns:
{
  chr:   [ ... ]
  start: [ ... ]
  end:   [ ... ]
  gene:  [ ... ]
  samples: {
    samp_01: [ ... ]
    [ ... ]
  }
}
