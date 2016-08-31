import os 
from progue import client

client.set_save_dir(os.path.dirname(os.path.abspath(__file__)))
client.run()