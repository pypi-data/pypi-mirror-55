"""Reading model configurations"""
import argparse
import os
import re
from dataclasses import dataclass, field

import yaml

DEFAULT_TMP_PATH = os.path.expanduser(os.path.join("~", "tmp"))
DEFAULT_DATASETS_PATH = os.path.expanduser(os.path.join("~", "tmp", "datasets"))
DEFAULT_SAVED_MODELS_PATH = "saved_models"
args = None


class ModuleConfigs:
    DATASETS_PATH = os.getenv("DLEX_DATASETS_PATH", DEFAULT_DATASETS_PATH)
    TMP_PATH = os.path.join(os.getenv("DLEX_TMP_PATH", DEFAULT_TMP_PATH), "dlex")
    SAVED_MODELS_PATH = os.getenv("DLEX_SAVED_MODELS_PATH", DEFAULT_SAVED_MODELS_PATH)


@dataclass
class OptimizerConfig:
    """
    Args:
        name (str): One of sgd, adam
    """
    name: str = "sgd"


@dataclass
class TrainConfig:
    """
    :param num_epochs: Number of epochs
    :type num_epochs: int
    :param batch_size: Batch size
    :type batch_size: int
    :param optimizer:
    :type optimizer: OptimizerConfig
    :param lr_scheduler (dict):
    :param eval: List of sets to be evaluated during training. Empty: no evaluation.
        Accepted values: `test`, `dev` (or `valid`).
        If both test and valid sets are presented, the test result for model with best valid result will also be recoreded. `dev` and `valid` can be used interchangeable
    :type eval: list
    :param max_grad_norm:
    :type max_grad_norm: float
    :param save_every: Time interval for saving model. Use s, m, h for number of seconds, minutes, hours. Use e for number of epochs.
            Examples: 100s, 30m, 2h, 1e
    :type save_every: str
    :param log_every: Time interval for logging to file
    :type log_every: str
    """
    num_epochs: int = None
    num_workers: int = None
    batch_size: int = None
    optimizer: OptimizerConfig = None
    lr_scheduler: dict = None
    eval: list = field(default_factory=lambda: ["test"])
    max_grad_norm: float = 5.0
    save_every: str = "1e"
    log_every: str = "5s"
    cross_validation: bool = False


@dataclass
class TestConfig:
    """
    :param batch_size:
    :type batch_size: int
    :param metrics: List of metrics for evaluation.
    :type metrics: list
    """
    batch_size: int = None
    metrics: list = field(default_factory=lambda: ["default"])


class AttrDict(dict):
    """Dictionary with key as property."""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        for key in self:
            if isinstance(self[key], dict):
                self[key] = AttrDict(self[key])

    def __getattr__(self, item: str):
        # logger.warning("Access to unset param %s", item)
        return None

    def set(self, field, value):
        setattr(self, field, value)

    def extend_default_keys(self, d):
        """
        Add key and default values if not existed
        :param d: default key-value pairs
        :return:
        """
        for key in d:
            if isinstance(d[key], dict):
                if key in self:
                    self[key].extend_default_keys(d[key])
                else:
                    setattr(self, key, AttrDict(d[key]))
            else:
                if key not in self:
                    setattr(self, key, d[key])


class MainConfig(AttrDict):
    """Dictionary with key as property."""
    model = None
    dataset = None
    training_id = None
    seed = 1
    shuffle = False
    batch_size = None
    path = None
    train: TrainConfig
    test: TestConfig
    verbose: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "train" in self:
            self.train = TrainConfig(**self['train'])
        if "test" in self:
            self.test = TestConfig(**self['test'])

    def __getattr__(self, item: str):
        # logger.warning("Access to unset param %s", item)
        return None

    def set(self, field, value):
        setattr(self, field, value)

    @property
    def log_dir(self):
        """Get logging directory based on model configs."""
        log_dir = os.path.join("logs", self.path)
        return os.path.join(log_dir, self.training_id)

    @property
    def output_dir(self):
        """Get output directory based on model configs"""
        result_dir = os.path.join(ModuleConfigs.TMP_PATH, "model_outputs", self.path)
        return result_dir


