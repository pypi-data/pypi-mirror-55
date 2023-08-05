import time

from swissarmykit.utils.loggerutils import LoggerUtils

try: from definitions_prod import *
except Exception as e: pass # Surpass error. Note: Create definitions_prod.py

class Timer:

    def __init__(self, total=0, file_name='/timer_', check_point=None):
        self.log = LoggerUtils(appConfig.LOG_PATH + file_name) # type: LoggerUtils
        self.t0 = time.time()
        self.prev_t0 = self.t0
        self.title = None
        self.total_task = total
        self.remain_task = total

        self.check_point = check_point if check_point else 1000

    def reset(self, total=0):
        self.t0 = time.time()
        self.total_task = total
        self.remain_task = total

    def check(self, item=None, idx=None):
        self.remain_task -= 1
        # print('.', end='', flush=True)

        if self.remain_task % self.check_point == 0:
            t1 = time.time()
            time_spent = (t1 - self.t0) / 60
            extra_msg = ''
            if item:
                extra_msg = '(id: %d url: %s)' % (item.id, item.url)
            if idx:
                extra_msg += ' Idx: %d' % idx

            if self.total_task:
                done_task = self.total_task - self.remain_task
                time_eta = self.remain_task * time_spent / done_task

                self.log.info("     {}% tasks - eta: {} - et: {} - remain: {} -  {}".format(
                    round(done_task * 100 / self.total_task), Timer.convert_mm_2_hh_mm(time_eta), Timer.convert_mm_2_hh_mm(time_spent), self.remain_task, extra_msg))
            else:
                self.log.info("     et: {} - total: {} tasks. {}".format(Timer.convert_mm_2_hh_mm(time_spent), abs(self.remain_task), extra_msg))

    def done(self):
        self.spent()

    def start(self, title=None):
        self.title = title
        self.prev_t0 = time.time()

    def spent(self):
        t1 = time.time()
        time_spent = (t1 - self.prev_t0) / 60
        if self.title:
            self.log.info("- {}. et: {}m.".format(self.title, round(time_spent, 2)))
            self.title = None
        else:
            self.log.info("et: {}m.".format(round(time_spent, 2)))

    @staticmethod
    def convert_mm_2_hh_mm(minutes):
        return "%dh %02dm" % (round(minutes / 60), minutes % 60)


if __name__ == '__main__':
    timer = Timer()
    for i in range(2001):
        timer.check()
