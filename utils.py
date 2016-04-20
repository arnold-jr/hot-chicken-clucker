from kitchen.text.converters import to_unicode, to_bytes

def flatten_json(y):
  out = {}

  def flatten(x, name=''):
    if type(x) is dict:
      for a in x:
        flatten(x[a], name + a + '_')
    elif type(x) is list and len(x)>0 and type(x[0]) is dict:
      for i,a in enumerate(x):
        flatten(a, name + to_bytes(i) + '_')
    else:
      out[to_bytes(name[:-1])] = x

  flatten(y)
  
  return out

if __name__ == '__main__':
  sample_object = {'Name':'John', 'Location':{'City':'Los Angeles','State':'CA'}, 'hobbies':['Music', 'Running']}
  print(flatten_json(sample_object))
