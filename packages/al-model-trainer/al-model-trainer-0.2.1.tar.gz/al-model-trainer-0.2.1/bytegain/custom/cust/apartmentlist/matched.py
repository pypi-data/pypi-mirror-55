import bytegain.custom.cust.apartmentlist.al_xgb
from bytegain.custom.cust.apartmentlist.feature_filter import FeatureFilter

from .common import EXCLUDED_FEATURES


NUMERICAL_FEATURES = [
    'preferences_lease_length',
    'preferences_move_urgency',
]

CATEGORY_FEATURES = [
    'property_city_id',
]

BUCKET_FEATURES = [
    'registered_source_app',
]

VERSION = "1.0.3"

filter = FeatureFilter(EXCLUDED_FEATURES, NUMERICAL_FEATURES, CATEGORY_FEATURES, [])

config = {'table': 'ml.matched_20190724',
          'model_name': 'matched',
          'model_version': VERSION,
          'feature_json': 'matched_v%s' % VERSION,
          'filter': filter,
          'outcome_field': 'leased_at_property',
          'control_field': 'lsd_control',
          'control_weight': 1,
          'id_field': 'event_id',
          'random_seed': 91876,
          'max_rounds': 1001,
          'max_depth': 2,
          'train_step_size': 0.35,
          'min_child_weight': 1000,
          'l2_norm': 200,
          'downsample': True}



prod_config = dict(config)
prod_config['downsample'] = False
