package main; 
import ( "fmt" );
var heap [100000]float64; 
var stack [100000]float64;
var P, H float64;
var T0,T1,T2,T3,T4,T5,T6 float64;

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
	T3=5.0+5.0; 
	fmt.Printf("%d", int(T3));
	T4=1.0*100.0; 
	T5=T4/2.0; 
	fmt.Printf("%f", T5);
	fmt.Printf("%c", int(10));
	if 5.0>0.0 {goto L2;}
	goto L3;
	L2:
	fmt.Printf("%c", int(116));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(117));
	fmt.Printf("%c", int(101));
	goto L4;
	L3:
	fmt.Printf("%c", int(102));
	fmt.Printf("%c", int(97));
	fmt.Printf("%c", int(108));
	fmt.Printf("%c", int(115));
	fmt.Printf("%c", int(101));
	L4:
	fmt.Printf("%c", int(10));
	goto L5;
	goto L6;
	L5:
	fmt.Printf("%c", int(116));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(117));
	fmt.Printf("%c", int(101));
	goto L7;
	L6:
	fmt.Printf("%c", int(102));
	fmt.Printf("%c", int(97));
	fmt.Printf("%c", int(108));
	fmt.Printf("%c", int(115));
	fmt.Printf("%c", int(101));
	L7:
	fmt.Printf("%c", int(10));
	if 5.0==10.0 {goto L8;}
	goto L9;
	goto L11;
	goto L10;
	if ==False {goto L12;}
	goto L13;
	L12:
	fmt.Printf("%c", int(116));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(117));
	fmt.Printf("%c", int(101));
	goto L14;
	L13:
	fmt.Printf("%c", int(102));
	fmt.Printf("%c", int(97));
	fmt.Printf("%c", int(108));
	fmt.Printf("%c", int(115));
	fmt.Printf("%c", int(101));
	L14:
	fmt.Printf("%c", int(10));
	if 5.0==10.0 {goto L15;}
	goto L16;
	L15:
	if 1.0!=1.0 {goto L17;}
	goto L16;
	L17:
	fmt.Printf("%c", int(116));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(117));
	fmt.Printf("%c", int(101));
	goto L18;
	L16:
	fmt.Printf("%c", int(102));
	fmt.Printf("%c", int(97));
	fmt.Printf("%c", int(108));
	fmt.Printf("%c", int(115));
	fmt.Printf("%c", int(101));
	L18:
	fmt.Printf("%c", int(10));
	if 5.0==10.0 {goto L19;}
	goto L20;
	L20:
	if 1.0==1.0 {goto L19;}
	goto L21;
	L19:
	fmt.Printf("%c", int(116));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(117));
	fmt.Printf("%c", int(101));
	goto L22;
	L21:
	fmt.Printf("%c", int(102));
	fmt.Printf("%c", int(97));
	fmt.Printf("%c", int(108));
	fmt.Printf("%c", int(115));
	fmt.Printf("%c", int(101));
	L22:
	fmt.Printf("%c", int(10));
}