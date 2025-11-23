

class ReportsList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.reports: list[Report] = [Report(report) for report in data.get("queue", [])]
		self.hasMore: bool = data.get("hasMore")
		self.reportCount: int = data.get("reportCount")


class Report:
	def __init__(self, data: dict):
		self.data: dict = data