## elastic 查询语法
[官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html)

### 正则
``` bash
GET online-nginx-*/_search
{ 
  "query": { 
    "prefix": { 
      "domain": "algo" 
    } 
  } 
}


{
  "query": {
    "terms": {
      "domain": [
        "algo.classba.cn",
        "algo.171xue.com",
        "algo-tx.classba.cn"
      ]
    }
  }
}
```