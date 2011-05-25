from unittest import defaultTestLoader


for module_name in ['test_mllp']:
    module = __import__(module_name, globals(), level=-1)
    defaultTestLoader.loadTestsFromModule(module)
    
