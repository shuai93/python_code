# coding=utf8
"""
Migrate pyecharts and Flask with custom template functions.
"""
from __future__ import unicode_literals

import random
import datetime
import os

from flask import Flask, render_template
from flask.templating import Environment

from pyecharts import HeatMap, Map, Scatter3D, Bar
from pyecharts.engine import ECHAERTS_TEMPLATE_FUNCTIONS
from pyecharts.conf import PyEchartsConfig



app = Flask(__name__)


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


# ----- Adapter ---------
class FlaskEchartsEnvironment(Environment):
    def __init__(self, *args, **kwargs):
        super(FlaskEchartsEnvironment, self).__init__(*args, **kwargs)
        self.pyecharts_config = PyEchartsConfig(jshost='/static/js')
        self.globals.update(ECHAERTS_TEMPLATE_FUNCTIONS)


# ---User Code ----

class MyFlask(Flask):
    jinja_environment = FlaskEchartsEnvironment


app = MyFlask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/heatmap/")
def heatmap():
    hm = create_heatmap()
    return render_template('heatmap.html', hm=hm)


def create_heatmap():
    begin = datetime.date(2017, 1, 1)
    end = datetime.date(2017, 12, 31)
    data = [[str(begin + datetime.timedelta(days=i)),
             random.randint(1000, 25000)] for i in
            range((end - begin).days + 1)]
    heatmap = HeatMap("日历热力图示例", "某人 2017 年微信步数情况", width=1100)
    heatmap.add("", data, is_calendar_heatmap=True,
                visual_text_color='#000', visual_range_text=['', ''],
                visual_range=[1000, 25000], calendar_cell_size=['auto', 30],
                is_visualmap=True, calendar_date_range="2017",
                visual_orient="horizontal", visual_pos="center",
                visual_top="80%", is_piecewise=True)
    return heatmap


@app.route('/fujian/')
def fujian():
    value = [20, 190, 253, 77, 65]
    attr = ['福州市', '厦门市', '南平市', '泉州市', '三明市']
    map = Map("福建地图示例", width='100%', height=600)
    map.add("", attr, value, maptype='福建', is_visualmap=True,
            visual_text_color='#000')
    return render_template('fujian_map.html', m=map)


@app.route('/3d/')
def hello():
    s3d = scatter3d()
    return render_template(
        "3d.html",
        myechart=s3d.render_embed(),
        host=REMOTE_HOST,
        script_list=s3d.get_js_dependencies(),
    )


def scatter3d():
    data = [generate_3d_random_point() for _ in range(800)]
    # range_color = [
    #     "#313695",
    #     "#4575b4",
    #     "#74add1",
    #     "#abd9e9",
    #     "#e0f3f8",
    #     "#fee090",
    #     "#fdae61",
    #     "#f46d43",
    #     "#d73027",
    #     "#a50026",
    # ]
    scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True)
    # scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    return scatter3D


def generate_3d_random_point(): 
    return [
        random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
    ]

@app.route('/bar/')
def bar():

    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 36, 10, 75, 90]
    v2 = [10, 25, 8, 60, 20, 80]
    bar = Bar("柱状图数据堆叠示例")
    # bar.add("商家A", attr, v1, is_stack=True)
    # bar.add("商家B", attr, v2, is_stack=True)
    bar.add("商家A", attr, v1, mark_point=["average"])
    bar.add("商家B", attr, v2, mark_line=["min", "max"])
    return render_template(
        "bar.html",
        m=bar,
      
    )


@app.route('/bar1/')
def bar1():
    attr = ["{}天".format(i) for i in range(30)]
    v1 = [random.randint(1, 30) for _ in range(30)]
    bar = Bar("Bar - datazoom - slider 示例")
    bar.add("", attr, v1, is_label_show=True, is_datazoom_show=True)
    return render_template(
        "bar.html",
        m=bar,
      
    )

