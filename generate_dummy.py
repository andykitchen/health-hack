import random
import json

out = {
  'chr':  [],
  'gene': [],
  'start': [],
  'end': [],
  'samples': {}
}

chr = 1
start = end = 0

for i in range(48):
  out['samples']['samp_{0:02d}'.format(i)] = []

for i in range(100):
  start = end + max(10000, int(random.gauss(100000, 10000)))
  end = start + max(1000, int(random.gauss(10000, 1000)))
  gene = 'gene_{0}'.format(i)
  out['gene'].append(gene)
  out['chr'].append(str(chr))
  out['start'].append(start)
  out['end'].append(end)
  if random.random() < .1:
    chr += 1
    start = end = 0

  samp_alpha = random.random() * 100
  for k,v in out['samples'].iteritems():
    v.append(random.gammavariate(samp_alpha, 1))


print json.dumps(out, indent=2)
