---
title: "ImageNet Classification with Deep Convolutional Neural Networks"
authors: "Krizhevsky, Sutskever, Hinton"
year: 2012
venue: "NeurIPS"
url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"
date_read: 2026-11-25
---

# ImageNet Classification with Deep Convolutional Neural Networks

AlexNet showed that a large deep CNN trained on GPUs could beat classical vision pipelines on ImageNet (15.3% vs 26.2% top-5 error), starting the modern deep learning era.

## Takeaways

Combining the GPU compute power with architectural choices like ReLU, dropout and normalization allowed the training of a 60M parameter network without overfitting.

ReLU, compared to tahn/sigmoid is much less saturating, speeding up convergence.

Regularization techniques like Dropout on the FC layers and data augmentation helped with generalization.

The main limiatation remained depth. Adding too many layers hurt accuracy, which was later solved by Residual Connections.

Most of the core recipe became standard practice, while Local Response Normalization and big fully connected heads were replaced by BatchNorm and global average pooling.

## Citation
```bibtex
@inproceedings{krizhevsky2012imagenet,
  title     = {ImageNet Classification with Deep Convolutional Neural Networks},
  author    = {Krizhevsky, Alex and Sutskever, Ilya and Hinton, Geoffrey E.},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2012},
  url       = {https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf}
}
```
