import torch
import math
from torch import nn
import torch.nn.functional as F
import numpy as np


def distillation_loss(y, labels, teacher_scores, T, alpha, reduction_kd='mean', reduction_nll='mean'):
    #if teacher_scores is not None and y.dtype != teacher_scores.dtype:
    #    teacher_scores = teacher_scores.half()

    if teacher_scores is not None:
        d_loss = nn.KLDivLoss(reduction=reduction_kd)(F.log_softmax(y / T, dim=1),
                                                      F.softmax(teacher_scores / T, dim=1)) * T * T
    else:
        assert alpha == 0, 'alpha cannot be {} when teacher scores are not provided'.format(alpha)
        d_loss = 0.0

    if y.shape[1] == 1:
        nll_loss = F.mse_loss(y.view(-1), labels.view(-1))
    else:
        nll_loss = F.cross_entropy(y, labels.long(), reduction=reduction_nll)
    # nll_loss = F.cross_entropy(y, labels.long(), reduction=reduction_nll)
    # print(d_loss.shape, d_loss)
    # print('\n', nll_loss.shape, nll_loss)

    tol_loss = alpha * d_loss + (1.0 - alpha) * nll_loss
    # print('in func:', d_loss.item(), nll_loss.item(), alpha, tol_loss.item())
    return tol_loss, d_loss, nll_loss


def patience_loss(teacher_patience, student_patience, normalized_patience=False):
    # n_batch = teacher_patience.shape[0]
    if normalized_patience:
        teacher_patience = F.normalize(teacher_patience, p=2, dim=2)
        student_patience = F.normalize(student_patience, p=2, dim=2)
    return F.mse_loss(teacher_patience.float(), student_patience.float()).half()

    # diff = (teacher_patience - student_patience).pow(2).sum()
    # const = math.sqrt(teacher_patience.numel())
    # return diff / const / const

def matching_alignment(t_embed, s_embed, only_cls=False):
    def compute_gcd(x, y):
        while y != 0:
            (x, y) = (y, x % y)
        return x

    gcd = compute_gcd(len(t_embed)-1, len(s_embed)-1)
    step_t = int((len(t_embed)-1) / gcd)
    step_s = int((len(s_embed)-1) / gcd)
    # t_embed = torch.cat((t_embed[0].unsqueeze(1),torch.stack(t_embed[step_t::step_t], dim=1)), dim=1)
    # s_embed = torch.cat((s_embed[0].unsqueeze(1),torch.stack(s_embed[step_s::step_s], dim=1)), dim=1)
    # s_embed = s_embed[:, 1:, :, :]
    return t_embed, s_embed

def batch_pairwise_squared_distance(x, squared=False):
    bsz, max_len, dim = x.size()
    x_sq = (x**2).sum(dim=2)
    prod = torch.bmm(x, x.transpose(1,2))
    dist = (x_sq.unsqueeze(1) + x_sq.unsqueeze(2) - 2*prod).clamp(min=1e-12)
    if squared == True:
        dist = torch.sqrt(dist).clone()
    #dist[dist!=dist] = 0
    dist[:, range(max_len), range(max_len)] = 0
    return dist


