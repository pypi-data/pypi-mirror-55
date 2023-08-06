import argparse
import importlib

from bytegain.custom.cust.apartmentlist import al_xgb
from bytegain.custom.nn_tools import model_utils


parser = argparse.ArgumentParser(description='Trains an AL model',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--model_config', required=True, help='filename of model_config')
parser.add_argument('--feature_analysis', action='store_true', help='If set then a new feature analysis is done')
parser.add_argument('--production', action='store_true', help='If set then push model to production')

args = parser.parse_args()

model_config = args.model_config

module = importlib.import_module('bytegain.custom.cust.apartmentlist.%s' % model_config)
config = getattr(module, 'prod_config' if args.production else 'config')

if args.feature_analysis:
    al_xgb.run_feature_analysis(config)

if args.production:
    al_xgb.train_and_push(config)
else:
    rh, dataset = al_xgb.create_rh_and_dataset(config)
    trained_model = al_xgb.train_from_dataset(config, rh, dataset)
    results_file = '%s.test_predictions.csv' % model_config
    model_utils.save_results_as_csv(results_file, 'id', 'pred',
        trained_model.get_sorted_results(dataset.test))
