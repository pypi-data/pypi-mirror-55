import os
import random
from typing import Optional, Union, List
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

from .hparams import HParams, Spec
from .utils import Nop


class Experiment:
  def __init__(self,
               seed: Optional[int] = None,
               log_dir: Optional[str] = None,
               log_int: int = 100,
               ckpt_int: int = 100):

    self._seed = self._set_seeds(seed)

    self._cuda = torch.cuda.is_available()

    self._logging = self._prep_workspace(log_dir, log_int, ckpt_int)
    self._init_logger()

  @staticmethod
  def spec_list() -> List[Spec]:
    '''
    A list of named-tuples containing name
    of the spec, number of trials to generate
    and an arbitrary parameter dictionary. See examples.
    '''
    raise NotImplementedError

  def run(self):
    raise NotImplementedError

  @property
  def seed(self) -> Optional[int]:
    return self._seed

  @property
  def cuda(self) -> bool:
    return self._cuda

  @property
  def log_dir(self) -> Optional[str]:
    return self._logging.get('log_dir')

  @property
  def log_interval(self) -> int:
    return self._logging.get('log_int')

  @property
  def ckpt_interval(self) -> int:
    return self._logging.get('ckpt_int')

  @property
  def tb(self) -> Union[SummaryWriter, Nop]:
    return self._logging.get('tb', Nop())

  @classmethod
  def generate(cls, trials_dir: str):
    hparams = HParams(cls)
    hparams.save_trials(trials_dir)

  def _set_seeds(self, seed: Optional[int]) -> Optional[int]:
    if seed:
      torch.manual_seed(seed)
      torch.cuda.manual_seed_all(seed)
      np.random.seed(seed)
      random.seed(seed)
    return seed

  def _init_logger(self):
    if self.log_dir:
      self._logging['tb'] = SummaryWriter(self.log_dir)

  def _prep_workspace(self, log_dir: str, log_int: int = 100,
                      ckpt_int: int = 100) -> dict:
    logging = {
        'log_int': log_int,
        'ckpt_int': ckpt_int,
    }

    if log_dir:
      log_dir = os.path.abspath(log_dir)
      logging['log_dir'] = log_dir

      os.makedirs(logging['log_dir'], exist_ok=True)

    return logging
