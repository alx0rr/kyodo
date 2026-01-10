from . import BaseProfile




class ReferralGoals:
	def __init__(self, data: dict):

		class goalObj:
			def __init__(self, data: dict):
				self.data: dict = data
				self.minCount: int = data.get("minCount")
				self.reached: bool = data.get("reached")
				self.i18nKey: str = data.get("i18nKey")


		self.data: dict = data
		self.freePremium: goalObj = goalObj(data.get("freePremium"))
		self.freeFrame: goalObj = goalObj(data.get("freeFrame"))

class ReferralCode:
	def __init__(self, data: dict):
		self.data: dict = data
		referralInvite: dict = data.get("referralInvite", {})
		self.apiPath: str = data.get("apiPath")
		self.appPath: str = data.get("appPath")
		self.id: str = referralInvite.get("id")
		self.code: str = referralInvite.get("code")
		self.usedCount: int = referralInvite.get("usedCount")
		self.maxUses: int = referralInvite.get("maxUses")
		self.createdTime: str = referralInvite.get("createdTime")
		self.owner: BaseProfile = BaseProfile(referralInvite.get("owner", {}))
		self.goals: ReferralGoals = ReferralGoals(referralInvite.get("goals", {}))