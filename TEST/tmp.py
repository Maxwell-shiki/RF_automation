import pyvisa as visa

rm = visa.ResourceManager()

print(rm.list_resources())
# how to clear cache? old resources are still there

rm.close()

