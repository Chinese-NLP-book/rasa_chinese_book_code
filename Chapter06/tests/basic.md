## 示例 #1
* query_knowledge_base: 有什么好听的[歌曲](object_type)？
    - slot{"object_type":"song"}
    - action_response_query
    - slot{"object_type":"song"}
    - slot{"mention":null}
    - slot{"attribute":null}
    - slot{"knowledge_base_last_object":null}
    - slot{"knowledge_base_last_object_type":"song"}
    - slot{"knowledge_base_listed_objects":[0,2,1]}
* query_knowledge_base: [第一首](mention)属于什么[专辑](attribute)？
    - slot{"attribute":"album"}
    - slot{"mention":"2"}
    - action_response_query
    - slot{"object_type":"song"}
    - slot{"attribute":null}
    - slot{"mention":null}
    - slot{"knowledge_base_last_object":2}
    - slot{"knowledge_base_last_object_type":"song"}

## 示例 #2
* query_knowledge_base: 列出一些[歌手](object_type)
    - slot{"object_type":"singer"}
    - action_response_query
    - slot{"object_type":"singer"}
    - slot{"mention":null}
    - slot{"attribute":null}
    - slot{"knowledge_base_last_object":null}
    - slot{"knowledge_base_last_object_type":"singer"}
    - slot{"knowledge_base_listed_objects":[3,2,0,1]}
* query_knowledge_base: [周杰伦](singer)的[生日](attribute)
    - slot{"attribute":"birthday"}
    - slot{"singer":"周杰伦"}
    - action_response_query
    - slot{"object_type":"singer"}
    - slot{"attribute":null}
    - slot{"mention":null}
    - slot{"knowledge_base_last_object":0}
    - slot{"knowledge_base_last_object_type":"singer"}

## 示例 #3
* query_knowledge_base: 给我列出[周杰伦](singer)的[歌曲](object_type)
    - slot{"object_type":"song"}
    - slot{"singer":"周杰伦"}
    - action_response_query
    - slot{"object_type":"song"}
    - slot{"mention":null}
    - slot{"attribute":null}
    - slot{"knowledge_base_last_object":0}
    - slot{"knowledge_base_last_object_type":"song"}
    - slot{"knowledge_base_listed_objects":[0]}
    - slot{"singer":null}

## 示例 #4
* query_knowledge_base: 列一些[男性](gender)[歌手](object_type)
    - slot{"gender":"male"}
    - slot{"object_type":"singer"}
    - action_response_query
    - slot{"object_type":"singer"}
    - slot{"mention":null}
    - slot{"attribute":null}
    - slot{"knowledge_base_last_object":null}
    - slot{"knowledge_base_last_object_type":"singer"}
    - slot{"knowledge_base_listed_objects":[0,1]}
    - slot{"gender":null}