class WR_Dist(nn.Module):
    def __init__(self):
        super(WR_Dist, self).__init__()

    def forward(self, t_embed, s_embed, attention_mask, distance, lossfunc, normalize=False, squard=False):
        bsz, layer_num, max_len, dim = t_embed.size()
        _, _, _, sdim = s_embed.size()
        t_embed = t_embed.reshape(-1, max_len, dim)
        s_embed = s_embed.reshape(-1, max_len, sdim)
        mask = self.make_mask(attention_mask, layer_num)
        mask = mask.reshape(-1, max_len, max_len)
        with torch.no_grad():
            if distance == "cos":
                t_norm = F.normalize(t_embed, p=2, dim=2)
                t_d = torch.bmm(t_norm, t_norm.transpose(1, 2))

                t_d = t_d * mask
                diagonal = (torch.ones(max_len, max_len) - torch.eye(max_len, max_len)).to(t_embed.device)
                t_d = t_d.masked_fill(diagonal == 0, -np.inf)
                t_d = t_d.masked_fill(mask == 0, -np.inf)
                t_d = F.softmax(t_d, dim=-1)
                t_d = t_d * mask
            elif distance == "l2":
                t_d = batch_pairwise_squared_distance(t_embed, squared=False)
                if normalize:
                    t_d = t_d * mask
                    nonzero = torch.sum((t_d.view(bsz * layer_num, -1) > 0), dim=-1)
                    mean_td = t_d.view(bsz * layer_num, -1).sum(dim=-1) / nonzero
                    t_d = t_d / mean_td.unsqueeze(1).unsqueeze(2)
                else:
                    t_d = t_d * mask
        if distance == "cos":
            s_norm = F.normalize(s_embed, p=2, dim=2)
            s_d = torch.bmm(s_norm, s_norm.transpose(1, 2))

            s_d = s_d * mask
            s_d = s_d.masked_fill(diagonal == 0, -np.inf)
            s_d = s_d.masked_fill(mask == 0, -np.inf)
            s_d = F.log_softmax(s_d, dim=-1)
            s_d = s_d * mask

        elif distance == "l2":
            s_d = batch_pairwise_squared_distance(s_embed, squared=False)
            if normalize:
                s_d = s_d * mask
                nonzero = torch.sum((s_d.view(bsz * layer_num, -1) > 0), dim=-1)
                mean_sd = s_d.view(bsz * layer_num, -1).sum(dim=-1) / nonzero
                s_d = s_d / mean_sd.unsqueeze(1).unsqueeze(2)
            else:
                s_d = s_d * mask

        if lossfunc == "kldiv":
            return F.kl_div(s_d, t_d, reduction="sum") / mask.sum().item()
        elif lossfunc == "l1loss":
            return F.l1_loss(s_d, t_d, reduction='sum') / mask.sum().item()
        elif lossfunc == "l2loss":
            return F.mse_loss(s_d, t_d, reduction='sum') / mask.sum().item()
        elif lossfunc == 'smoothl1':
            return F.smooth_l1_loss(s_d, t_d, reduction='sum') / mask.sum().item()

    def make_mask(self, attention_mask, layers):
        mask = attention_mask.unsqueeze(2) * attention_mask.unsqueeze(1)
        return mask.unsqueeze(1).repeat(1, layers, 1, 1).float()

def window_index(w_size, bsz, length):

    w_size_2 = (w_size - 1)/2
    idx = torch.arange(0, length).unsqueeze(0).unsqueeze(2).repeat(bsz, 1, w_size)
    idx_range = torch.range(-w_size_2, w_size_2).expand_as(idx)
    idx = idx + idx_range
    idx = torch.clamp(idx, 0, length-1)
    idx_base = torch.arange(0, bsz).view(-1,1,1)*length
    idx = (idx + idx_base)
    return idx

class WR_Angle_window(nn.Module):
    def __init__(self):
        super(WR_Angle_window, self).__init__()
    def forward(self, t_embed, s_embed, attention_mask, lossfunc, window=5):
        assert (window % 2) == 1
        bsz, layer_num, max_len, dim = t_embed.size()
        bsz, layer_num, max_len, sdim = s_embed.size()
        t_embed = t_embed.reshape(-1, max_len, dim)
        s_embed = s_embed.reshape(-1, max_len, sdim)
        new_bsz = bsz * layer_num
        idx = window_index(window, new_bsz, max_len)
        #idx = idx.long().unsqueeze(1).repeat(1, layer_num,1,1).view(-1, max_len, window)
        idx = idx.long()
        t_round_emb = t_embed.reshape(new_bsz*max_len, -1)[idx, :]
        s_round_emb = s_embed.reshape(new_bsz*max_len, -1)[idx, :]
        mask = self.make_mask(attention_mask, layer_num, window)
        mask = mask.view(-1, max_len, window, window)

        with torch.no_grad():
            t_sub = (t_embed.unsqueeze(2) - t_round_emb)
            # bsz, len, window, window, dim
            t_sub = F.normalize(t_sub, p=2, dim=3).view(-1, window, dim)
            t_angle = torch.bmm(t_sub, t_sub.transpose(1,2)).view(new_bsz, max_len, window, window)
            t_angle = t_angle * mask
        s_sub = (s_embed.unsqueeze(2) - s_round_emb)   #2737
        s_sub = F.normalize(s_sub, p=2, dim=3).view(-1, window, sdim)   #3169
        s_angle = torch.bmm(s_sub, s_sub.transpose(1,2)).view(new_bsz, max_len, window, window)
        s_angle = s_angle * mask

        if lossfunc == "l1loss":
            return F.l1_loss(s_angle, t_angle, reduction='sum') / mask.sum().item()
        elif lossfunc == "l2loss":
            return F.mse_loss(s_angle, t_angle, reduction='sum') / mask.sum().item()
        elif lossfunc == "smoothl1":
            return F.smooth_l1_loss(s_angle, t_angle, reduction='sum') / mask.sum().item()

    def make_mask(self, attention_mask, layers, window):
        mask = attention_mask.unsqueeze(2).unsqueeze(3).repeat(1,1,window,window)
        return mask.unsqueeze(1).repeat(1,layers,1,1,1).float()


