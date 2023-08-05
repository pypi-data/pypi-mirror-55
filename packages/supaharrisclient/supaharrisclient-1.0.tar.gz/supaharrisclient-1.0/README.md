# supaharris-client

**API client for the supaharris.com globular and star cluster database**

[![Software license](http://img.shields.io/badge/license-AGPL3-brightgreen.svg)](https://github.com/tlrh314/supaharris/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/tlrh314/supaharris-client.svg?branch=master)](https://travis-ci.org/tlrh314/supaharris-client)


# Usage with https://www.supaharris.com

```python
from supaharrisclient import SupaHarrisClient

shc = SupaHarrisClient()

shc.print_parameters()
shc.print_astro_object_classifications()
shc.print_astro_objects()

print("\nRetrieved {0} references".format(len(shc.references)))
print("\nReference 0\n  {0:<25s}{1}".format("Key", "Value"))
for k, v in shc.references_json[0].items():
    print("  {0:<25s}{1}".format(k, v))

print("shc.observations.shape:\n{}\n".format(shc.observations.shape))
print("shc.observations.dtype:\n{}\n".format(shc.observations.dtype))
print("shc.observations['RA']:\n{}\n".format(shc.observations['RA']))
print("shc.observations_ref['RA']:\n{}\n".format(shc.observations_ref['RA']))
```

# Usage with local development setup
```python

from supaharrisclient import SupaHarrisClient

shc = SupaHarrisClient(base_url="https://nginx/api/v1/", verify=False)
shc.print_parameters()
```
