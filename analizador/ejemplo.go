package main
import ("fmt")

var Heap [100000]float64
var Stack [100000]float64

var SP, HP float64                                         // declaración de Stack y heap pointer
var T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10 float64


func main (){
    /*a:integer*/
    T0=0;
    Heap[int(T0)]=0;        //valor por defecto de variable a

    /**a:=10;*/
    T1=0;
    Heap[int(T1)]=10;

    /*  while a<20 do
        begin
            writeln(a);
            a := a + 1;
        end;
    */
    L1:              //label para continuar iterando. Servirá para el continue
    T2=0;
    T3=Heap[int(T2)];   //OBTENEMOS el valor de a
    if (T3<20) {goto L3};
    goto L4;
    L3:
        T4=1;       //condicional devuelve true
        goto L5;
    L4:
        T4=0;       // condicional devuelve false
    L5:
    if (T4 == 1) {goto L2};
    goto L6;
    L2:
        // todas las instrucciones que lleva en el cuerpo

        /*writeln(a)*/
        T5=0;
        T6=Heap[int(T5)];
        fmt.Printf("%d", int(T6));
        fmt.Printf("%c",10);

        /*a:=a+1;*/
        T7=0;
        T8=Heap[int(T7)];
        T9=T8+1;

        T10=0;
        Heap[int(T10)]=T9;

       /*continue;*/
       goto L1;
      
       /*writeln(33);*/
       fmt.Printf("%d", 33);
       fmt.Printf("%c", 10);

        goto L1;        //volvemos al inicio para continuar evaluando

    L6:
        // Etiqueta de salida del while. Servirá para break. 

    return;
}
