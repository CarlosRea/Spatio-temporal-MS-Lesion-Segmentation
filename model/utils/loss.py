import torch
import torch.nn.functional as F

from model.utils import metric_utils


def inf(*args):
    return torch.as_tensor(float("Inf"))


def gradient_loss(s):
    dy = torch.abs(s[:, :, 1:, :] - s[:, :, :-1, :]) ** 2
    dx = torch.abs(s[:, :, :, 1:] - s[:, :, :, :-1]) ** 2
    return (torch.mean(dx) + torch.mean(dy)) / 2.0


def multitask_loss(warp, flow, output, input_fixed, target_fixed):
    recon_loss = mse(warp, input_fixed)
    grad_loss = gradient_loss(flow)
    seg_loss = mse(output, target_fixed)
    return recon_loss + 0.01 * grad_loss + seg_loss


def deformation_loss(warp, flow, input_fixed):
    recon_loss = mse(warp, input_fixed)
    grad_loss = gradient_loss(flow)
    return recon_loss + 0.01 * grad_loss


def l1(output, target):
    return F.l1_loss(output, target)


def mse(output, target):
    return F.mse_loss(output, target)


def nll_loss(output, target):
    return F.nll_loss(metric_utils.flatten(output), metric_utils.flatten(target))


def dice_loss(output, target):
    return metric_utils.asymmetric_loss(1, output, target)


def asymmetric_loss(output, target):
    return metric_utils.asymmetric_loss(2, output, target)


def deep_atlas_loss(
        y_seg_moving, y_seg_fixed, y_deformation, y_seg_deformation, flow,
        target_moving, target_fixed, input_fixed
):
    seg_moving_loss = mse(y_seg_moving, target_moving)
    seg_fixed_loss = mse(y_seg_fixed, target_fixed)
    seg_deformation_loss = mse(y_seg_deformation, target_fixed)
    recon_loss = mse(y_deformation, input_fixed)
    grad_loss = 0.01 * gradient_loss(flow)
    loss = seg_moving_loss + seg_fixed_loss + seg_deformation_loss + recon_loss + grad_loss

    return loss
