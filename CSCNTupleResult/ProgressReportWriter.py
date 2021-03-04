from ..ProgressBar import ProgressReport

##____________________________________________________________________________||
class ProgressReportWriter(object):
    """A progress report writer of an event loop
    """
    def write(self, taskid, dataset, event, total):
        return ProgressReport(
            name = dataset,
            done = event + 1,
            total = total,
            taskid = taskid
        )
