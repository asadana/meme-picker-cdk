from aws_cdk import (
    core as cdk,
    aws_events as events,
    aws_lambda as _lambda,
    aws_events_targets as targets
)


class MemePickerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines a Lambda
        lambda_fn = _lambda.Function(
            self, 'MemePickerLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('resources'),
            handler='lambda_meme_picker.handler',
            timeout=cdk.Duration.seconds(500),
        )

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