class LTR_Dist(nn.Module):
    def __init__(self):
        super(LTR_Dist, self).__init__()

    def forward(self, t_embed, s_embed, attention_mask, distance, lossfunc, normalize=False, squard=False):
        bsz, layer_num, max_len, dim = t_embed.size()
        bsz, layer_num, max_len, sdim = s_embed.size()
        t_embed = t_embed.transpose(1, 2).reshape(-1, layer_num, dim)
        s_embed = s_embed.transpose(1, 2).reshape(-1, layer_num, sdim)

        mask = self.make_mask(attention_mask, layer_num).view(-1, layer_num, layer_num)
        mask = mask.view(-1, layer_num, layer_num)

        with torch.no_grad():
            if distance == "cos":
                t_norm = F.normalize(t_embed, p=2, dim=2)
                t_d = torch.bmm(t_norm, t_norm.transpose(1, 2))
                t_d = t_d * mask
                diagonal = (torch.ones(layer_num, layer_num) - torch.eye(layer_num, layer_num)).to(t_embed.device)
                t_d = t_d.masked_fill(diagonal == 0, -np.inf)
                t_d = t_d.masked_fill(mask == 0, -np.inf)
                # t_d = t_d.masked_fill(t_d == 1.0, -np.inf)
                t_d = F.softmax(t_d, dim=-1)
                t_d = t_d * mask

            elif distance == "l2":
                t_d = batch_pairwise_squared_distance(t_embed, squared=False)
                if normalize:
                    t_d = t_d * mask
                    nonzero = torch.sum((t_d.view(bsz * max_len, -1) > 0), dim=-1)
                    nonzero[nonzero == 0] = 1
                    mean_td = t_d.view(bsz * max_len, -1).sum(dim=-1) / nonzero
                    mean_td[mean_td == 0] = 1
                    t_d = t_d / mean_td.unsqueeze(1).unsqueeze(2)
                else:
                    t_d = t_d * mask
        if distance == "cos":
            s_norm = F.normalize(s_embed, p=2, dim=2)
            s_d = torch.bmm(s_norm, s_norm.transpose(1, 2))
            s_d = s_d * mask
            s_d = s_d.masked_fill(diagonal == 0, -np.inf)
            s_d = s_d.masked_fill(mask == 0, -np.inf)
            # s_d = s_d.masked_fill(s_d == 1.0, -np.inf)
            s_d = F.log_softmax(s_d, dim=-1)
            s_d = s_d * mask

        elif distance == "l2":
            s_d = batch_pairwise_squared_distance(s_embed, squared=False)
            if normalize:
                s_d = s_d * mask
                nonzero = torch.sum((s_d.view(bsz * max_len, -1) > 0), dim=-1)
                nonzero[nonzero == 0] = 1
                mean_sd = s_d.view(bsz * max_len, -1).sum(dim=-1) / nonzero
                mean_sd[mean_sd == 0] = 1
                s_d = s_d / mean_sd.unsqueeze(1).unsqueeze(2)
            else:
                s_d = s_d * mask

        if lossfunc == "kldiv":
            return F.kl_div(s_d, t_d, reduction="sum") / mask.sum().item()
        elif lossfunc == "l1loss":
            return F.l1_loss(s_d, t_d, reduction='sum') / mask.sum().item()
        elif lossfunc == "l2loss":
            return F.mse_loss(s_d, t_d, reduction='sum') / mask.sum().item()
        elif lossfunc == 'smoothl1':
            return F.smooth_l1_loss(s_d, t_d, reduction='sum') / mask.sum().item()

    def make_mask(self, attention_mask, layer):
        # attention mask -> b, len
        # mask -> b, len, 6, 6
        mask = attention_mask.unsqueeze(2).unsqueeze(3)
        return mask.repeat(1, 1, layer, layer).float()