class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
        [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
        |\\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
        |[-+]?\\.(?:inf|Inf|INF)
        |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.')
)


def str2bool(val):
    """Convert boolean argument."""
    if val.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif val.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class Configs:
    """All configurations"""
    params: MainConfig = None
    args = None

    def __init__(self, mode, argv=None):
        self.mode = mode
        self.parse_args(argv)
        self.params = self.get_params()

    def parse_args(self, argv=None):
        """Parse arguments."""
        parser = argparse.ArgumentParser(description="")

        parser.add_argument(
            '-c, --config_path',
            required=True,
            dest="config_path",
            help="path to model's configuration file")
        if self.mode == "train":
            parser.add_argument('--debug', action="store_true",
                                help="train and eval on the same small data to check if the model works")
        parser.add_argument('--download', action="store_true",
                            help="force to download, unzip and preprocess the data")
        parser.add_argument('--preprocess', action="store_true",
                            help="force to preprocess the data")
        parser.add_argument('--no-prepare', action="store_true",
                            help="do not prepare dataset")
        parser.add_argument('--verbose', action="store_true")
        parser.add_argument('-l, --load', dest="load", default=None,
                            required=self.mode in ["eval", "infer"],
                            help="tag of the checkpoint to load")
        parser.add_argument('--cpu', action='store_true', default=False,
                            help='disables CUDA training')

        parser.add_argument('--batch_size', default=None,
                            help="Size of each batch. This will overwrite the value in the config file")
        parser.add_argument(
            '--save_every', default=False,
            help='Save after a certain period of time. Unit: e (epoch), s, m, h (seconds, minutes, hours)')
        parser.add_argument(
            '--log_every', action='store_true', default=False,
            help='Log after a certain period of time. Unit: e (epoch), s, m, h (seconds, minutes, hours)')

        parser.add_argument('--num-workers', type=int, default=0, metavar='N',
                            help="Number of workers for loading data")

        if self.mode == "train":
            parser.add_argument(
                '--num-processes', type=int, default=1, metavar='N',
                help="how many training process to use")
            parser.add_argument(
                '--save-all', action='store_true',
                help='save every epoch')
            parser.add_argument(
                '--exit-on-runtime-error', action="store_true",
                help="Exit when encoutering rumtime error (eg: CUDA out of memery). Exit code: 2")
            parser.add_argument(
                '--output_test_samples', action="store_true",
                help="Output samples after evaluation."
            )
        elif self.mode == "test":
            parser.add_argument(
                "--eval-set", default="test",
                help="Set to evaluate on (test / valid / train)"
            )
        elif self.mode == "infer":
            parser.add_argument(
                '-i --input',
                nargs="*", action="append",
                dest="input")

        if argv is None:
            self.args = parser.parse_args()
        else:
            self.args = parser.parse_args(argv)

    def get_params(self):
        """Load model configs from yaml file"""
        args = self.args
        paths = [
            args.config_path,
            os.path.join("model_configs", args.config_path),
            os.path.join("model_configs", args.config_path + ".yml")
        ]
        paths = [p for p in paths if os.path.exists(p)]
        if not paths:
            raise Exception("Config file '%s' not found." % args.config_path)
        else:
            path = paths[0]
            try:
                with open(path, 'r') as stream:
                    params = yaml.load(stream, Loader=Loader)
                    params = MainConfig(params)
                params.set("mode", self.mode)
                params.set("path", self.args.config_path)
                params.set("verbose", bool(self.args.verbose))

                params.dataset.num_workers = args.num_workers
                if params.train is not None and params.train.num_workers is None:
                    params.train.num_workers = args.num_workers

                # Some config values are overwritten by command arguments
                if args.batch_size is not None:
                    params.train.batch_size = args.batch_size

                return params
            except yaml.YAMLError:
                raise Exception("Invalid config syntax.")

