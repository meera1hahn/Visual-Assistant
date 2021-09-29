# Visual-Assistant
Learning a visually grounded memory assistant

This is an implementation of the paper: Learning a Visually Grounded Memory Assistant

This repository contains the data, the data analysis and the results for TaskA presented in the paper

For information on how the dataset was collected or to get access to the AMT set up please contact the authors. 

## The Visually Grounded Memory Assistant Dataset

Contains human participants participating in the task Memory Question Answering with Navigation (MemQA). Please refer the [video](https://www.youtube.com/watch?v=T97r2leqFyQ)

The task was encapsulated in the 3D simulated indoor environments from the Matterport3D dataset and was run on Amazon Mechanical Turk.

## Tasks

We present 2 tasks on top of the dataset which are useful to realization of an AR assistant -- to predict when humans request assistance on visual-memory tasks. We present results for task A. 

### Task A
Take in the fly-through and a single question. Predict: correctness, navigation behavior, assistance request behavior.

### Task B
Take in the fly-through, all four questions and the sequence of frames during the answering phase. At each time step of the answering phase predict behavior: navigation, request for assistance, answer selection or nothing

## Contributing

If you find something wrong or have a question, feel free to open an issue. If you would like to contribute, please install pre-commit before making commits in a pull request:

```bash
python -m pip install pre-commit
pre-commit install
```

## Citing

If you use The Visually Grounded Memory Assistant Dataset in your research, please cite the following [paper](https://arxiv.org/):

```
@inproceedings{hahn2020visualassistant,
  title={Learning a Visually Grounded Memory Assistan},
  author={Hahn, Meera and Carlberg, Kevin and Desai, Ruta and Batra, Dhruv and Hillis, James},
  booktitle={Arxiv},
  year={2020}
}
