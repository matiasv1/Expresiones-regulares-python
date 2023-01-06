import re
import time
from sys import argv

#Esta funcion captura el stilo y color de la seccion [v4+ stryles] y retorna una lista
def style_color(text,lista):
    contador=0
    re_styles=re.findall(r'Style: ?(.*?),',text)
    re_color=re.findall(r'\w*,\w*,\d*(\&\w*)',text)
    while contador<len(re_styles):
        lista.append((re_styles[contador],re_color[contador]))
        contador+=1
    return lista
#Esta funcion utiliza la lista de stilo y color ,se comparan con los datos de la seccion[events].Finalmente retorna una lista con toda la informacion util
def dialogue_style_color(text,lista,lista_final):
    color_ordenado=""
    time_style=re.findall(r'((?:\d+\:){1,2}\d+.\d+),((?:\d+\:){1,2}\d+.\d+),(.*?),',text)
    dialogo=re.findall(r',,[\d,]*(.*)\n?',text)
    contador=0
    while contador< len(dialogo):
        for style,color in lista:
            if style==time_style[contador][2]:
                color_ordenado=""
                color=re.findall(r'&(\w{3})(\w{2})(\w{2})(\w{2})',color)
                color_ordenado=color[0][3]+color[0][2]+color[0][1]
                lista_final.append((time_style[contador][0],time_style[contador][1],color_ordenado,dialogo[contador]))
        contador+=1
 
    return lista_final  

#Esta funcion convierte en segundos el tiempo de inicio y final ingresado en los parametros(dependiendo si se ingresa con hora o sin).
def sum_time(sumainicial,sumafinal,flag,tiempo):
    if flag:
        return None
    else:
        re_tiempos=re.findall(r'(?:((?:\d+\:){1,2}\d+.\d{2,3})((?:\d+\:){1,2}\d+.\d{2,3}))',tiempo)
        
        inicio=re.findall(r'(\d+)',re_tiempos[0][0])
        
        fin=re.findall(r'(\d+)',re_tiempos[0][1])
        if (len(inicio)==3 and len(fin)==3):
            sumainicial=int(inicio[0])*60+int(inicio[1])+int(inicio[2])*(10**-3)
            sumafinal=int(fin[0])*60+int(fin[1])+int(fin[2])*(10**-3)
            return (sumainicial,sumafinal)
        elif(len(inicio)==3 and len(fin)==4):
            sumainicial=int(inicio[0])*60+int(inicio[1])+int(inicio[2])*(10**-3)
            sumafinal=int(fin[0])*3600+int(fin[1])*60+int(fin[2])+int(fin[3])*(10**-3)
            return(sumainicial,sumafinal)

        elif (len(inicio)==4 and len(fin)==3):
            sumainicial=int(inicio[0])*3600+int(inicio[1])*60+int(inicio[2])+int(inicio[3])*(10**-3)
            sumafinal=int(fin[0])*60+int(fin[1])+int(fin[2])*(10**-3)
            return(sumainicial,sumafinal)

        elif (len(fin)==4 and len(inicio)==4):
            sumainicial=int(inicio[0])*3600+int(inicio[1])*60+int(inicio[2])+int(inicio[3])*(10**-3)
            sumafinal=int(fin[0])*3600+int(fin[1])*60+int(fin[2])+int(fin[3])*(10**-3)
            return (sumainicial,sumafinal)

#imprime los datos por pantalla dependiendo de las diversas posibilidades,con hora ,sin hora ,etc.
def print_values(variable,flag):
    if flag==True:
        print("Traduciendo "+variable[1]+" a "+variable[2]+".srt")
        print("Proceso Finalizado.")
    else:
        re_tiempos=re.findall(r'(?:((?:\d+\:){1,2}\d+.\d{2,3})((?:\d+\:){1,2}\d+.\d{2,3}))',variable[3])
        inicio=re.findall(r'(\d+)',re_tiempos[0][0])
        final=re.findall(r'(\d+)',re_tiempos[0][1])
        if (len(inicio)==3 and len(final)==3):
            print("Traduciendo "+variable[1]+" a "+variable[2]+".srt")
            print("Desde "+str(inicio[0])+"[min], "+str(inicio[1])+"[s], "+str(inicio[2])+"[ms]")
            print("Hasta "+str(final[0])+"[min], "+str(final[1])+"[s], "+str(final[2])+"[ms]")
            print("Proceso Finalizado.")
        elif ((len(inicio)==4)and(len(final)==4)):
            print("Traduciendo "+variable[1]+" a "+variable[2]+".srt")
            print("Desde "+str(inicio[0])+"[h], "+str(inicio[1])+"[min], "+str(inicio[2])+"[s], "+str(inicio[3])+"[ms]")
            print("Hasta "+str(final[0])+"[h], "+str(final[1])+"[min], "+str(final[2])+"[s], "+str(final[3])+"[ms]")
            print("Proceso Finalizado.")
        else:
            print("Traduciendo "+variable[1]+" a "+variable[2]+".srt")
            print("Desde "+str(inicio[0])+"[min], "+str(inicio[1])+"[s], "+str(inicio[2])+"[ms]")
            print("Hasta "+str(final[0])+"[h], "+str(final[1])+"[min], "+str(final[2])+"[s], "+str(final[3])+"[ms]")
            print("Proceso Finalizado.")


#funcion que retorna si algun tiempo de inicio del ass coincide con el parametro o hay desfase.
#Tambien capturo el primer dato que sobrepasa el tiempo ingresado,para hacer el desfase de tiempo.
def different_cases(inicio,lista_style_color):
    for tiempo_ini,tiempo_fin,color,dialogo in lista_style_color:
        cambio=tiempo_ini+"0"
        re_time=re.findall(r'(\d+)',cambio)
        sumainicial=int(re_time[0])*3600+int(re_time[1])*60+int(re_time[2])+int(re_time[3])*(10**-3)
        if sumainicial==inicio:
            sumainicial=0
            return sumainicial
        elif sumainicial>inicio:
            
            return sumainicial
            
