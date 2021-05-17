from aws_cdk import (
    core as cdk,
    aws_events as events,
    aws_lambda as _lambda,
    aws_lambda_python as _lambda_py,
    aws_events_targets as targets,
    aws_s3 as s3
)


class MemePickerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket
        s3_bucket = s3.Bucket(self,
                              'MemeBucket',
                              encryption=s3.BucketEncryption.S3_MANAGED,
                              public_read_access=False,
                              versioned=True,
                              lifecycle_rules=[
                                  s3.LifecycleRule(
                                      expiration=cdk.Duration.days(30),
                                      noncurrent_version_expiration=cdk.Duration.days(30)
                                  )
                              ])

        # Defines a Lambda
        lambda_fn = _lambda_py.PythonFunction(
            self, 'MemePickerLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            entry="lambda_meme_picker",
            index="main.py",
            timeout=cdk.Duration.seconds(500),
            environment={
                "S3_BUCKET_NAME": s3_bucket.bucket_name
            }
        )
        s3_bucket.grant_write(lambda_fn)

        # Run every Friday
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='0',
                month='*',
                week_day='FRI',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambda_fn))
