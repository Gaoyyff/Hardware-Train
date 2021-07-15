# 一、上传训练样本

训练图片传入：`VOCdevkit/VOC2007/JPEGImages`

训练图片对应标签(`.xml`格式)传入：`VOCdevkit/VOC2007/Annotations`

**代码自动将训练图片分为 训练集 和 交叉验证集**

# 二、训练

1. 运行`VOCdevkit/VOC2007`文件夹下，`voc2yolo3.py`文件
2. 修改根目录下 `voc_annotation.py`文件中，13行`classes`
3. 运行根目录下 `voc_annotation.py`文件
4. 修改`train.py`中143行`num_classes`
5. 运行根目录下`train.py`文件
6. 训练完成后，训练权重保存在 `log`文件夹下
   将最终loss，将文件路径复制到 `yolo.py`中 `"model_path": 'logs/Epoch50-Total_Loss11.6703-Val_Loss7.3870.pth'`，把后面文件名改了

（注意：下一次训练的时候，之前训练的权重不会自动删除，注意把之前权重手动删掉）

（初始权重为：`train.py`中，`model_path      = "model_data/yolo_weights.pth"`）

（训练过程：共150轮。先进行50轮迁移学习，再100轮训练）

> 训练可能会出现`GPU`内存不足情况
>
> 解决方式：减小`train.py`中`Batch_size`
>
> 如果不好使（我遇到的情况是前面50轮迁移学习没问题，但是后面100轮训练就不行了），再减小`train.py`中`num_workers`

# 三、预测

1. 上传预测样本：把图片上传到 `img` 文件夹下
2. 单张图片预测：
   将根目录下 `predict.py`文件，代码改为 `mode = 'predict'`
   运行即可
3. 批量图片预测：
   将根目录下 `predict.py`文件，代码改为 `mode = 'predictAllAndSave'`
   * 先运行根目录下 `saveResult.py`，生成待预测图片名称 txt 文件，保存在 `result`文件夹中
   * 运行`predict.py`文件。
   * 预测结果保存在 `result`文件夹下。





