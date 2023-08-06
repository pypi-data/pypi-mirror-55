import pymongo as pym
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec

class SacredPlotter(object):

	@staticmethod
	def auth_url(creds, host="localhost"):
		url = "mongodb://{user}:{password}@{host}:27017/{db_name}?authSource=admin".format(
			host=host, **creds)
		return url

	def __init__(self, creds):
		super(SacredPlotter, self).__init__()
		self.client = pym.MongoClient(SacredPlotter.auth_url(creds))

		self.db = self.client[creds["db_name"]]
		self.metrics = self.db["metrics"]
		self.runs = self.db["runs"]

	def get_values(self, metric, query):

		values = []
		runs = list(self.runs.find(query))

		for run in runs:

			accuracies = self.metrics.find_one(dict(
				name=metric,
				run_id=run["_id"],
			))
			if accuracies is None or accuracies["values"] is None:
				continue

			values.append(accuracies["values"][-1])

		return values

	def plot(self,
		metrics,
		setups,
		query_factory,
		setup_to_label,
		include_running=False,
		metrics_key="val/main/",
		**plot_kwargs):

		"""
			Arguments:
				- metrics: defines which metrics to plot

				- setups: defines different setups, that
					will be compared

				- query_factory: callable; creates from the setup
					specification the pymongo query

				- setup_to_label: callable; converts a setup
					specification into a readable label

				- include_running: whether running experiments should
					be included or not

				- metrics_key: prefix that will be appended to each
					metric name

		"""

		n_metrics = len(metrics)
		n_cols = int(np.ceil(np.sqrt(n_metrics)))
		n_rows = int(np.ceil(n_metrics / n_cols))

		grid = GridSpec(n_rows, n_cols)
		axs = []
		for i, metric in enumerate(metrics):

			res = []

			for setup in setups:
				query = query_factory(setup)

				if not include_running:
					query["status"] = {"$ne": "RUNNING"}

				res.append((setup, self.get_values(f"{metrics_key}{metric}", query)))

			row, col = np.unravel_index(i, (n_rows, n_cols))


			ax = plt.subplot(grid[row, col])
			labels, values = zip(*[(setup_to_label(setup, vals), vals) for setup, vals in res if vals])
			ax.boxplot(values, labels=labels, **plot_kwargs)
			ax.set_title(f"Metric: {metric}")

			axs.append(ax)

		return axs


