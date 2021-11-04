package main; 
import ( "fmt" );
var heap [100000]float64; 
var stack [100000]float64;
var P, H float64;
var T0,T1,T2,T3,T4,T5 float64;

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


func main(){
	T3=H; 
	heap[int(T3)]=1;
	H = H + 1;
	heap[int(H)]=0;
	H = H + 1;
	heap[int(H)]=2;
	H = H + 1;
	heap[int(H)]=1.0;
	H = H + 1;
	heap[int(H)]=23.0;
	H = H + 1;
	T4=4.0*3.0; 
	heap[int(H)]=T4;
	H = H + 1;
	stack[int(1)]=T3;
}