from chainer_addons.training.extensions import SacredReport

class SacredTrainerMixin(object):
	def __init__(self, opts, sacred_params, sacred_trigger=(1, "epoch"), *args, **kwargs):
		super(SacredTrainerMixin, self).__init__(opts=opts, *args, **kwargs)
		self.sacred_reporter = SacredReport(opts,
			sacred_params=sacred_params,
			trigger=sacred_trigger)
		self.extend(self.sacred_reporter)

		def _run(*args, **kwargs):
			return super(SacredTrainerMixin, self).run(*args, **kwargs)

		self.sacred_reporter.ex.main(_run)

	def run(self, *args):
		return self.sacred_reporter.ex(*args)


