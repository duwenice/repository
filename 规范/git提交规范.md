# 格式
> type: description

##  type 类型
type 是 commit 的类别，只允许如下几种标识：
* feat：提交新功能
* fix：修复了bug
* docs：只修改了文档
* style：调整代码格式，未修改代码逻辑（比如修改空格、格式化、缺少分号等）
* refactor：代码重构，既没修复bug也没有添加新功能
* perf：性能优化，提高性能的代码更改
* test：添加或修改代码测试
* chore：对构建流程或辅助工具和依赖库（如文档生成等）的更改


## description
description 是对本次提交的简短描述，
不超过50个字符。

推荐以动词开头，如： 设置、修改、增加、删减、撤销等