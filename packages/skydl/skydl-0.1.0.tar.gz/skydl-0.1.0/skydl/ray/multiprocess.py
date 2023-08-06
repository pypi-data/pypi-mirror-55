import ray
import ray.experimental.signal as signal

# Define a user signal.
class UserSignal(signal.Signal):
    def __init__(self, value):
          self.value = value

    def get_value(self):
          return self.value

@ray.remote
def send_signal(value):
    signal.send(UserSignal(value))
    return

ray.init()
signal_value = 'simple signal'
object_id = send_signal.remote(signal_value)
# Wait up to 10sec to receive a signal from the task. Note the task is
# identified by the object_id it returns.
result_list = signal.receive([object_id], timeout=10)
# Print signal values. This should print "simple_signal".
# Note that result_list[0] is the signal we expect from the task.
# The signal is a tuple where the first element is the first object ID
# returned by the task and the second element is the signal object.
print(result_list[0][1].get_value())