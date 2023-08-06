# coding=utf-8
"""
    此接口用于计算公司员工薪资
"""
company = "自学自用"


def yearSalary(monthSalary):
    """根据传入的月薪的值，计算出年薪：monthSalary*12"""
    return monthSalary


def daySalary():
    """根据传入的月薪，计算出一天的薪资，一个月按照22.5天计算（国家规定工作日）"""
    pass





# print(yearSalary(12))
if __name__=="__main__":
    print(yearSalary(2000))
"""实现就是将pass添加一些计算内容或者返回响应的值"""
