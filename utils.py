
def flatten_json(y):
  out = {}

  def flatten(x, name=''):
    if type(x) is dict:
      for a in x:
        flatten(x[a], name + a + '_')
    elif type(x) is list:
      i = 0
      for a in x:
        flatten(a, name + unicode(i) + '_')
        i += 1
    else:
      out[unicode(name[:-1])] = unicode(x)

  flatten(y)
  
  return out

if __name__ == '__main__':
  sample_object = {'Name':'John', 'Location':{'City':'Los Angeles','State':'CA'}, 'hobbies':['Music', 'Running']}
  print(flatten_json(sample_object))
