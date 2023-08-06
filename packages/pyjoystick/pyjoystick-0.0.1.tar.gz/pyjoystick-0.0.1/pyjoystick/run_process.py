import time
import threading
import multiprocessing as mp
from queue import Empty

from pyjoystick.stash import Stash
from pyjoystick.run_thread import ThreadEventManager


class MultiprocessingEventManager(object):
    def __init__(self, event_loop=None, add_joystick=None, remove_joystick=None, handle_key_event=None, alive=None,
                 button_repeater=None, activity_timeout=0.01):
        super().__init__()

        if add_joystick is not None:
            self.add_joystick = add_joystick
        if remove_joystick is not None:
            self.remove_joystick = remove_joystick
        if handle_key_event is not None:
            self.handle_key_event = handle_key_event
        if alive is None:
            alive = mp.Event()

        self.activity_timeout = activity_timeout
        self.button_repeater = button_repeater

        self.event_loop = event_loop
        self.joysticks = Stash()
        self.alive = alive
        self.process = None
        self.queue = mp.Queue()

        if self.button_repeater is not None:
            self.button_repeater.key_repeated = self.save_key_event

    def add_joystick(self, joy):
        """Save the added joystick."""
        pass

    def remove_joystick(self, joy):
        """Remove the given joystick."""
        pass

    def handle_key_event(self, key):
        """Function to handle key event happens"""
        pass

    def save_joystick(self, joy):
        """Save the added joystick."""
        self.joysticks.append(joy)

        # Run the callback handler
        self.add_joystick(joy)

    def delete_joystick(self, joy):
        """Delete the removed joystick."""
        try:
            self.joysticks.remove(joy)
        except:
            pass

        # Run the callback handler
        self.remove_joystick(joy)

    def save_key_event(self, key):
        """Save the initial key event."""
        try:
            joy = self.joysticks[key.joystick]
            key.joystick = joy
            joy.update_key(key)
        except:
            pass

        try:
            self.button_repeater.set(key)
        except:
            pass

        with self.event_lock:
            if key.keytype == key.BUTTON or key not in self.event_list:
                self.event_list.append(key)

    def process_events(self):
        """Process all of the saved events."""
        with self.event_lock:
            for k in self.event_list:
                k.update_value()

                # Run the callback handler
                self.handle_key_event(k)
            self.event_list = []

    def run(self, event_loop, add_joystick, remove_joystick, handle_key_event, alive=None, button_repeater=None):
        """Run the an event loop to process SDL Events.

        Args:
            event_loop (callable/function): Event loop function to run.
            add_joystick (callable/function): Called when a new Joystick is found!
            remove_joystick (callable/function): Called when a Joystick is removed!
            handle_key_event (callable/function): Called when a new key event occurs!
            alive (callable/function)[None]: Function to return True to continue running. If None run forever
            button_repeater (ButtonRepeater): Thread to start which will monitor button keys and trigger repeating.
        """
        if alive is None:
            alive = lambda: True

        if button_repeater is not None:
            button_repeater.start()

        th = ThreadEventManager(event_loop)
        event_loop(add_joystick, remove_joystick, handle_key_event, alive=alive)

    def is_running(self):
        """Return if the event loop is running."""
        return self.alive.is_set()

    def start(self):
        """Start running the event loop."""
        self.stop()

        self.alive.set()
        self.thread = threading.Thread(target=self.run,
                                       args=(self.event_loop, self.save_joystick, self.delete_joystick,
                                             self.save_key_event),
                                       kwargs={'alive': self.is_running, 'button_repeater': self.button_repeater})
        self.thread.daemon = True
        self.thread.start()

        self.process_tmr = PeriodicThread(self.activity_timeout, self.process_events)
        self.process_tmr.daemon = True
        self.process_tmr.start()

    def stop(self):
        """Stop running the event loop."""
        try:
            self.alive.clear()
        except:
            pass
        try:
            self.thread.join(0)
        except:
            pass
        self.thread = None

    def __enter__(self):
        if not self.is_running():
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return exc_type is None

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass
