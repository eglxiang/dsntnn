import torch
from torch.testing import assert_allclose

from dsntnn import average_loss, euclidean_losses


def test_euclidean_forward_and_backward():
    input_tensor = torch.Tensor([
        [[3, 4], [3, 4]],
        [[3, 4], [3, 4]],
    ])

    target = torch.Tensor([
        [[0, 0], [0, 0]],
        [[0, 0], [0, 0]],
    ])

    in_var = input_tensor.detach().requires_grad_(True)

    expected_loss = 5.0
    actual_loss = average_loss(euclidean_losses(in_var, target))
    expected_grad = torch.Tensor([
        [[0.15, 0.20], [0.15, 0.20]],
        [[0.15, 0.20], [0.15, 0.20]],
    ])
    actual_loss.backward()

    assert expected_loss == actual_loss.item()
    assert_allclose(expected_grad, in_var.grad)


def test_euclidean_mask():
    output = torch.Tensor([
        [[0, 0], [1, 1], [0, 0]],
        [[1, 1], [0, 0], [0, 0]],
    ])

    target = torch.Tensor([
        [[0, 0], [0, 0], [0, 0]],
        [[0, 0], [0, 0], [0, 0]],
    ])

    mask = torch.Tensor([
        [1, 0, 1],
        [0, 1, 1],
    ])

    expected = 0.0
    actual = average_loss(euclidean_losses(output, target), mask)
    assert expected == actual.item()
