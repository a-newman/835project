import integration
backend = {
    'words': ['kick', 'wave','yawn','swim'],
    'get_classification': backend_funct,
    'record_delay': 2
  }

integration.runUI(backend);