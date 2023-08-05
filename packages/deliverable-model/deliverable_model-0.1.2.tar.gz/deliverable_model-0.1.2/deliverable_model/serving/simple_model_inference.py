from typing import Tuple, Union, List

from tqdm import tqdm

from deliverable_model.builtin.processor.biluo_decode_processor import PredictResult
from micro_toolkit.data_process.batch_iterator import BatchingIterator
from tokenizer_tools.tagset.offset.sequence import Sequence

from deliverable_model.request import Request
from deliverable_model.serving import DeliverableModel


class SimpleModelInference(object):
    def __init__(self, model_dir, batch_size=1):
        self.batch_size = batch_size

        self.server = DeliverableModel.load(model_dir)

    def _parse(self, msg):
        if not isinstance(msg, list) or not isinstance(msg[0], list):
            msg = [[j for j in i] for i in msg]

        request_obj = Request(msg)

        response_obj = self.server.parse(request_obj)

        for predict_info in response_obj.data:
            yield predict_info

    def parse(self, msg_list: Union[List[str], List[List[str]]]) -> Tuple[Sequence, PredictResult]:
        bi = BatchingIterator(self.batch_size)
        for i in tqdm(bi(msg_list)):
            for j in zip(i, self._parse(i)):
                yield j
