package main; 
import ( "fmt");
var heap [100000]float64; 
var stack [100000]float64;
var P, H float64;
var T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24,T25,T26,T27,T28,T29,T30,T31,T32,T33,T34,T35,T36,T37,T38,T39,T40,T41,T42,T43,T44,T45,T46,T47,T48,T49,T50,T51,T52,T53,T54,T55,T56,T57,T58,T59,T60,T61,T62,T63,T64,T65,T66,T67,T68,T69,T70,T71,T72,T73,T74,T75,T76,T77,T78,T79,T80,T81,T82,T83,T84,T85,T86,T87,T88,T89,T90,T91,T92,T93,T94,T95,T96,T97,T98,T99,T100,T101,T102,T103,T104,T105,T106,T107,T108,T109 float64;

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
func potenNativeFunc(){
    T66=P+1; 
    T65=stack[int(T66)];
    T67=P+3; 
    stack[int(T67)]=T65;
    L3:
    T69=P+2; 
    T68=stack[int(T69)];
    if T68>1.0 {goto L4};
    goto L5;
    L4:
    T71=P+3; 
    T70=stack[int(T71)];
    T73=P+1; 
    T72=stack[int(T73)];
    T74=T70*T72; 
    T75=P+3; 
    stack[int(T75)]=T74;
    T77=P+2; 
    T76=stack[int(T77)];
    T78=T76-1.0; 
    T79=P+2; 
    stack[int(T79)]=T78;
    goto L3;
    L5:
    T81=P+3; 
    T80=stack[int(T81)];
    stack[int(P)]=T80;
    goto L2;
    L2:
    return;
}


