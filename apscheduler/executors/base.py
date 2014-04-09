from abc import ABCMeta, abstractmethod
from collections import defaultdict
from datetime import datetime, timedelta
import logging
import sys

from dateutil.tz import tzutc
import six

from apscheduler.events import JobEvent, EVENT_JOB_MISSED, EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

logger = logging.getLogger('apscheduler.executors')
utc = tzutc()


class MaxInstancesReachedError(Exception):
    pass


class BaseExecutor(six.with_metaclass(ABCMeta, object)):
    """Base class of all executors."""

    _scheduler = None
    _lock = None

    def __init__(self):
        super(BaseExecutor, self).__init__()
        self._instances = defaultdict(lambda: 0)

    def start(self, scheduler):
        """
        Called by the scheduler when the scheduler is being started or when the executor is being added to an already
        running scheduler.

        :type scheduler: `~apscheduler.scheduler.base.BaseScheduler`
        """

        self._scheduler = scheduler
        self._lock = scheduler._create_lock()

    def shutdown(self, wait=True):
        """
        Shuts down this executor.

        :param wait: ``True`` to wait until all submitted jobs have been executed
        """

    def submit_job(self, job, run_times):
        """
        Submits job for execution.

        :param job: job to execute
        :param run_times: list of `~datetime.datetime` objects specifying when the job should have been run
        :type job: `~apscheduler.scheduler.job.Job`
        :type run_times: list
        """

        assert self._lock is not None, 'This executor has not been started yet'
        with self._lock:
            if self._instances[job.id] >= job.max_instances:
                raise MaxInstancesReachedError

            self._do_submit_job(job, run_times)
            self._instances[job.id] += 1

    @abstractmethod
    def _do_submit_job(self, job, run_times):
        """Performs the actual task of scheduling `run_job` to be called."""

    def _run_job_success(self, job_id, events):
        """Called by the executor with the list of generated events when `run_job` has been successfully called."""

        with self._lock:
            self._instances[job_id] -= 1

        for event in events:
            self._scheduler._notify_listeners(event)

    def _run_job_error(self, job_id, exc_type, exc_value, traceback):
        """Called by the executor with the exception if there is an error calling `run_job`."""

        with self._lock:
            self._instances[job_id] -= 1

        exc_info = (exc_type, exc_value, traceback)
        logger.error('Error running job %s' % job_id, exc_info=exc_info)


def run_job(job, run_times):
    """Called by executors to run the job. Returns a list of scheduler events to be dispatched by the scheduler."""

    events = []
    for run_time in run_times:
        # See if the job missed its run time window, and handle possible misfires accordingly
        difference = datetime.now(utc) - run_time
        grace_time = timedelta(seconds=job.misfire_grace_time)
        if difference > grace_time:
            events.append(JobEvent(EVENT_JOB_MISSED, job, run_time))
            logger.warning('Run time of job "%s" was missed by %s', job, difference)
            continue

        logger.info('Running job "%s" (scheduled at %s)', job, run_time)
        try:
            retval = job.func(*job.args, **job.kwargs)
        except:
            exc, tb = sys.exc_info()[1:]
            events.append(JobEvent(EVENT_JOB_ERROR, job, run_time, exception=exc, traceback=tb))
            logger.exception('Job "%s" raised an exception', job)
        else:
            events.append(JobEvent(EVENT_JOB_EXECUTED, job, run_time, retval=retval))
            logger.info('Job "%s" executed successfully', job)

    return events