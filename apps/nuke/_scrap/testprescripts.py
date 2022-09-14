import nukepub.publish_scenes_ui as publish_scenes_ui
from six.moves import reload_module as reload  # type: ignore


import pp_project.project as project

import pp_io.util as iopubutil
import common


reload(common)
reload(iopubutil)
reload(publish_scenes_ui)
reload(project)


publish_scenes_ui.main()
