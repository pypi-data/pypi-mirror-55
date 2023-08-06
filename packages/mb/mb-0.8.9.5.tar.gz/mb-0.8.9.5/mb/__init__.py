from .files.yota import Yota, Cue, Sample, Mixtape
from .files.bit import Link, Mp3
from .files.lib import Convert
from .files import cnf
#from .files.yota_fuzz import main as yota_fuzz
#from .files.bit_fuzz import main as bit_fuzz
#from .files.ono import check_ono as ono
from .files.onoObject import MediabyteHashObj


omm = Convert.omm
youtube = Convert.search_to_mixtape
search = Convert.search
history = Convert._search_history("")
#regex = Convert.regex_search

input = Convert.omm
version = Convert.version()
readme = Convert.readme()
docs = Convert.docs
summary = cnf.summary