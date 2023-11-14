from machine import Pin, PWM
from time import sleep
import utime
IN1 = Pin(1, Pin.OUT)
IN2 = Pin(2, Pin.OUT)
IN3 = Pin(3, Pin.OUT)
IN4 = Pin(4, Pin.OUT)
ena = PWM(Pin(0))
enb = PWM(Pin(5))
ena.freq(1000)
enb.freq(1000)
speed=65535
trigger = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN)
sensor1 = Pin(12,Pin.IN)
sensor2 = Pin(15,Pin.IN)
def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print("The distance from object is ",distance,"cm")
    return distance
def clk(en,in1,in2,duty):
    en.duty_u16(duty)
    in1.low() #spin forward
    in2.high()
def aclk(en,in1,in2,duty):
    en.duty_u16(duty)
    in1.high() #spin backward
    in2.low()
def brk(en,in1,in2,duty):
    en.duty_u16(duty)
    in1.low() #brake
    in2.low()
def fwd():
    clk(ena,IN1,IN2,speed)
    clk(enb,IN3,IN4,speed)
while True:
    d=ultra()
    #utime.sleep(0.5)
    #print(sensor1.value(),sensor2.value())
    if(sensor1.value() and sensor2.value()):
        if(d<=30):
            #print("fwd")
            speed=0
        elif(d>30 and d<=50):
            speed=45000
        elif(d>50 and d<=60):
            speed=50000
        elif(d>60 and d<=70):
            speed=53000
        elif(d>70 and d<=80):
            speed=55000
        elif(d>80 and d<=100):
            speed=57000
        elif(d>100 and d<=250):
            speed=60000
        else:
            speed=0
        fwd()
    elif(sensor1.value() and not(sensor2.value())):
        clk(ena,IN1,IN2,65535)
        aclk(enb,IN3,IN4,65535)
        sleep(0.8)
    elif(sensor2.value() and not(sensor1.value())):
        aclk(ena,IN1,IN2,65535)
        clk(enb,IN3,IN4,65535)
        sleep(0.8)
    else:
        brk(ena,IN1,IN2,0)
        brk(enb,IN3,IN4,0)
