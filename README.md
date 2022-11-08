# fast-translate
一款适用于Linux系统的翻译软件，支持选中即翻译，方便文献阅读等。

github: [fast-translate](https://github.com/KaleW515/fast-translate)

gitee: [fast-trasnlate](https://gitee.com/kalew515/fast-translate)

如果觉得好用就点个:star:吧～

- [x] 支持复制自动翻译
- [x] 支持百度翻译，谷歌翻译
- [x] 支持划词即时翻译
- [x] 支持多语种翻译
- [x] 支持追加翻译
- ~~**谷歌翻译国内源无法使用的解决方案**：https://zhuanlan.zhihu.com/p/569452790~~
- sadly, 谷歌翻译国内源彻底失效，现在还是推荐百度翻译或者配置代理使用谷歌翻译

## ChangeLog

- 2022-11-08： 由于百度翻译或者未来可能会支持的翻译源按照字符收费，为了避免不必要的网络IO以及重复翻译一段话浪费免费字符数，现在添加了**缓存**功能，默认过期时间是一天，支持redis和本地缓存～

## Installtion

**注：本项目基于qt开发，在kde等基于qt的平台上体验较好**

### 手动编译安装

1. 下载源码到本地

   `git clone https://github.com/KaleW515/fast-translate.git`

2. 进入代码目录

   `cd fast-translate`

3. 确保安装了make，如果安装了这一步可以跳过，如果没有安装则需要进行安装

   `sudo pacman -S make`

4. 编译安装

   ```cmake
   make build
   make install
   ```

### Arch Linux & Manjaro

如果你是arch系用户，包含arch，manjaro等发行版，你可以选择使用yay进行安装

#### 使用yay安装

1. 项目已经打包到AUR，使用yay命令即可完成安装

   `yay -S fast-translate`

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

## 最后

如果你在使用中觉得缺失什么功能或者发现什么bug，欢迎提issue～
