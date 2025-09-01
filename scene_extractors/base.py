from abc import ABC, abstractmethod
from typing import List

class SceneExtractor(ABC):
    @abstractmethod
    def extract_scenes(self, video_path: str, temp_dir: str) -> List[str]:
        """
        비디오에서 장면을 추출하고, 대표 이미지를 temp_dir에 저장한 뒤 이미지 파일 경로 리스트를 반환합니다.
        """
        pass
