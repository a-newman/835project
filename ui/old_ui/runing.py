import integration

def backend_funct(obj):
  print len(obj.backend_data)
  obj.backend_wait = False;
  obj.word = "YAY!"
backend = {
    'words': ['kick', 'wave','yawn','swim'],
    'get_classification': backend_funct,
    'save_sequence': backend_funct,
    'record_delay': 2
  }
integration.runUI(backend);