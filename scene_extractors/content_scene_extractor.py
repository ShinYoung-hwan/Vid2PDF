import os
from typing import List
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images
from .base import SceneExtractor

class ContentSceneExtractor(SceneExtractor):
    def __init__(self, threshold: float = 27.0):
        self.threshold = threshold

    def extract_scenes(self, video_path: str, temp_dir: str) -> List[str]:
        video = open_video(video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=self.threshold))
        scene_manager.detect_scenes(video=video)
        scene_list = scene_manager.get_scene_list()
        if not scene_list:
            return []
        save_images(
            scene_list=scene_list,
            video=video,
            num_images=1,
            output_dir=temp_dir,
            image_name_template='$SCENE_NUMBER'
        )
        image_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]
        image_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
        return image_files
