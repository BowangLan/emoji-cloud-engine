import os

parent_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(parent_dir, "data")
# vendor_dir_list = os.listdir(data_dir)
print("data_dir = %s" % data_dir)