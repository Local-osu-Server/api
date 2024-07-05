# the whole concept is
# the project is the target
# the exrernal third party is the Adaptee (useful, but isn't directly usable)
# These adapters are the bridge between the two, allowing the project (target) to use the Adaptee
from . import osu_daily_api
from . import osu_direct
