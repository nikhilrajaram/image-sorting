import os
import re
import numpy as np
import pandas as pd
from itertools import combinations_with_replacement
import matplotlib.pyplot as plt

filenames = os.listdir('../img/')


def strip(s):
	s = re.sub('.jpg', '', s)
	s = re.sub('_[0-9]+', '', s)
	s = re.sub('MV', '', s)
	s = re.sub('-EFFECTS', '', s)
	check1 = re.findall('[0-9]'*4, s)
	if (check1):
		if (check1[0] == s):
			return 1
		else:
			return 2
	elif s == 'IMG':
		return 3
	elif s == 'paris_general':
		return 4


df = []
with open('sims/sims_500_filenames.csv', 'w') as newf:
	with open('sims/sims_500.csv', 'r') as f:
		for line in f:
			s = line.split(', ')
			newf.write('{:33s}, {:33s}, {}, {}, {}'.format(s[0], s[1], strip(s[0]), strip(s[1]), s[2]))
			df.append([s[0], s[1], strip(s[0]), strip(s[1]), float(s[2])])

df = pd.DataFrame(df)

idx_combs = list(combinations_with_replacement(range(1, 5), 2))
sims = {k: 0 for k in idx_combs}
sims_counts = {k: 0 for k in idx_combs}

for i in range(len(df)):
	sims[(df.iloc[i][2], df.iloc[i][3])] += df.iloc[i][4]
	sims_counts[(df.iloc[i][2], df.iloc[i][3])] += 1


sims_means = {k: sims[k]/sims_counts[k] for k in idx_combs}

fig, ax = plt.subplots()
x = list(map(lambda x:x[0], list(sims_means.keys())))
y = list(map(lambda x:x[1], list(sims_means.keys())))
sizes = np.array(list(sims_means.values()))
sizes_labs = sizes/(np.max(sizes)/2000)
plt.scatter(x, y, s=sizes_labs)

for i, txt in enumerate(sizes):
    ax.annotate(round(txt, 6), (x[i], y[i]))

plt.title('Rough Confusion Diagram')
plt.xlabel('Image 1 category')
plt.xlabel('Image 2 category')
plt.savefig('img/rough_confusion_diagram.png', dpi=300)
plt.show()
