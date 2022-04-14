import os

CONFIG = {
    "name": f"{os.path.basename(__file__).split('.')[0]}",
    "n_gpu": 1,

    "arch": {
        "type": "MultitaskNetwork",
        "args": {
            "in_channels": 2,
            "resolution": (218, 218)
        }
    },
    "dataset": {
        "type": "DatasetLongitudinal",
        "args": {
            "data_dir": "../train/",
            "preprocess": True,
            "modalities": ['flair'],
            "val_patients": [4]
        }
    },
    "data_loader": {
        "type": "Dataloader",
        "args": {
            "batch_size": 2,
            "shuffle": True,
            "num_workers": 4,
        }
    },
    "optimizer": {
        "type": "Adam",
        "args": {
            "lr": 0.0001,
            "weight_decay": 0,
            "amsgrad": True
        }
    },
    "loss": "multitask_loss",
    "metrics": [
        "precision", "recall", "dice_loss", "dice_score", "asymmetric_loss"
    ],
    "lr_scheduler": {
        "type": "StepLR",
        "args": {
            "step_size": 50,
            "gamma": 0.1
        }
    },
    "trainer": {
        "type": "LongitudinalMultitaskTrainer",
        "epochs": 100,
        "save_dir": "../saved/",
        "save_period": 1,
        "verbosity": 2,
        "monitor": "min val_dice_loss",
        "early_stop": 10,
        "tensorboard": True
    }
}
