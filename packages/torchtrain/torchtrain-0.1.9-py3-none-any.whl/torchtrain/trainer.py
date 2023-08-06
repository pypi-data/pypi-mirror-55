import os
from collections import defaultdict
from datetime import datetime

import torch
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from . import utils
from .callbacks import EarlyStop


class Trainer:
    """Supervised trainer.

    Parameters
    ----------
    config : dict
        'max_train_epoch' : int
        'early_stop_patience' : int
        'watching_metric' : str
            Metric to monitor for early stop and lr scheduler.
        'watch_mode' : str, ['min', 'max']
        'cuda_list' : str
            E.g. '1,3'. Will be used like `config["cuda_list"][0]` and
            `eval(config["cuda_list"])`.
        'save_path' : str
            Create a subfolder using current datetime.
            Best checkpoint and tensorboard logs are saved inside.
        'early_stop_verbose' : bool, optional
            If True, early stop print verbose message. Default to False.
        'tqdm' : bool, optional
            If True, tqdm progress bar for batch iteration. Default to False.
        'data_parallel_dim' : int, optional
            Default to 0.
        'train_one_epoch' : bool, optional
            If True, only train one epoch for testing code. Default to False.
    data_iter : dict
        'train', 'val', 'test' : iterator
            Data iterators should be on the right device beforehand.
    model, optimizer : torch
        PyTorch model, optimizer.
    criteria : dict
        Other criterions will be calculated as well.
        'loss' : function
            Calculate loss for `backward()`.
    scheduler : torch, optional
        PyTorch scheduler.
    hparams_to_save, metrics_to_save : list[str]
        Save to tensorboard hparams. Default to not save hparams.
    batch_to_xy : function
        Will be used as `inputs, labels = self.batch_to_xy(batch, phase)`.
    """

    def __init__(
        self,
        config,
        data_iter,
        model,
        optimizer,
        criteria,
        scheduler=None,
        hparams_to_save=None,
        metrics_to_save=None,
        batch_to_xy=lambda batch, phase: batch,
    ):
        self.data_iter = data_iter
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criteria = criteria
        self.hparams_to_save = hparams_to_save
        self.metrics_to_save = metrics_to_save
        self.batch_to_xy = batch_to_xy
        self.config = self.append_config(config)
        self.model = utils.distribute_model(model, self.config)
        self.writer = SummaryWriter(self.config["save_path"])

    def append_config(self, config):
        config = defaultdict(bool, config)
        config["device"] = (
            "cuda:" + config["cuda_list"][0]
            if (torch.cuda.is_available() and config["cuda_list"])
            else "cpu"
        )
        config["save_path"] = os.path.join(
            config["save_path"], datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        )
        config["checkpoint_path"] = os.path.join(
            config["save_path"], "checkpoint.pt"
        )
        config["data_parallel_dim"] = int(config["data_parallel_dim"])
        if config["train_one_epoch"]:
            config["max_train_epoch"] = 1
        return config

    def current_stats(
        self, phase, epoch, tqdm_wrapper, reset=False, write=False
    ):
        metrics = {}
        desc = f" epoch: {epoch:3d} "
        for name, criterion in self.criteria.items():
            metric = criterion.value(reset)
            metrics[f"{name}/{phase}"] = metric
            desc += f"{name}_{phase:5s}: {metric:.6f} "
            if write:
                self.writer.add_scalar(f"{name}/{phase}", metric, epoch)
        self.writer.flush()
        tqdm_wrapper.set_description(desc)
        return metrics

    def iter_batch(self, phase, epoch=1):
        is_train = phase == "train"
        self.model.train(is_train)
        data_iter = tqdm(
            self.data_iter[phase], desc=phase, disable=not self.config["tqdm"]
        )
        for batch in data_iter:
            inputs, labels = self.batch_to_xy(batch, phase)
            if is_train:
                self.optimizer.zero_grad()
            with torch.set_grad_enabled(is_train):
                outputs = self.model(inputs)
                for criterion in self.criteria.values():
                    criterion.update(outputs, labels)
            if is_train:
                self.criteria["loss"].batch_score().backward()
                self.optimizer.step()
            self.current_stats(phase, epoch, data_iter)
        metrics = self.current_stats(
            phase, epoch, data_iter, reset=True, write=True
        )
        return metrics

    def schedule_lr(self, epoch, metrics):
        if self.scheduler:
            metric = metrics[self.config["watching_metric"]]
            self.writer.add_scalar(
                "lr",
                [group["lr"] for group in self.optimizer.param_groups][0],
                epoch,
            )
            self.scheduler.step(metric)

    def save_hparams(self, best_metrics):
        if self.hparams_to_save:
            self.writer.add_hparams(
                utils.filter_dict(self.config, self.hparams_to_save),
                utils.filter_dict(best_metrics, self.metrics_to_save),
            )
            self.writer.flush()

    def train(self):
        early_stopper = EarlyStop(self.config, self.model)
        for epoch in range(1, self.config["max_train_epoch"] + 1):
            metrics = {
                **self.iter_batch("train", epoch),
                **self.iter_batch("val", epoch),
            }
            if early_stopper.check(metrics):
                break
            self.schedule_lr(epoch, metrics)
        self.save_hparams(early_stopper.best_metrics)

    def test(self, checkpoint_path=None):
        if not checkpoint_path:
            checkpoint_path = self.config["checkpoint_path"]
        self.model.load_state_dict(torch.load(checkpoint_path))
        metrics_test = self.iter_batch("test")
        self.writer.add_hparams(
            utils.filter_dict(self.config, self.hparams_to_save), metrics_test
        )
        self.writer.flush()
        return metrics_test
