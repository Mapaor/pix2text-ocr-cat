# coding: utf-8
# [Pix2Text](https://github.com/breezedeus/pix2text): an Open-Source Alternative to Mathpix.
# Copyright (C) 2022-2024, [Breezedeus](https://www.breezedeus.com).
import logging
from typing import Sequence, List, Optional

import numpy as np
import cv2

from .utils import custom_deepcopy

logger = logging.getLogger(__name__)


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
        paddlex_pipeline = getattr(self.ocr_engine, 'paddlex_pipeline', None)
        pipeline = getattr(paddlex_pipeline, '_pipeline', None)
        detector = getattr(pipeline, 'text_det_model', None)
        if detector is not None:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            result = next(iter(detector.predict([img], batch_size=1)), None)
            if result is not None:
                polygons = self._result_value(result, 'dt_polys')
                if polygons is not None:
                    return {
                        'detected_texts': [
                            {'position': np.asarray(polygon)}
                            for polygon in polygons
                        ]
                    }

        return {
            'detected_texts': [
                {'position': box}
                for box, _, _ in self._readtext(img, **kwargs)
            ]
        }

    def recognize_only(self, img: np.ndarray, **kwargs) -> dict:
        # TextFormulaOCR already detected the text boxes. Calling the public
        # OCR pipeline here would run text detection again for every crop.
        paddlex_pipeline = getattr(self.ocr_engine, 'paddlex_pipeline', None)
        pipeline = getattr(paddlex_pipeline, '_pipeline', None)
        recognizer = getattr(pipeline, 'text_rec_model', None)
        if recognizer is not None:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            results = recognizer.predict([img], batch_size=1)
            result = next(iter(results), None)
            if result is not None:
                text = self._result_value(result, 'rec_text')
                score = self._result_value(result, 'rec_score')
                if text is not None and score is not None:
                    return {'text': text, 'score': float(score)}

        out = {'text': '', 'score': 0.0}
        results = self._readtext(img, **kwargs)
        if results:
            _, text, score = results[0]
            out = {'text': text, 'score': score}
        return out

    def recognize_batch(self, imgs: Sequence[np.ndarray], **kwargs) -> List[dict]:
        paddlex_pipeline = getattr(self.ocr_engine, 'paddlex_pipeline', None)
        pipeline = getattr(paddlex_pipeline, '_pipeline', None)
        recognizer = getattr(pipeline, 'text_rec_model', None)
        if recognizer is None:
            return [self.recognize_only(img, **kwargs) for img in imgs]

        images = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in imgs]
        results = recognizer.predict(images, batch_size=min(2, len(images)))
        return [
            {
                'text': self._result_value(result, 'rec_text') or '',
                'score': float(self._result_value(result, 'rec_score') or 0.0),
            }
            for result in results
        ]

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
        results = self.ocr_engine.predict(img, **kwargs)
        outputs = []
        for result in results:
            polygons = self._result_value(result, 'rec_polys', 'dt_polys')
            texts = self._result_value(result, 'rec_texts')
            scores = self._result_value(result, 'rec_scores')
            if polygons is None or texts is None or scores is None:
                continue
            outputs.extend(
                (np.asarray(polygon), text, float(score))
                for polygon, text, score in zip(polygons, texts, scores)
            )
        return outputs

    @staticmethod
    def _result_value(result, *names):
        for name in names:
            try:
                value = result[name]
            except (KeyError, TypeError):
                value = getattr(result, name, None)
            if value is not None:
                return value
        return None


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
        ocr_engine_config.setdefault('use_doc_orientation_classify', False)
        ocr_engine_config.setdefault('use_doc_unwarping', False)
        ocr_engine_config.setdefault('use_textline_orientation', False)
        ocr_engine = PaddleOCR(lang=languages[0], device='cpu', **ocr_engine_config)
        engine_wrapper = PaddleOCREngine(languages, ocr_engine)
        logger.info('Using PaddleOCR for languages: %s', ', '.join(languages))
    else:
        raise ValueError(f'Unsupported text OCR engine: {engine_name}')
    return engine_wrapper
