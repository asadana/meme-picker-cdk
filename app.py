#!/usr/bin/env python3

from aws_cdk import core as cdk

from meme_picker.meme_picker_stack import MemePickerStack

app = cdk.App()
MemePickerStack(app, "meme-picker", env={'region': 'us-east-1'})

app.synth()
