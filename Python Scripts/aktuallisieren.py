import numpy as np
import matplotlib.pyplot as plt

# Data
categories = ['A', 'B', 'C', 'D', 'E']
values = [4,3,4,6,2]

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values)
ax.fill(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values, alpha=0.25)

# Set ticks
ax.set_xticks(np.linspace(0, 2 * np.pi, len(categories), endpoint=False))
ax.set_xticklabels(categories)

# Title
plt.title("Radar Chart")