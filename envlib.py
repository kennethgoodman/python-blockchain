from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

def get_env(var_name, default=''):
	return os.getenv(var_name, default='')
