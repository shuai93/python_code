from flask import Flask
from flask_restaction import Api

app = Flask(__name__)
# 创建一个 Api 对象，把 app 作为参数
api = Api(app)


# 创建 Welcome 类，描述欢迎信息(框架可以序列化任意类型的对象)
class Welcome:
    def __init__(self, name):
        self.name = name
        self.message = "Hello %s, Welcome to flask-restaction!" % name


# 创建一个 Hello 类，定义 get 方法
class Hello:
    """Hello world"""

    # 在 get 方法文档字符串中描述输入参数和输出的格式
    def get(self, name):
        """
        Get welcome message

        $input:
            name?str&default="world": Your name
        $output:
            message?str: Welcome message
        """
        return Welcome(name)

    def post(self, age):

        return Welcome({"age": age})


# 添加资源
api.add_resource(Hello)
# 配置API文档的访问路径
app.route('/')(api.meta_view)
url_for("hello")

if __name__ == '__main__':
    app.run(debug=True)