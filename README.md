# fast-translate
一款适用于Linux系统的翻译软件，支持选中即翻译，方便文献阅读等。

如果觉得好用就点个:star:吧～

- [x] 支持复制自动翻译
- [x] 支持百度翻译，谷歌翻译
- [x] 支持划词即时翻译
- [x] 支持多语种翻译
- [x] 支持追加翻译

- 使用pyqt5开发，借鉴[兰译](https://github.com/yuhldr/ldr-translate)的部分代码进行开发，在原作基础上完善了即时翻译，多翻译源同时翻译等功能。

## Usage

使用前需要完善相关翻译api的一些必要参数，如下图，打开设置进行相关参数的填写，填写后别忘了保存

![2022-06-17_00-08.png](https://s2.loli.net/2022/06/17/dvGH9AshZfQSYec.png)

### 百度翻译

[点击此处查看配置教程](https://github.com/KaleW515/fast-translate/blob/main/docs/百度翻译.md)

### 谷歌翻译

[点击此处查看配置教程](https://github.com/KaleW515/fast-translate/blob/main/docs/谷歌翻译.md)

### 使用介绍

|    特性    |                             操作                             |                             演示                             |
| :--------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| google翻译 | 选中百度翻译和谷歌翻译，会出现百度翻译和谷歌翻译的结果框，复制即可进行翻译，需要先在设置中填写相关的参数 | ![google翻译.gif](https://s2.loli.net/2022/06/16/YqABIFdsknuw6KP.gif) |
| 多语种翻译 |                      更改翻译的目标结果                      | ![多语种翻译.gif](https://s2.loli.net/2022/06/16/jOT6wLlY8BPZtdu.gif) |
|  即时翻译  |   选中即时翻译，选中一段后即可自动进行翻译，省去复制的操作   | ![即时翻译.gif](https://s2.loli.net/2022/06/16/xqBjub7hJGMTXWd.gif) |
|  追加翻译  |                         选中追加翻译                         | ![追加翻译.gif](https://s2.loli.net/2022/06/16/4xR9MBTstH2FidS.gif) |
| 自定义翻译 |             点击翻译按钮，可以翻译原文框中的原文             | ![自定义翻译.gif](https://s2.loli.net/2022/06/16/RtWxJw1faU4mnFV.gif) |



## Installtion

### 手动编译安装

1. 下载源码到本地

   `git clone https://github.com/KaleW515/fast-translate.git`

2. 进入代码目录

   `cd fast-translate`

3. 确保安装了cmake，如果安装了这一步可以跳过，如果没有安装则需要进行安装

   `sudo pacman -S --noconfirm cmake`

4. 编译安装

   ```cmake
   make check-dependency
   make build
   make install
   ```

### 使用yay安装
