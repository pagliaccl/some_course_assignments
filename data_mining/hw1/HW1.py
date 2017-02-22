import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
	data = pd.read_csv("./Auto.csv")

	#Generate data descriptive statistics
	data.describe().to_csv("./descriptive.csv")

	#Generate box plot
	plot1=data.plot(kind='box')
	plot1.get_figure().savefig("./box.png")
	#
	#Generate scatterMatrix Plot
	plot0=pd.scatter_matrix(data, diagonal='kde', figsize=(10, 10))
	plt.savefig("./scatter.png")

	# Generate Correlation matrix
	data.corr().to_csv("./corr.csv")
	plt.show()



