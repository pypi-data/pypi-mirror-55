### Common setup

```
% export AWS_ACCESS_KEY_ID=<IAM user with write permission to S3 bucket>
% export AWS_SECRET_ACCESS_KEY=<key for IAM user>
% export SNOWFLAKE_USER=ml_training
% export SNOWFLAKE_PASSWORD=<see Platform Analytics>
% export PYTHONPATH=$(pwd)
```

### Publish a new package

```
% git commit
% git push origin master
% ./scripts/push_version.sh
```

### Training a new model

1. Update version and training table name `<model config>.py` file in `bytegain/custom/cust/apartmentlist/`
2. Update file to reflect new model version and training table name
3. Run the feature analysis and create row handler
  * `python bytegain/custom/cust/apartmentlist/train_model.py --model_config <model config> --feature_analysis`
4. Tweak configuration and iterate
  * `python bytegain/custom/cust/apartmentlist/train_model.py --model_config <model config>`
5. Train the production model and upload the configuration files to S3
  * `python bytegain/custom/cust/apartmentlist/train_model.py --model_config <model config> --production`
