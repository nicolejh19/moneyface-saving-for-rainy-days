import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class chart:
    def make_piechart(self, f, c, t, d, o, monthly=True):
        labels = 'Food','Clothes','Transport', 'Daily Necessities', 'Others'
        dictionary = {}
        if (f > 0): dictionary['Food'] = f
        if (c > 0): dictionary['Clothes'] = c
        if (t > 0): dictionary['Transport'] = t
        if (d > 0): dictionary['Daily Necessities'] = d
        if (o > 0): dictionary['Others'] = o
        
        labels = []
        sizes = []
        for entry in dictionary:
            labels.append(entry)
            sizes.append(dictionary[entry])
        explode = tuple([0] * len(labels))
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%')
        if monthly:
            plt.savefig('monthly.png')
        else:
            plt.savefig('current.png')
        plt.clf()

        return max(dictionary, key=dictionary.get) #return name of max category