func main(){
	T3=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=2;
	H = H + 1;
	T4=H; 
	heap[int(H)]=1;
	H = H + 1;
	T5=H; 
	H = H + 1;
	T6=H; 
	H = H + 1;
	/* VALORES */
	T7=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=13;
	H = H + 1;
	T8=H; 
	heap[int(H)]=1;
	H = H + 1;
	T9=H; 
	H = H + 1;
	T10=H; 
	H = H + 1;
	T11=H; 
	H = H + 1;
	T12=H; 
	H = H + 1;
	T13=H; 
	H = H + 1;
	T14=H; 
	H = H + 1;
	T15=H; 
	H = H + 1;
	T16=H; 
	H = H + 1;
	T17=H; 
	H = H + 1;
	T18=H; 
	H = H + 1;
	T19=H; 
	H = H + 1;
	T20=H; 
	H = H + 1;
	T21=H; 
	H = H + 1;
	/* VALORES */
	T22=H; 
	heap[int(T22)]=12.0;
	H = H + 1;
	heap[int(T9)]=T22;
	T23=H; 
	heap[int(T23)]=9.0;
	H = H + 1;
	heap[int(T10)]=T23;
	T24=H; 
	heap[int(T24)]=4.0;
	H = H + 1;
	heap[int(T11)]=T24;
	T25=H; 
	heap[int(T25)]=99.0;
	H = H + 1;
	heap[int(T12)]=T25;
	T26=H; 
	heap[int(T26)]=56.0;
	H = H + 1;
	heap[int(T13)]=T26;
	T27=H; 
	heap[int(T27)]=34.0;
	H = H + 1;
	heap[int(T14)]=T27;
	T28=H; 
	heap[int(T28)]=78.0;
	H = H + 1;
	heap[int(T15)]=T28;
	T29=H; 
	heap[int(T29)]=22.0;
	H = H + 1;
	heap[int(T16)]=T29;
	T30=H; 
	heap[int(T30)]=1.0;
	H = H + 1;
	heap[int(T17)]=T30;
	T31=H; 
	heap[int(T31)]=3.0;
	H = H + 1;
	heap[int(T18)]=T31;
	T32=H; 
	heap[int(T32)]=10.0;
	H = H + 1;
	heap[int(T19)]=T32;
	T33=H; 
	heap[int(T33)]=13.0;
	H = H + 1;
	heap[int(T20)]=T33;
	T34=H; 
	heap[int(T34)]=120.0;
	H = H + 1;
	heap[int(T21)]=T34;
	/* INSERTAR TIPO */
	heap[int(T8)]=1;
	T35=H; 
	heap[int(T5)]=T7;
	T36=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=16;
	H = H + 1;
	T37=H; 
	heap[int(H)]=1;
	H = H + 1;
	T38=H; 
	H = H + 1;
	T39=H; 
	H = H + 1;
	T40=H; 
	H = H + 1;
	T41=H; 
	H = H + 1;
	T42=H; 
	H = H + 1;
	T43=H; 
	H = H + 1;
	T44=H; 
	H = H + 1;
	T45=H; 
	H = H + 1;
	T46=H; 
	H = H + 1;
	T47=H; 
	H = H + 1;
	T48=H; 
	H = H + 1;
	T49=H; 
	H = H + 1;
	T50=H; 
	H = H + 1;
	T51=H; 
	H = H + 1;
	T52=H; 
	H = H + 1;
	T53=H; 
	H = H + 1;
	/* VALORES */
	T54=H; 
	heap[int(T54)]=32.0;
	H = H + 1;
	heap[int(T38)]=T54;
	T55=7.0*3.0; 
	T56=H; 
	heap[int(T56)]=T55;
	H = H + 1;
	heap[int(T39)]=T56;
	T57=H; 
	heap[int(T57)]=7.0;
	H = H + 1;
	heap[int(T40)]=T57;
	T58=H; 
	heap[int(T58)]=89.0;
	H = H + 1;
	heap[int(T41)]=T58;
	T59=H; 
	heap[int(T59)]=56.0;
	H = H + 1;
	heap[int(T42)]=T59;
	T60=H; 
	heap[int(T60)]=909.0;
	H = H + 1;
	heap[int(T43)]=T60;
	T61=H; 
	heap[int(T61)]=109.0;
	H = H + 1;
	heap[int(T44)]=T61;
	T62=H; 
	heap[int(T62)]=2.0;
	H = H + 1;
	heap[int(T45)]=T62;
	T63=H; 
	heap[int(T63)]=9.0;
	H = H + 1;
	heap[int(T46)]=T63;
	T64=P+2; 
	stack[int(T64)]=9874.0;
	T64=T64+1; 
	stack[int(T64)]=0.0;
	P=P+1;
	potenNativeFunc();
	T64=stack[int(P)];
	P=P-1;
	T82=H; 
	heap[int(T82)]=T64;
	H = H + 1;
	heap[int(T47)]=T82;
	T83=H; 
	heap[int(T83)]=44.0;
	H = H + 1;
	heap[int(T48)]=T83;
	T84=H; 
	heap[int(T84)]=3.0;
	H = H + 1;
	heap[int(T49)]=T84;
	T85=820.0*10.0; 
	T86=H; 
	heap[int(T86)]=T85;
	H = H + 1;
	heap[int(T50)]=T86;
	T87=H; 
	heap[int(T87)]=11.0;
	H = H + 1;
	heap[int(T51)]=T87;
	T88=8.0*0.0; 
	T89=T88+8.0; 
	T90=H; 
	heap[int(T90)]=T89;
	H = H + 1;
	heap[int(T52)]=T90;
	T91=H; 
	heap[int(T91)]=10.0;
	H = H + 1;
	heap[int(T53)]=T91;
	/* INSERTAR TIPO */
	heap[int(T37)]=1;
	T92=H; 
	heap[int(T6)]=T36;
	/* INSERTAR TIPO */
	heap[int(T4)]=1;
	stack[int(1)]=T3;
	/* ACCESO ARRAY */
	T93=stack[int(1)];
	T94=0; 
	/* ACCESO POS 1.0  */
	T95=T93; 
	T98=1.0; 
	T96=heap[int(T95)];
	if T96!=-2 {goto L8;}
	T95=T95+1; 
	T96=heap[int(T95)];
	T97=T96; 
	T95=T95+1; 
	if T98>T97 {goto L9;}
	T95=T95+T98; 
	T96=heap[int(T95)];
	T94=heap[int(T96)];
	if T94==-2 {goto L10;}
	goto L7;
	L10:
	T93=T96; 
	goto L7;
	L8:
	fmt.Printf("No es un array");
	goto L7;
	L9:
	fmt.Printf("Posicion fuera de los limites del array");
	L7:
	if T94!=-2 {goto L11;}
	T94=T96; 
	L11:
	/* PRINT */
	fmt.Printf("%d", int(T94));
	T99=H; 
	heap[int(H)]=32;
	H = H + 1;
	heap[int(H)]=-1;
	H = H + 1;
	/* PRINT */
	stack[int(0)]=T99;
	printString();	/* PRINT */
	fmt.Printf("%d", int(1.0));
	T100=H; 
	heap[int(H)]=32;
	H = H + 1;
	heap[int(H)]=-1;
	H = H + 1;
	/* PRINT */
	stack[int(0)]=T100;
	printString();	/* ACCESO ARRAY */
	T101=stack[int(1)];
	T102=0; 
	/* ACCESO POS 1.0  */
	T103=T101; 
	T106=1.0; 
	T104=heap[int(T103)];
	if T104!=-2 {goto L13;}
	T103=T103+1; 
	T104=heap[int(T103)];
	T105=T104; 
	T103=T103+1; 
	if T106>T105 {goto L14;}
	T103=T103+T106; 
	T104=heap[int(T103)];
	T102=heap[int(T104)];
	if T102==-2 {goto L15;}
	goto L12;
	L15:
	T101=T104; 
	goto L12;
	L13:
	fmt.Printf("No es un array");
	goto L12;
	L14:
	fmt.Printf("Posicion fuera de los limites del array");
	L12:
	if T102!=-2 {goto L16;}
	T102=T104; 
	L16:
	T107=T102; 
	T108=heap[int(T107)];
	if T108!=-2 {goto L17;}
	T107=T107+1; 
	T108=heap[int(T107)];
	goto L18;
	L17:
	fmt.Printf("Error, no es de tipo array");
	L18:
	/* PRINT */
	fmt.Printf("%d", int(T108));
}