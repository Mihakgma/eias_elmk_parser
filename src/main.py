from session_manager import SessionManager
from text_caching import TextCaching
from threading import Thread


class ELMKParser:
    @staticmethod
    def start(text_caching_sleep=3,
              ask_for_cancel_interval_navigator=5000,
              sleep_secs_up_to_navigator=1.1,
              sleep_secs_up_to_pesr_data_navigator=0.5,
              max_iterations_caching=15,
              cache_dir_caching="..\\text_data"):
        session_manager = SessionManager()
        session_manager.start_new_session()
        navigator = session_manager.get_navigator()
        text_caching = TextCaching(sleep_time=text_caching_sleep,
                                   obj=navigator,
                                   cache_dir=cache_dir_caching,
                                   max_iterations=max_iterations_caching)
        text_caching.start()
        # Создаем поток для navigator
        navigator_thread = Thread(target=navigator,
                                  args=(
                                      ask_for_cancel_interval_navigator,
                                      sleep_secs_up_to_navigator,
                                      sleep_secs_up_to_pesr_data_navigator,
                                  ))
        navigator_thread.start()
        # navigator(ask_for_cancel_interval=ask_for_cancel_interval_navigator,
        #           sleep_secs_up_to=sleep_secs_up_to_navigator,
        #           sleep_secs_up_to_pesr_data=sleep_secs_up_to_pesr_data_navigator)
