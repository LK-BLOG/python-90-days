"""
Challenge 05: 多模态应用 (Boss)
整合图片理解、语音处理和多模态对话。
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from enum import Enum
import base64
import hashlib


class Modality(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"


@dataclass
class MultimodalMessage:
    """多模态消息"""
    role: str
    modality: Modality
    content: str  # 文本内容 / 图片URL / 音频文件路径
    metadata: Dict = field(default_factory=dict)


@dataclass
class AudioResult:
    """语音处理结果"""
    text: str
    language: str = "zh"
    duration: float = 0.0
    segments: List[Dict] = field(default_factory=list)


@dataclass
class ImageAnalysis:
    """图片分析结果"""
    description: str
    objects: List[str] = field(default_factory=list)
    ocr_text: str = ""
    confidence: float = 0.0


class ModalityRouter:
    """模态路由器"""

    @staticmethod
    def detect(input_data: str) -> Modality:
        """自动检测输入类型"""
        # TODO: 根据内容判断是文本/图片URL/音频文件
        # 图片: 以 http 开头且含图片后缀 / 本地图片路径
        # 音频: 以 http 开头且含音频后缀 / 本地音频路径
        # 其他: 文本
        pass


class ImageProcessor:
    """图片处理器"""

    def describe(self, image_path: str) -> str:
        """生成图片描述"""
        # TODO: 模拟图片描述
        pass

    def ocr(self, image_path: str) -> str:
        """图片文字识别"""
        # TODO: 模拟 OCR
        pass

    def analyze(self, image_path: str, question: str = None) -> ImageAnalysis:
        """图片综合分析"""
        # TODO: 结合描述、OCR、问答
        pass


class AudioProcessor:
    """语音处理器"""

    def transcribe(self, audio_path: str) -> AudioResult:
        """语音转文字"""
        # TODO: 模拟 STT
        pass

    def synthesize(self, text: str, voice: str = "alloy") -> str:
        """文字转语音"""
        # TODO: 模拟 TTS，返回"音频文件路径"
        pass

    def voice_chat(self, audio_path: str, system_prompt: str = None) -> str:
        """语音对话: STT → LLM → TTS"""
        # TODO:
        pass


class MultimodalApp:
    """多模态 AI 应用"""

    def __init__(self):
        self.router = ModalityRouter()
        self.image_proc = ImageProcessor()
        self.audio_proc = AudioProcessor()
        self.conversations: Dict[str, List[MultimodalMessage]] = {}
        self._current_conv_id: Optional[str] = None

    def chat(self, user_input: str, conversation_id: str = None) -> Dict:
        """
        统一聊天接口。自动检测输入模态并路由到对应处理器。
        """
        # TODO:
        # 1. 检测输入模态
        # 2. 路由到对应处理器
        # 3. 管理对话历史
        # 4. 返回结构化结果
        pass

    def image_qa(self, image_path: str, question: str,
                 conversation_id: str = None) -> Dict:
        """图片问答"""
        # TODO:
        pass

    def voice_chat(self, audio_path: str,
                   conversation_id: str = None) -> Dict:
        """语音对话"""
        # TODO:
        pass

    def get_conversation(self, conversation_id: str) -> List[Dict]:
        """获取对话历史"""
        # TODO:
        pass

    def clear_conversation(self, conversation_id: str):
        """清空对话"""
        # TODO:
        pass

    def detect_modality(self, input_data: str) -> str:
        """检测输入模态"""
        return self.router.detect(input_data).value


# 测试
if __name__ == "__main__":
    app = MultimodalApp()
    print("模态检测:", app.detect_modality("Hello World"))
    print("模态检测:", app.detect_modality("https://example.com/photo.jpg"))
    print("模态检测:", app.detect_modality("/path/to/audio.mp3"))
    result = app.chat("你好，帮我看看这张图片 https://example.com/cat.jpg")
    print(f"聊天结果: {result}")
