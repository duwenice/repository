# 格式
> type: description

##  type 类型
type 是 commit 的类别，只允许如下几种标识：
* fix: 修复bug
* add: 新功能
* update: 更新
* style : 代码格式改变
* test: 增加测试代码
* revert: 撤销上一次的commit
* build: 构建工具或构建过程等的变动，如：gulp 换成了 webpack，webpack 升级等


## description
description 是对本次提交的简短描述，
不超过50个字符。

推荐以动词开头，如： 设置、修改、增加、删减、撤销等