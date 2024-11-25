from patterns.browser_error_wrapper import handle_exceptions_quit_driver
from classes.session_manager import SessionManager


class ELMKParser:

    @staticmethod
    # @handle_exceptions_quit_driver
    def start(test_regime: bool = False,
              ask_for_cancel_interval_navigator=5000,
              sleep_secs_up_to_navigator=1.1,
              sleep_secs_up_to_pesr_data_navigator=0.5,
              daemon_tm: bool = False,
              need_parse_left_df: bool = False,
              personal_data_by_filter: bool = False):
        session_manager = SessionManager()
        session_manager.start_new_session(test_regime=test_regime,
                                          personal_data_by_filter=personal_data_by_filter,
                                          need_parse_left_df=need_parse_left_df,
                                          ask_for_cancel_interval_navigator=ask_for_cancel_interval_navigator,
                                          sleep_secs_up_to_navigator=sleep_secs_up_to_navigator,
                                          sleep_secs_up_to_pesr_data_navigator=sleep_secs_up_to_pesr_data_navigator)
        print("session manager started")
        if test_regime:
            return
        # else:
        #     navigator.set_need_parse_left_df(need_parse_left_df=need_parse_left_df)
        #     navigator(ask_for_cancel_interval=ask_for_cancel_interval_navigator,
        #               sleep_secs_up_to=sleep_secs_up_to_navigator,
        #               sleep_secs_up_to_pesr_data=sleep_secs_up_to_pesr_data_navigator,
        #               personal_data_by_filter=True)


if __name__ == '__main__':
    ELMKParser().start(test_regime=False)
