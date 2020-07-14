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
        
        max_cat = max(dictionary, key=dictionary.get)

        labels = []
        sizes = []
        explode = []
        for entry in dictionary:
            labels.append(entry)
            sizes.append(dictionary[entry])
            if entry == max_cat:
                explode.append(0.1)
            else:
                explode.append(0)

        plt.pie(sizes, explode=tuple(explode), labels=labels, autopct='%1.1f%%', shadow=True)
        if monthly:
            plt.savefig('monthly.png')
        else:
            plt.savefig('current.png')
        plt.clf()

        return max_cat #return name of max category