@app.route('/geo/')
def geo():
    from pyecharts import Geo

    data = [
    ("海门", 9),("鄂尔多斯", 12),("招远", 12),("舟山", 12),("齐齐哈尔", 14),("盐城", 15),
    ("赤峰", 16),("青岛", 18),("乳山", 18),("金昌", 19),("泉州", 21),("莱西", 21),
    ("日照", 21),("胶南", 22),("南通", 23),("拉萨", 24),("云浮", 24),("梅州", 25),
    ("文登", 25),("上海", 25),("攀枝花", 25),("威海", 25),("承德", 25),("厦门", 26),
    ("汕尾", 26),("潮州", 26),("丹东", 27),("太仓", 27),("曲靖", 27),("烟台", 28),
    ("福州", 29),("瓦房店", 30),("即墨", 30),("抚顺", 31),("玉溪", 31),("张家口", 31),
    ("阳泉", 31),("莱州", 32),("湖州", 32),("汕头", 32),("昆山", 33),("宁波", 33),
    ("湛江", 33),("揭阳", 34),("荣成", 34),("连云港", 35),("葫芦岛", 35),("常熟", 36),
    ("东莞", 36),("河源", 36),("淮安", 36),("泰州", 36),("南宁", 37),("营口", 37),
    ("惠州", 37),("江阴", 37),("蓬莱", 37),("韶关", 38),("嘉峪关", 38),("广州", 38),
    ("延安", 38),("太原", 39),("清远", 39),("中山", 39),("昆明", 39),("寿光", 40),
    ("盘锦", 40),("长治", 41),("深圳", 41),("珠海", 42),("宿迁", 43),("咸阳", 43),
    ("铜川", 44),("平度", 44),("佛山", 44),("海口", 44),("江门", 45),("章丘", 45),
    ("肇庆", 46),("大连", 47),("临汾", 47),("吴江", 47),("石嘴山", 49),("沈阳", 50),
    ("苏州", 50),("茂名", 50),("嘉兴", 51),("长春", 51),("胶州", 52),("银川", 52),
    ("张家港", 52),("三门峡", 53),("锦州", 54),("南昌", 54),("柳州", 54),("三亚", 54),
    ("自贡", 56),("吉林", 56),("阳江", 57),("泸州", 57),("西宁", 57),("宜宾", 58),
    ("呼和浩特", 58),("成都", 58),("大同", 58),("镇江", 59),("桂林", 59),("张家界", 59),
    ("宜兴", 59),("北海", 60),("西安", 61),("金坛", 62),("东营", 62),("牡丹江", 63),
    ("遵义", 63),("绍兴", 63),("扬州", 64),("常州", 64),("潍坊", 65),("重庆", 66),
        ("台州", 67),("南京", 67),("滨州", 70),("贵阳", 71),("无锡", 71),("本溪", 71),
        ("克拉玛依", 72),("渭南", 72),("马鞍山", 72),("宝鸡", 72),("焦作", 75),("句容", 75),
        ("北京", 79),("徐州", 79),("衡水", 80),("包头", 80),("绵阳", 80),("乌鲁木齐", 84),
        ("枣庄", 84),("杭州", 84),("淄博", 85),("鞍山", 86),("溧阳", 86),("库尔勒", 86),
        ("安阳", 90),("开封", 90),("济南", 92),("德阳", 93),("温州", 95),("九江", 96),
        ("邯郸", 98),("临安", 99),("兰州", 99),("沧州", 100),("临沂", 103),("南充", 104),
        ("天津", 105),("富阳", 106),("泰安", 112),("诸暨", 112),("郑州", 113),("哈尔滨", 114),
        ("聊城", 116),("芜湖", 117),("唐山", 119),("平顶山", 119),("邢台", 119),("德州", 120),
        ("济宁", 120),("荆州", 127),("宜昌", 130),("义乌", 132),("丽水", 133),("洛阳", 134),
        ("秦皇岛", 136),("株洲", 143),("石家庄", 147),("莱芜", 148),("常德", 152),("保定", 153),
        ("湘潭", 154),("金华", 157),("岳阳", 169),("长沙", 175),("衢州", 177),("廊坊", 193),
        ("菏泽", 194),("合肥", 229),("武汉", 273),("大庆", 279)]

    geo = Geo(
        "全国主要城市空气质量",
        "data from pm2.5",
        title_color="#fff",
        title_pos="center",
        width=1200,
        height=600,
        background_color="#404a59",
    )
    attr, value = geo.cast(data)
    geo.add(
        "",
        attr,
        value,
        visual_range=[0, 200],
        visual_text_color="#fff",
        symbol_size=15,
        is_visualmap=True,
    )
    return render_template(
        "map.html",
        myechart=geo.render_embed(),
        host=REMOTE_HOST,
        script_list=geo.get_js_dependencies(),
      
    )


@app.route('/graph/')
def graph():
    
    from pyecharts import Graph

    import json
    # 这里需要关系的数据
    with open(os.path.join("fixtures", "weibo.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories, cont, mid, userl = j

    graph = Graph("微博转发关系图", width=1200, height=600)
    graph.add(
        "",
        nodes,
        links,
        categories,
        label_pos="right",
        graph_repulsion=50,
        is_legend_show=False,
        line_curve=0.2,
        label_text_color=None,
    )
    return render_template(
        "graph.html",
        myechart=graph.render_embed(),
        host=REMOTE_HOST,
        script_list=graph.get_js_dependencies(),
      
    )

@app.route('/line3d/')
def line3d():
    from pyecharts import Line3D

    import math
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    line3d = Line3D("3D 折线图示例", width=1200, height=600)
    line3d.add(
        "",
        _data,
        is_visualmap=True,
        visual_range_color=range_color,
        visual_range=[0, 30],
        is_grid3d_rotate=True,
        grid3d_rotate_speed=180,
    )

    return render_template(
        "graph.html",
        name='3D 折线图',
        myechart=line3d.render_embed(),
        host=REMOTE_HOST,
        script_list=line3d.get_js_dependencies(),
      
    )



if __name__ == "__main__":

    app.run(debug=True)
