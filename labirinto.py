from hub import port, motion_sensor
import runloop, motor_pair, distance_sensor, color, color_sensor


CM_PER_ROT = 17.6#ROTACAO DA RODA
VELOCIDADE = 250
VELOCIDADEGYRO = 100
#VARIÁVEL GLOBAL PARA A FUNÇÃO DE CHECAGEM DO GIROSCÓPIO
TARGET_ANGLE_GYRO = 0

def achou_cor_vermelha():
    #FUNCAO RETORNA 1 SE VER VERMELHO
    return color_sensor.color(port.A) == color.RED

def encontrou_cor_verde():
    #RETONAR VERDADEIRO SE VER VERDE
    return color_sensor.color(port.A) == color.GREEN

def obstaculo_proximo():
    #FUNÇÃO RETORNA VERDADEIRO (TRUE) SE UM OBSTÁCULO FOR ENCONTRADO A 5CM
    distance = distance_sensor.distance(port.F)
    #DISTÂNCIA TEM QUE SER VÁLIDA E INFERIOR A 4.1CM (41MM)
    return distance > 0 and distance < 41

def obstaculo_muitoproximo():#PARA QUANDO NAO TIVER MUITO PERTO MAS AINDA TEM PAREDE
    #FUNÇÃO RETORNA VERDADEIRO (TRUE) SE UM OBSTÁCULO FOR ENCONTRADO A 10CM
    distance = distance_sensor.distance(port.F)
    #DISTÂNCIA TEM QUE SER VÁLIDA E INFERIOR A 15CM (150MM)
    return distance > 0 and distance < 150

def deg_for_cm(cm):
    #CM -> GRAUS DO MOTOR
    return int(cm / CM_PER_ROT * 360)

async def virar_precisamente(graus, direcao):
    steering_val = 0
    print("VIRANDO", graus, "PARA A", direcao)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)

    if direcao == 'direita':
        steering_val = 100
    elif direcao == 'esquerda':
        steering_val = -100

    motor_pair.move(motor_pair.PAIR_1, steering_val, velocity=VELOCIDADEGYRO)

    if graus < 180:
        # Para valores menor q 180 graus
        while abs(motion_sensor.tilt_angles()[0] * 0.1) < graus:
            await runloop.sleep_ms(10)
    else:
        # Para 180 graus, a lógica de checagem do sinal é INVERTIDA
        if direcao == 'direita':
            while motion_sensor.tilt_angles()[0] * 0.1 <= 0:
                await runloop.sleep_ms(10)
        elif direcao == 'esquerda': 
            while motion_sensor.tilt_angles()[0] * 0.1 >= 0:
                await runloop.sleep_ms(10)

    motor_pair.stop(motor_pair.PAIR_1)
    print("GYRO: CURVA CONCLUÍDA.")
    await runloop.sleep_ms(100)

async def main():
    #FASES DO LABIRINTO (0 = IDA, 1 = VOLTA, 2 = FIM)
    CORV= 0
    #CONTADOR PARA AS FITAS VERMELHAS
    CONTADOR_VERMELHO = 0
    #CONTADOR DE PAREDE
    PAREDE = 0

    #SETA O PAR DE MOTORES
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.C)

    print("INICIANDO)")
    #INICIA O MOVIMENTO
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=VELOCIDADE)

    #LOOP PRINCIPAL
    while True:
        if obstaculo_proximo():
            motor_pair.stop(motor_pair.PAIR_1)
            PAREDE += 1
            print("Obstáculo encontrado!! PAREDE NÚMERO:", PAREDE)

            if PAREDE == 4 or PAREDE == 27:
                print("PAREDE ESPECIAL ENCONTRADA! FAZENDO MANOBRA...")
                await virar_precisamente(90, 'direita')

            else:
                await virar_precisamente(90, 'esquerda')

                if obstaculo_muitoproximo():
                    PAREDE += 1
                    print("AINDA HA OBSTACULO. PAREDE NÚMERO:", PAREDE)
                    await virar_precisamente(180, 'direita')

                    if obstaculo_muitoproximo():
                        PAREDE += 1
                        print("AINDA PRESO! PAREDE NÚMERO:", PAREDE)
                        await virar_precisamente(90, 'esquerda')

            print("Continuando o percurso...")
            motor_pair.move(motor_pair.PAIR_1, 0, velocity=VELOCIDADE)

        #FASE 0: IDA
        elif CORV == 0:
            if encontrou_cor_verde():
                print("ACHOU A FITA PELA PRIMEIRA VEZ. VOLTANDO. COR ", CORV)
                CORV = 1
                motor_pair.stop(motor_pair.PAIR_1)

                #MANOBRA DA FITA VERDE
                await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(25), 0, velocity=VELOCIDADE)
                await virar_precisamente(90, 'direita')
                await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(22), 0, velocity=VELOCIDADE)
                await motor_pair.move_for_degrees(motor_pair.PAIR_1, -deg_for_cm(20), 0, velocity=VELOCIDADE)
                await virar_precisamente(180, 'direita')

                print("COR=1. Volta iniciada.")
                motor_pair.move(motor_pair.PAIR_1, 0, velocity=VELOCIDADE)

        #FASE 1: VOLTA
        elif CORV == 1:
            if achou_cor_vermelha():
                motor_pair.stop(motor_pair.PAIR_1)

                print("Saindo da fita vermelha...")
                await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(5), 0, velocity=VELOCIDADE)

                CONTADOR_VERMELHO += 1
                print("Encontrou FITA VERMELHA NÚMERO:", CONTADOR_VERMELHO)

                #MANOBRAS DA FITA VERMELHA
                if CONTADOR_VERMELHO == 1:
                    print("FAZENDO CURVA 1")
                    await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(18), 0, velocity=VELOCIDADE)
                    await runloop.sleep_ms(100)
                    await virar_precisamente(90, 'direita')
                    await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(21), 0, velocity=VELOCIDADE)
                    await runloop.sleep_ms(100)
                    await virar_precisamente(90, 'direita')
                    await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(20), 0, velocity=VELOCIDADE)
                    await runloop.sleep_ms(100)
                    await virar_precisamente(90, 'esquerda')

                elif CONTADOR_VERMELHO == 2:
                    print("FAZENDO CURVA 2 ")
                    await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(13), 0, velocity=VELOCIDADE)
                    await runloop.sleep_ms(100)
                    await virar_precisamente(90, 'direita')

                elif CONTADOR_VERMELHO == 3:
                    print("FAZENDO CURVA 3 ")
                    await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(15), 0, velocity=VELOCIDADE)
                    await runloop.sleep_ms(100)
                    await virar_precisamente(90, 'direita')

                elif CONTADOR_VERMELHO == 4:
                    print("FAZENDO CURVA 4")
                    await virar_precisamente(90, 'esquerda')

                print("CONCLUIU A CURVA")
                motor_pair.move(motor_pair.PAIR_1, 0, velocity=VELOCIDADE)

            elif encontrou_cor_verde():
                print("ACHOU A FITA PELA SEGUNDA VEZ FIM DO LABIRINTO, Cor:", CORV)
                CORV = 2
                motor_pair.stop(motor_pair.PAIR_1)
                await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_for_cm(60), 0, velocity=VELOCIDADE)

        #FASE 2: FIM
        elif CORV == 2:
            print("FIM DO PROGRAMA.")
            motor_pair.stop(motor_pair.PAIR_1)
            break
        await runloop.sleep_ms(20)

runloop.run(main())