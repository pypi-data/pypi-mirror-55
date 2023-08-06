import time
import yaml
import logging

from py_wa_adb.wa_adb import WA_ADB, datetime_to_epoch
from py_wa_adb.wa_sqlite import WA_SQLITE


class WAEndToEnd(object):
    """ Base Class that will contain any related 
    information needed for the tests.
    """

    def __init__(self, wa_bot_number):
        """ Constructor method.
        Defines wa_bot_number to the value recived in the wa_bot_number argument
        """
        self.wa_bot_number = wa_bot_number


def parse_yaml_data_file(file_path):
    """ Read the contents of of the file located at `file_path`
    and return the yaml parsed object from it.
    """
    with open(file_path, "r+") as f:
        content = f.read()
        yaml_input = yaml.load(content, Loader=yaml.Loader)
    return yaml_input




def log_received_messages(messages, last_n_messages):
    for i, message in enumerate(messages[last_n_messages * -1:], 1):
        logging.info("Received message {}:\n {} \n---------------\n".format(i,message[-2].decode()))

def log_sent_message(message):
    logging.info("SENDING MESSAGE:\n {} \n---------------\n".format(message))


def wait_for_n_messages(wa_adb_instance, expected_n_messages, n_iterations=10, iteration_sleep_time=3):
    for _ in range(n_iterations):
        try:
            post_restart_messages = wa_adb_instance.get_messages()
            len_post_messages = len(post_restart_messages)
            if expected_n_messages == len_post_messages:
                break
            else:
                time.sleep(iteration_sleep_time)
        except Exception as e:
            
            time.sleep(iteration_sleep_time)
            pass
        pass
    else:
        logging.info(f"{len_post_messages} out of expected {expected_n_messages} messages not found")
        raise Exception(f"{expected_n_messages} messages not found")
    pass


def send_expect_n_and_validate(
    TEXT_TO_BE_SENT, EXPECT_N_MESSAGES, VALIDATE_FUNCTION
):
    wa_adb = WA_ADB()

    def inner_wrapper(received_function):
        
        def double_wrapper(test_run_instance):
            
            received_function(test_run_instance)
            
            if TEXT_TO_BE_SENT is not None:
                ttbs = TEXT_TO_BE_SENT if type(TEXT_TO_BE_SENT) is str else TEXT_TO_BE_SENT(test_run_instance)
            else:
                ttbs = None
            log_sent_message(ttbs)
            prev_messages = wa_adb.get_messages()
            if ttbs:
                wa_adb.send_text_message(test_run_instance.wa_bot_number, ttbs)
            if EXPECT_N_MESSAGES is not None:
                wait_for_n_messages(wa_adb, len(prev_messages) + EXPECT_N_MESSAGES + (0 if not TEXT_TO_BE_SENT else 1))
            post_wait_messages = wa_adb.get_messages()
            if EXPECT_N_MESSAGES is not None:
                log_received_messages(post_wait_messages, EXPECT_N_MESSAGES)
            VALIDATE_FUNCTION(post_wait_messages, test_run_instance)
        
        return double_wrapper

    return inner_wrapper