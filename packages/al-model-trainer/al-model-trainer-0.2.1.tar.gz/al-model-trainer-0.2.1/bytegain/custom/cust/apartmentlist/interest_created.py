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

VERSION = "1.2.0.x.lease180"

filter = FeatureFilter(EXCLUDED_FEATURES, NUMERICAL_FEATURES, CATEGORY_FEATURES, [])

config = {'table': 'SCRATCH.hdedhia.interest_created_20191004',
          'model_name': 'interest_created',
          'model_version': VERSION,
          'feature_json': 'interest_created_v%s' % VERSION,
          'filter': filter,
          'outcome_field': 'leased_at_property_180',
          'control_field': 'lsd_control',
          'positive_outcome_rate_field': 'pct_leases_imported',
          'control_weight': 2,
          'id_field': 'event_id',
          'random_seed': 91876,
          'max_rounds': 801,
          'max_depth': 3,
          'train_step_size': 0.25,
          'min_child_weight': 1800,
          'l2_norm': 300,
          'downsample': True}


prod_config = dict(config)
prod_config['downsample'] = False
