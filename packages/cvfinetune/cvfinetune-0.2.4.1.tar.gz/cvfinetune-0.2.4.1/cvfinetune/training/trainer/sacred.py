from .base import default_intervals, Trainer
from chainer_addons.training.extensions import SacredReport

class SacredTrainer(Trainer):
	def __init__(self, ex, intervals=default_intervals, *args, **kwargs):
		super(SacredTrainer, self).__init__(intervals=intervals, *args, **kwargs)
		self.extend(SacredReport(ex=ex, trigger=intervals.log))
