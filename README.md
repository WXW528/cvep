# cvep
Computer Vision Experiment Platform

本项目以京东AI的fast-reid（https://github.com/JDAI-CV/fast-reid）为基础进行开发，重点扩展在智慧交通领域的应用。
首先安装所需软件：
```base
pip install yacs
pip install pyyaml
sudo apt-get cython
pip install termcolor
pip install tabulate
pip install tensorboard
```
下载内置缺省数据集：
到[百度网盘](https://pan.baidu.com/s/1ntIi2Op)下面下载Market1501数据集的Market-1501-v15.09.15.zip文件，将其解压到./datasets/目录下，目录结构如下所示：
datasets/
    Market-1501-v15.09.15/
        bounding_box_test/
        bounding_box_train/
运行缺省训练程序：
```bash
python ./tools/train_net.py --config-file ./configs/Market1501/bagtricks_R50.yml MODEL.DEVICE "cuda:3"
```
这里指定使用第四块GPU进行训练。

