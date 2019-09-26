
import signal
import threading
import time
# import logging
from propagating_thread import PropagatingThread
from kafka_consumers import polls

HALT_NOW = threading.Event()
RESPONSE_READY_EV = threading.Event()
NOTIFIER_READY_EV = threading.Event()


def halt_handler(sig, _):
    print("Signal %d.  Halting all threads.", sig)
    HALT_NOW.set()
    RESPONSE_READY_EV.set()
    NOTIFIER_READY_EV.set()


def start_flashmaint_handler(events=None, flashmaint_event=None, pstats=None,
                             database_host=None, dmrqhost=None, topic_in=None):
    print("start_flashmaint_handler")
    flashmaint_event


def start_notifier_handler(events=None, pstats=None, database_host=None,
                           dmrqhost=None, topic_in=None):

    print('start_notifier_handler')
    halt_event = events['halt_event']
    response_ready_event = events['response_ready_event']
    notifier_ready_event = events['notifier_ready_event']
    print('Waiting for ResponseHandler ready.')
    response_ready_event.wait()
    print(halt_event)
    if halt_event.is_set():
        return
    print('Canceling stale requests.')
    print('Signalling ready.')
    notifier_ready_event.set()
    if halt_event.is_set():
        return
    print('Beginning normal operation.')


def start_response_handler(events=None, pstats=None, database_host=None,
                           dmrqhost=None, topic_in=None):

    print("start_response_handler")
    response_ready_event = events['response_ready_event']
    # kafka poll
    polls('test')
    response_ready_event.set()


def start_request_handler(events=None, pstats=None, database_host=None,
                          dmrqhost=None, topic_out=None):

    print('start_request_handler')



def main():

    connector_restart_event = threading.Event()

    flashmaint_wakeup = threading.Event()

    req_handler_wakeup = threading.Event()

    events = {'response_ready_event': RESPONSE_READY_EV,
              'notifier_ready_event': NOTIFIER_READY_EV,
              'halt_event': HALT_NOW,
              'req_handler_wakeup': req_handler_wakeup,
              'connector_restart_event': connector_restart_event}

    flashmaint_thread = PropagatingThread(
        target=start_flashmaint_handler,
        name='FlashmaintHandler',
        kwargs={'events': events,
                'flashmaint_event': flashmaint_wakeup,
                'pstats': 'pstats',
                'database_host': 'database_host',
                'dmrqhost': 'args.dmrqhost',
                'topic_in': 'BKR.kafka_flashmaint_default'})

    # Create the notifier queue handler.
    notifier_thread = PropagatingThread(
        target=start_notifier_handler,
        name='NotifierHandler',
        kwargs={'events': events,
                'pstats': 'pstats',
                'database_host': 'database_host',
                'dmrqhost': 'args.dmrqhost',
                'topic_in': 'BKR.kafka_notifier_default'})

    # Create the response queue handler.
    resp_thread = PropagatingThread(
        target=start_response_handler,
        name='ResponseHandler',
        kwargs={'events': events,
                'pstats': 'pstats',
                'database_host': 'database_host',
                'dmrqhost': 'args.dmrqhost',
                'topic_in': 'args.topic_in'})

    # Create the request queue handler.
    req_thread = PropagatingThread(
        target=start_request_handler,
        name='RequestHandler',
        kwargs={'events': events,
                'pstats': 'pstats',
                'database_host': 'database_host',
                'dmrqhost': 'args.dmrqhost',
                'topic_out': 'args.topic_out'})

    # Enable the signal handler before starting the threads.
    signal.signal(signal.SIGINT, halt_handler)
    signal.signal(signal.SIGTERM, halt_handler)
    signal.signal(signal.SIGQUIT, halt_handler)

    thread_list = [resp_thread, req_thread, notifier_thread,
                   flashmaint_thread]
    for thr in thread_list:
        thr.start()

    print('All Thread started')
    status = 0
    while thread_list:
        try:
            for thr in thread_list:
                thr.join(timeout=0.1)
                if not thr.is_alive():
                    print("Thread %s terminated.", thr.name)
                    thread_list.remove(thr)
        except BaseException as ex:  # pylint: disable=W0703
            status = 1
            print("Thread %s error:", thr.name)
            print(ex)
            # Remove the bad thread; stop the other thread(s).
            thread_list.remove(thr)
            HALT_NOW.set()
            print("Signalling ready to let threads see their "
                            "halt_event.")
            RESPONSE_READY_EV.set()
            NOTIFIER_READY_EV.set()
        finally:
            if thread_list:
                if HALT_NOW.is_set():
                    print("Waiting for threads to terminate.")
                time.sleep(5)

    return status
if __name__ == '__main__':
    main()