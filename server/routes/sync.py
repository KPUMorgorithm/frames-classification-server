from datetime import datetime, timedelta
from flask import request, Blueprint
from server.tools.face_tool import FaceTool

from server.db.db import  DB

from server.store.checklistStore import Checklist, MemberDict

from server.tools.mask_detector import MaskDetector

import numpy as np
import cv2

ft = FaceTool.instance()
bp = Blueprint('sync', __name__, url_prefix='/sync')

@bp.route('/', methods=['POST'], strict_slashes=False)
def sync():
    ft.sync()
    return {'data': "ok"}, 200