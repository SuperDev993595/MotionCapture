import os
  

def test_envs_available():
    variable = os.environ.get("ENVIRONMENT")
    assert variable is not None
    print("test_envs_available")