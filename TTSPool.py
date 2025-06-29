# import threading
# from concurrent.futures import ThreadPoolExecutor
# from TTS.api import TTS
# import asyncio
# import SystemConfig
# from TTS.utils.radam import RAdam
# from TTS.config.shared_configs import BaseDatasetConfig
# from builtins import dict
# from collections import defaultdict
# import torch
# import os
# from pathlib import Path
# import uuid
#
# Path("output").mkdir(exist_ok=True)
#
# class TTSThreadWorker:
#     def __init__(self, id):
#         self.id = id
#
#         if not SystemConfig.is_use_gpu:
#             from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
#             from torch.serialization import add_safe_globals
#             from TTS.tts.configs.xtts_config import XttsConfig
#             add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs, defaultdict, dict, RAdam])
#
#         serial_number = f"{uuid.uuid4().hex}"
#         print(f"[Thread {id}]  {serial_number}⏳ 初始化 TTS 模型...")
#         self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=SystemConfig.is_use_gpu)
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.tts.to(device)
#         print(f"[Thread {id}]  {serial_number}✅ TTS 实例初始化完成")
#
#     def synthesize(self, voice_id: str, text: str, output_path: str):
#         print(f"[Thread {self.id}] 开始生成音频")
#
#         if voice_id == "male":
#             self.tts.tts_to_file(
#                 text=text,
#                 speaker_wav="male.wav",
#                 language="zh",
#                 file_path=output_path
#             )
#         elif voice_id == "female":
#             self.tts.tts_to_file(
#                 text=text,
#                 speaker_wav="female.wav",
#                 language="zh",
#                 file_path=output_path
#             )
#         print(f"[Thread {self.id}] ✅ 合成完成：{output_path}")
#
#
# class TTSPool:
#     def __init__(self, num_workers=3):
#         self.num_workers = num_workers
#         self.executor = ThreadPoolExecutor(max_workers=num_workers)
#         self.workers = [TTSThreadWorker(i) for i in range(num_workers)]
#         self._counter = 0
#         self._lock = threading.Lock()
#
#     def _get_next_worker(self):
#         with self._lock:
#             idx = self._counter % self.num_workers
#             self._counter += 1
#             return self.workers[idx]
#
#     async def generate(self, voice_id: str, text: str, output_path: str):
#         loop = asyncio.get_event_loop()
#         worker = self._get_next_worker()
#         await loop.run_in_executor(self.executor, worker.synthesize, voice_id, text, output_path)
