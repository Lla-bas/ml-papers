---
title: "Attention Is All You Need"
authors: "Vaswani et al."
year: 2017
venue: "NeurIPS"
url: "https://arxiv.org/pdf/1706.03762.pdf"
date_read: 2026-11-27
---

# Attention Is All You Need

The Transformer was the first sequence transduction model based entirely on attention, enabling parallelized training across the sequence and kick-starting the modern LLM era.

## Takeaways

It replaces recurrent and convolutional layers with multi-head self-attention built on Scaled Dot-Product Attention. Scaling by `1/sqrt(d_k)` keeps softmax gradients from vanishing at large dimensions, while multiple heads let the model attend to different representation subspaces at once.

Positional encodings (the same shape as the token embeddings, added element-wise) inject sequence order since attention itself has no notion of position.

## Citation
```bibtex
@article{vaswani2017attention,
  title   = {Attention Is All You Need},
  author  = {Ashish Vaswani and Noam Shazeer and Niki Parmar and Jakob Uszkoreit and Llion Jones and Aidan N. Gomez and Lukasz Kaiser and Illia Polosukhin},
  year    = {2017},
  journal = {NeurIPS},
  url     = {https://arxiv.org/pdf/1706.03762.pdf}
}
```
