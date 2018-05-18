def calculate(isphysics, penetrate):
    if isphysics:
        if penetrate > 100 or penetrate < 0:
            return -1
        zero_point = (penetrate + 200 + penetrate*0.45) / 0.45
    else:
        if penetrate > 88 or penetrate < 0:
            return -1
        zero_point = (penetrate + 75 + penetrate*0.45) / 0.45
    return round(zero_point, 0)


def main():
    type = int(input("\t1、物理穿透\n\t2、法术穿透\n查询法术穿透还是物理穿透（回复序号）？"))
    flag = True
    while flag:
        penetrate = int(input("铭文穿透属性为多少(回复-2退出):"))
        if type == 1:
            if calculate(True, penetrate) != -1:
                print("当护甲高于{0}时，优先出破甲弓，当护甲低于{0}时，优先出暗影战斧。".format(False, calculate(penetrate)))
            elif penetrate == -2:
                flag = False
            else:
                print("铭文穿透属性的范围只能在 0~100 之间。")
        elif type == 2:
            if calculate(False, penetrate) != -1:
                print("当护甲高于{0}时，优先出法穿杖，当护甲低于{0}时，优先出痛苦面具。".format(calculate(False, penetrate)))
            elif penetrate == -2:
                flag = False
            else:
                print("铭文穿透属性的范围只能在 0~88 之间。")



if __name__ == '__main__':
    main()
