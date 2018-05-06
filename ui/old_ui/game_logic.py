from threading import Thread
class MyThread(Thread):

    def __init__(self, parent=None):
        self.parent = parent
        super(MyThread, self).__init__()

    def run(self):
        # ...
        self.parent and self.parent.on_thread_finished(self, 42)

mgr    = Manager()
thread = mgr.new_thread()
thread.start()

class BackendInterface:
  '''
  load the pre-trained model;
  - Pass the pre-trained model into the run classification model;
  - Pass the 
  '''
  def __init__(self,callerObj):
    self.
