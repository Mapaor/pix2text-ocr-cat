# coding: utf-8
# [Pix2Text](https://github.com/breezedeus/pix2text): an Open-Source Alternative to Mathpix.
# Copyright (C) 2022-2024, [Breezedeus](https://www.breezedeus.com).
from typing import Sequence, List, Optional

import numpy as np
import cv2

from .utils import custom_deepcopy


class TextOcrEngine:
    """Text OCR Engine Wrapper"""

    name = 'unknown'

    def __init__(self, languages: Sequence[str], ocr_engine):
        self.languages = languages
        self.ocr_engine = ocr_engine

    def detect_only(self, img: np.ndarray, **kwargs):
        """
        Only detect the texts from the input image.
        Args:
            img (np.ndarray): RGB image with shape: (height, width, 3)
            kwargs: more configs

        Returns:
            Dict[str, List[dict]]: The dictionary contains the following keys:
               * 'detected_texts': list, each element stores the information of a detected box, recorded in a dictionary, including the following values:
                   'position': The rectangular box corresponding to the detected text; np.ndarray, shape: (4, 2), representing the coordinates (x, y) of the 4 points of the box;

                 Example:
                   {'detected_texts':
                       [{'position': array([[416,  77],
                                       [486,  13],
                                       [800, 325],
                                       [730, 390]], dtype=int32),
                        },
                        ...
                       ]
                   }
        """
        pass

    def recognize_only(self, img: np.ndarray, **kwargs):
        """
        Only recognize the texts for cropped images, which are from bboxes detected by detect_only.
        Args:
            img (): RGB image with shape [height, width] or [height, width, channel].
                    channel should be 1 (gray image) or 3 (RGB formatted color image). scaled in [0, 255];
            kwargs: more configs

        Returns:
            dict, with keys:
                - 'text' (str): The recognized text
                - 'score' (float): The score of the recognition result (confidence level), ranging from `[0, 1]`; the higher the score, the more reliable it is

            Example:
            ```
             {'score': 0.8812797665596008,
              'text': 'Current Line'}
            ```
        """
        pass

    def ocr(self, img: np.ndarray, rec_config: Optional[dict] = None, **kwargs):
        """
        Detect texts first, and then recognize the texts for detected bbox patches.
        Args:
            img (np.ndarray): RGB image with shape [height, width] or [height, width, channel].
                    channel should be 1 (gray image) or 3 (RGB formatted color image). scaled in [0, 255];
            rec_config (Optional[dict]): The config for recognition
            kwargs: more configs

        Returns:
            list of detected texts, which element is a dict, with keys:
                - 'text' (str): The recognized text
                - 'score' (float): The score of the recognition result (confidence level), ranging from `[0, 1]`; the higher the score, the more reliable it is
                - 'position' (np.ndarray): 4 x 2 array, representing the coordinates (x, y) of the 4 points of the box

            Example:
            ```
             [{'score': 0.88,
              'text': 'Line 1',
              'position': array([[146, 22],
                                 [179, 22],
                                 [179, 60],
                                 [146, 60]], dtype=int32)
              },
              {'score': 0.78,
              'text': 'Line 2'
              'position': array([[641, 115],
                                 [1180, 115],
                                 [1180, 244],
                                 [641, 244]], dtype=int32)
              }]
            ```
        """

        pass


class CnOCREngine(TextOcrEngine):
    name = 'cnocr'

    def detect_only(self, img: np.ndarray, **kwargs):
        outs = self.ocr_engine.det_model.detect(img, **kwargs)
        for out in outs['detected_texts']:
            out['position'] = out.pop('box')
        return outs

    def recognize_only(self, img: np.ndarray, **kwargs):
        try:
            return self.ocr_engine.ocr_for_single_line(img)
        except:
            return {'text': '', 'score': 0.0}

    def ocr(self, img: np.ndarray, rec_config: Optional[dict] = None, **kwargs) -> str:
        rec_config = rec_config or {}
        outs = self.ocr_engine.ocr(img, **rec_config)
        return outs


class PaddleOCREngine(TextOcrEngine):
    name = 'paddleocr'

    def detect_only(self, img: np.ndarray, **kwargs):
        return {
            'detected_texts': [
                {'position': box}
                for box, _, _ in self._readtext(img, **kwargs)
            ]
        }

    def recognize_only(self, img: np.ndarray, **kwargs) -> dict:
        out = {'text': '', 'score': 0.0}
        results = self._readtext(img, **kwargs)
        if results:
            _, text, score = results[0]
            out = {'text': text, 'score': score}
        return out

    def ocr(
        self, img: np.ndarray, rec_config: Optional[dict] = None, **kwargs
    ) -> List[dict]:
        read_config = {**(rec_config or {}), **kwargs}
        results = self._readtext(img, **read_config)
        outs = []
        for box, text, score in results:
            outs.append({'text': text, 'score': score, 'position': box})
        return outs

    def _readtext(self, img: np.ndarray, **kwargs) -> List[tuple]:
        kwargs.pop('resized_shape', None)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        results = self.ocr_engine.ocr(img, cls=True, **kwargs)
        if not results or not results[0]:
            return []
        return [
            (np.asarray(result[0]), result[1][0], float(result[1][1]))
            for result in results[0]
        ]


def prepare_ocr_engine(languages: Sequence[str], ocr_engine_config):
    ocr_engine_config = custom_deepcopy(ocr_engine_config) if ocr_engine_config else {}
    engine_name = ocr_engine_config.pop('engine', 'paddleocr')
    if engine_name == 'cnocr':
        from cnocr import CnOcr

        if tuple(languages) == ('en',):  # only recognize english characters
            if 'det_model_name' not in ocr_engine_config:
                ocr_engine_config['det_model_name'] = 'en_PP-OCRv3_det'
            if 'rec_model_name' not in ocr_engine_config:
                ocr_engine_config['rec_model_name'] = 'en_PP-OCRv3'
        ocr_engine = CnOcr(**ocr_engine_config)
        engine_wrapper = CnOCREngine(languages, ocr_engine)
    elif engine_name == 'paddleocr':
        try:
            from paddleocr import PaddleOCR
        except ImportError as exc:
            raise ImportError('Please install paddleocr and paddlepaddle first') from exc
        ocr_engine_config.pop('context', None)
        ocr_engine_config.setdefault('use_angle_cls', True)
        ocr_engine = PaddleOCR(lang=languages[0], use_gpu=False, **ocr_engine_config)
        engine_wrapper = PaddleOCREngine(languages, ocr_engine)
    else:
        raise ValueError(f'Unsupported text OCR engine: {engine_name}')
    return engine_wrapper
