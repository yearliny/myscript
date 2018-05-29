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
    selected = int(input("\t1、物理穿透\n\t2、法术穿透\n查询法术穿透还是物理穿透（回复序号）？"))
    replay_template = "当{defense}低于{critical_point}时，优先出{attack_1}，" \
                      "当{defense}高于{critical_point}时，优先出{attack_2}。"

    if selected == 1:
        penetrate = int(input("铭文物理穿透属性为多少(回复-2退出):"))
        if calculate(True, penetrate) != -1:
            answer = {
                'defense': '物理防御',
                'critical_point': calculate(penetrate),
                'attack_1': '暗影战斧',
                'attack_2': '破甲弓(碎星锤)'

            }
            print(replay_template.format(**answer))
        elif penetrate == -2:
            flag = False
        else:
            print("铭文物理穿透属性的范围为 0~100。")
    elif selected == 2:
        penetrate = int(input("铭文物理穿透属性为多少(回复-2退出):"))
        if calculate(False, penetrate) != -1:
            answer = {
                'defense': '法术防御',
                'critical_point': calculate(False, penetrate),
                'attack_1': '痛苦面具',
                'attack_2': '法穿杖'

            }
            print(replay_template.format(**answer))
        elif penetrate == -2:
            flag = False
        else:
            print("法术铭文穿透属性的范围为 0~88。")
    else:
        print("不正确的选项，程序退出。")


if __name__ == '__main__':
    main()