class LTR_Angle(nn.Module):
    def __init__(self):
        super(LTR_Angle, self).__init__()

    def forward(self, t_embed, s_embed, attention_mask, lossfunc):
        bsz, layer_num, max_len, dim = t_embed.size()
        bsz, layer_num, max_len, sdim = s_embed.size()
        t_embed = t_embed.transpose(1, 2).reshape(-1, layer_num, dim)
        s_embed = s_embed.transpose(1, 2).reshape(-1, layer_num, sdim)
        mask = self.make_mask(attention_mask, layer_num)
        mask = mask.reshape(-1, layer_num, layer_num, layer_num)
        with torch.no_grad():
            # 1441
            t_sub = (t_embed.unsqueeze(1) - t_embed.unsqueeze(2))  # 1873
            t_sub = F.normalize(t_sub, p=2, dim=3).reshape(-1, layer_num, dim)  # 2305
            t_angle = torch.bmm(t_sub, t_sub.transpose(1, 2)).view(-1, layer_num, layer_num, layer_num)
            t_angle = t_angle * mask

        s_sub = (s_embed.unsqueeze(1) - s_embed.unsqueeze(2))  # 2737
        s_sub = F.normalize(s_sub, p=2, dim=3).reshape(-1, layer_num, sdim)  # 3169
        s_angle = torch.bmm(s_sub, s_sub.transpose(1, 2)).reshape(-1, layer_num, layer_num, layer_num)  # 3385
        s_angle = s_angle * mask
        if lossfunc == "l1loss":
            return F.l1_loss(s_angle, t_angle, reduction='sum') / mask.sum().item()
        elif lossfunc == "l2loss":
            return F.mse_loss(s_angle, t_angle, reduction='sum') / mask.sum().item()
        elif lossfunc == "smoothl1":
            return F.smooth_l1_loss(s_angle, t_angle, reduction='sum') / mask.sum().item()

    def make_mask(self, attention_mask, layers):
        mask = attention_mask.unsqueeze(2).unsqueeze(3).unsqueeze(4)
        return mask.repeat(1, 1, layers, layers, layers).float()

def contextual_loss(t_hidden, s_hidden, attention_mask):
    t_embed, s_embed = matching_alignment(t_hidden, s_hidden)

    # wrdist
    wrdist_function = WR_Dist()
    wrdist_loss = wrdist_function(t_embed, s_embed, attention_mask,
                                  distance='cos',
                                  lossfunc='kldiv',
                                  normalize=True)

    # wrang_windows
    wrang_function = WR_Angle_window()

    wrang_loss = wrang_function(t_embed, s_embed, attention_mask,
                                lossfunc='l2loss',
                                window=21)

    # ltrdist
    ltrdist_function = LTR_Dist()
    ltrdist_loss = ltrdist_function(t_embed, s_embed, attention_mask,
                                    distance='cos',
                                    lossfunc='kldiv',
                                    normalize=True)

    # ltrang
    ltrang_function = LTR_Angle()

    ltrang_loss = ltrang_function(t_embed, s_embed, attention_mask,lossfunc='l2loss')
    return wrdist_loss, wrang_loss, ltrdist_loss, ltrang_loss


