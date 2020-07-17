mport pandas as pd
from numpy import nan
from sklearn.tree import DecisionTreeRegressor
from sklearn.impute import SimpleImputer

class MLhelper:
    def __init__(self, ml_data, pred_data):
        self.pred_data = pd.DataFrame(pred_data)
        prepro_data = pd.DataFrame(ml_data)
        prepro_data['amount'].replace(0.0, nan, inplace=True)
        imputer = SimpleImputer(missing_values=nan, strategy='mean')
        self.ml_data = pd.DataFrame(imputer.fit_transform(prepro_data))
        self.ml_data.columns = prepro_data.columns
        self.y = self.ml_data.amount
        self.X = self.ml_data.drop(['amount'], axis=1)
        self.model = DecisionTreeRegressor(random_state = 1)
        self.model.fit(self.X, self.y)
        self.X_pred = self.pred_data.drop(['amount'], axis=1)
        
    def run_model(self):
        pred = self.model.predict(self.X_pred)
        return pred[0]
                                                                                                                        ## CODE USED FOR TESTING SEPARATELY
    # ml_data = {'food': [200.50, 180.30, 210.60, 230.80, 225.60], 'clothes': [50.90, 35.60, 0.00, 36.90, 0.00], 'transport': [60.20, 50.30, 48.40, 36.40, 70.60], 'nec': [20.30, 0.00, 15.90, 0.00, 16.20], 'others': [86.50, 0.00, 0.00, 0.00, 35.50], 'amount': [300, 280, 0.0, 320, 0.0]}
    # pred_data = {'food': [218.90] , 'clothes': [0.00], 'transport': [56.30], 'nec': [0.00], 'others': [20.50], 'amount': [0.00]}
    # mlhelper = MLhelper(ml_data, pred_data)
    # print(mlhelper.ml_data)
    # print(mlhelper.run_model())