#Funcion que escribe en el archivo dependiendo de los diferentes casos y tambien se convierten los tiempos en segundos haciendo toda la operatoria correspondiente.
#Tambien se agregan los 0 cuando son milisegundos como 6 le agrega dos 0 o 65 le agrega un cero.

def write(inicio,fin,lista_style_color,primervalor,flag1,argv):
    contador=0
    archivo2=open(argv+'.srt','a',encoding='utf8')
    for tiempo_ini,tiempo_fin,color,dialogo in lista_style_color:
        cambio1=tiempo_ini+"0"
        cambio2=tiempo_fin+"0"
        re_time_inicial=re.findall(r'(\d+)',cambio1)
        re_time_final=re.findall(r'(\d+)',cambio2)
        sumafinal=int(re_time_final[0])*3600+int(re_time_final[1])*60+int(re_time_final[2])+int(re_time_final[3])*(10**-3)
        sumainicial=int(re_time_inicial[0])*3600+int(re_time_inicial[1])*60+int(re_time_inicial[2])+int(re_time_inicial[3])*(10**-3)
        if flag1:
            contador+=1
            archivo2.write(str(contador)+"\n")
            archivo2.write("0"+tiempo_ini+"0"+" --> "+"0"+tiempo_fin+"0"+"\n")
            archivo2.write('<font color="#'+color+'">'+dialogo+"</font>"+'\n')
            archivo2.write("\n")

        elif primervalor==0:
            if sumainicial>=inicio and sumafinal<=fin:
                contador+=1
                archivo2.write(str(contador)+"\n")
                archivo2.write("0"+tiempo_ini+"0"+" --> "+"0"+tiempo_fin+"0"+"\n")
                archivo2.write('<font color="#'+color+'">'+dialogo+"</font>"+'\n')
                archivo2.write("\n")
            
        else:
            if primervalor==sumainicial:
                contador+=1
                corrimiento_inicio=primervalor-inicio
                diferencia=sumafinal-sumainicial
                intervalo_final=corrimiento_inicio+diferencia
                guardar_intervalo=sumafinal

                convert_ini=time.strftime("%H:%M:%S",time.gmtime(corrimiento_inicio))
                convert_fin=time.strftime("%H:%M:%S",time.gmtime(intervalo_final))
                mili_ini=str(round((corrimiento_inicio-int(corrimiento_inicio))*1000))
                mili_fin=str(round((intervalo_final-int(intervalo_final))*1000))
                if len(mili_ini)==1:
                    mili_ini=mili_ini+"0"+"0"
                if len(mili_ini)==2:
                    mili_ini=mili_ini+"0"
                if len(mili_fin)==1:
                    mili_fin=mili_fin+"0"+"0"
                if len(mili_fin)==2:
                    mili_fin=mili_fin+"0"
                    
                archivo2.write(str(contador)+"\n")
                archivo2.write(convert_ini+"."+str(mili_ini)+" --> "+convert_fin+"."+str(mili_fin)+"\n")
                archivo2.write('<font color="#'+color+'">'+dialogo+"</font>"+'\n')
                archivo2.write("\n")

            elif sumainicial>inicio and sumafinal<=fin:
                contador+=1
                diferencia=sumafinal-sumainicial
                corrimiento_inicio=sumainicial-guardar_intervalo
                nuevo_inicio=intervalo_final+corrimiento_inicio
                intervalo_final=nuevo_inicio+diferencia
                guardar_intervalo=sumafinal

                convert_ini=time.strftime("%H:%M:%S",time.gmtime(nuevo_inicio))
                convert_fin=time.strftime("%H:%M:%S",time.gmtime(intervalo_final))
                mili_ini=str(round((nuevo_inicio-int(nuevo_inicio))*1000))
                mili_fin=str(round((intervalo_final-int(intervalo_final))*1000))  
                if len(mili_ini)==1:
                    mili_ini=mili_ini+"0"+"0"
                if len(mili_ini)==2:
                    mili_ini=mili_ini+"0"
                if len(mili_fin)==1:
                    mili_fin=mili_fin+"0"+"0"
                if len(mili_fin)==2:
                    mili_fin=mili_fin+"0"
                    
                archivo2.write(str(contador)+"\n")
                archivo2.write(convert_ini+"."+str(mili_ini)+" --> "+(convert_fin)+"."+str(mili_fin)+"\n")
                archivo2.write('<font color="#'+color+'">'+dialogo+"</font>"+'\n')
                archivo2.write("\n")
    archivo2.close()   
flag=False
sumainicial=0
sumafinal=0
primervalor=0
#abre el archivo y se crea una flag en caso que no se ingresa tiempo.
if len(argv)==3:
    flag=True
    archivo=open(argv[1],'r',encoding='utf8')
else:
    archivo=open(argv[1],'r',encoding='utf8')
text=archivo.read()

lista_style_color=[]
lista_final=[]
lista_style_color=style_color(text,lista_style_color)
alldatos=dialogue_style_color(text,lista_style_color,lista_final)
#En caso que se cumpla la flag no se ingreso tiempo entonces quedan como 0 y en el otro caso se llaman las funciones.
if flag:
    inicio=0
    fin=0
else:
    
    inicio,fin=sum_time(sumainicial,sumafinal,flag,argv[3])
    primervalor=different_cases(inicio,alldatos)
print_values(argv,flag)
write(inicio,fin,alldatos,primervalor,flag,argv[2])
archivo.close()
