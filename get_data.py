from decouple import config
from binance.client import Client
from datetime import datetime as dt
import pandas as pd
import sys
import argparse
from tabulate import tabulate

# import API keys from .env
API_KEY_B = config('API_KEY_B')
SECRET_KEY_B = config('SECRET_KEY_B')

print(API_KEY_B)