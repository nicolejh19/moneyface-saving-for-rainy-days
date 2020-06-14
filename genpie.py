import matplotlib.pyplot as plt

class chart:
    def make_pie(self, f, c, t, d, o):
        print("done")
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        sizes = [f, c, t, d, o]
        explode = (0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        plt.pie(sizes, explode=explode, labels=labels)
        plt.savefig('foo.png')

