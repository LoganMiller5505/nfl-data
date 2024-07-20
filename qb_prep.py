import deepchecks as dc
import pandas as pd
import matplotlib.pyplot as plt

raw = pd.read_csv("nn_data/qb_nn.csv")

train = raw[raw["2023"] == 0]
test = raw[raw["2023"] == 1]

from deepchecks.tabular import Dataset
train_ds = Dataset(train_df, label=label,cat_features=categorical_features, \
                   index_name=index_name, datetime_name=datetime_name)
test_ds = Dataset(test_df, label=label,cat_features=categorical_features, \
                   index_name=index_name, datetime_name=datetime_name)


from deepchecks.tabular.suites import train_test_validation
validation_suite = train_test_validation()
suite_result = validation_suite.run(train_ds, test_ds)
# Note: the result can be saved as html using suite_result.save_as_html()
# or exported to json using suite_result.to_json()
suite_result.print_summary()