import os
import sys

vision_service_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vision_service')
if vision_service_path not in sys.path:
    sys.path.append(vision_service_path)
