from oauth_dropins.appengine_config import *

# Suppress warnings. These are duplicated in oauth-dropins and bridgy; keep them
# in sync!
import warnings
warnings.filterwarnings('ignore', module='bs4',
                        message='No parser was explicitly specified')
warnings.filterwarnings('ignore', message='urllib3 is using URLFetch')
warnings.filterwarnings('ignore',
                        message='URLFetch does not support granular timeout')
warnings.filterwarnings('ignore',
                        message='.*No parser was explicitly specified.*')
