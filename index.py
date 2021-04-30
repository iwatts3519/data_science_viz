import preprocessing
import datavizFunctions as fx
import matplotlib.pyplot as plt

job_listings = preprocessing.df

print(job_listings)

comp, cloud = fx.createWordCloud(3)

print(comp)
plt.imshow(cloud)
plt.axis('off')
plt.show()
