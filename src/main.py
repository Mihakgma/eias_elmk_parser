from session_manager import SessionManager
from text_caching import TextCaching


class ELMKParser:
    @staticmethod
    def start(text_caching_sleep=3,
              ask_for_cancel_interval_navigator=5000,
              sleep_secs_up_to_navigator=1.1,
              sleep_secs_up_to_pesr_data_navigator=0.5):
        session_manager = SessionManager()
        session_manager.start_new_session()
        navigator = session_manager.get_navigator()
        text_caching = TextCaching(sleep_time=text_caching_sleep,
                                   obj=navigator)
        text_caching.start()
        navigator(ask_for_cancel_interval=ask_for_cancel_interval_navigator,
                  sleep_secs_up_to=sleep_secs_up_to_navigator,
                  sleep_secs_up_to_pesr_data=sleep_secs_up_to_pesr_data_navigator)
