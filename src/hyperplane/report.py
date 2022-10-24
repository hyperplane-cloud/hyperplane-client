from datetime import datetime


class JobReport(object):
    def __init__(self, report_dict: dict):
        self.report_dict = report_dict
        self.received_at = report_dict.get('received_at')
        self.report = report_dict.get('report')

    def __repr__(self) -> str:
        received_at = datetime.fromisoformat(self.received_at)
        return f"[{received_at}]: {self.report}"
