class NotDataStr(Exception):
    '''
    data异常
    '''
    def __str__(self):
        return "输入的数据应该是str类型"


class StartUrlNotNone(Exception):
    '''
    start_url异常
    '''

    def __str__(self):
        return "开始Url不可以为空"


class InsertUrlNotList(Exception):
    '''
    添加url错误
    '''

    def __str__(self):
        return "不是list"
