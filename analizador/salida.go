package main; 
import ( "fmt" );
var heap [100000]float64; 
var stack [100000]float64;
var P, H float64;
var T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19 float64;

func printString(){
T0 = P+0;
T1 = stack[int(T0)];
L0:
T2 = heap[int(T1)];
if T2 == -1 { goto L1;}
fmt.Printf("%c", int(T2));
T1 = T1 + 1; 
goto L0;
L1: 
return;
}

/* funciones */
func potenciaNativa(){
	/* ACCESO ID */
	T4=P+1; 
	T3=stack[int(T4)];
	T5=P+3; 
	stack[int(T5)]=T3;
	/* INSTRUCCION WHILE */
	L4:
	/* ACCESO ID */
	T7=P+2; 
	T6=stack[int(T7)];
	:
	/* ACCESO ID */
	T9=P+3; 
	T8=stack[int(T9)];
	/* ACCESO ID */
	T11=P+1; 
	T10=stack[int(T11)];
	T12=T8+T10; 
	stack[int(3)]=T12;
	/* ACCESO ID */
	T14=P+2; 
	T13=stack[int(T14)];
	T15=T13-1.0; 
	stack[int(2)]=T15;
	goto L4;
	:
	/* ACCESO ID */
	T17=P+3; 
	T16=stack[int(T17)];
	stack[int(P)]=T16;
	goto L2;
	L2:
	return;
}

func main(){
	T18=P+2; 
	stack[int(T18)]=5.0;
	T18=T18+1; 
	stack[int(T18)]=7.0;
	P=P+1;
	potenciaNativa();
	T18=stack[int(P)];
	P=P-1;
	/* PRINT */
	fmt.Printf("%f", T18);
	fmt.Printf("%c", int(10));
}