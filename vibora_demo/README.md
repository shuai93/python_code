# vibora_demo
一个性感和快速的异步Python 3.6 + Python Web框架  
[vibora github](https://github.com/vibora-io/vibora)

## 为什么性能那么高
- uvloop 一个c实现的事件循环框架,基于libuv.uvloop
- cython实现的http_parser, 再加上一些cython构建的web组件，比如 模板，user-route等

总结来说：谁替换的C代码多，谁性能就高