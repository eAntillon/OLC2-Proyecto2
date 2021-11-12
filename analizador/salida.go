package main; 
import ( "fmt");
var heap [100000]float64; 
var stack [100000]float64;
var P, H float64;
var T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24,T25,T26,T27,T28,T29,T30,T31,T32,T33,T34,T35,T36,T37,T38,T39,T40,T41,T42,T43,T44,T45,T46,T47,T48,T49,T50,T51,T52,T53,T54,T55,T56,T57,T58,T59,T60,T61,T62,T63,T64,T65,T66,T67,T68,T69,T70,T71,T72,T73,T74,T75,T76,T77,T78,T79,T80,T81 float64;

func printString(){
T0 = 0;
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
/* funciones nativas */
func printArrNative(){
	/* PARAMETRO 1 */
	T68=P+1; 
	T69=stack[int(T68)];
	T69=T69+1; 
	/* PARAMETRO 2 */
	T70=T69+1; 
	T71=heap[int(T70)];
	/* PRINT */
	T72=heap[int(T69)];
	fmt.Printf("%c", int(91));
	T73=T70+1; 
	L12:
	if T72<=0 {goto L16;}
	T74=heap[int(T73)];
	T75=heap[int(T74)];
	if T75==-2 {goto L13;}
	goto L14;
	L13:
	T76=P+2; 
	stack[int(T76)]=T72;
	T76=P+3; 
	stack[int(T76)]=T73;
	T76=P+4; 
	stack[int(T76)]=T74;
	P=P+3;
	printArrNative();
	fmt.Printf(",");
	P=P-3;
	goto L15;
	L14:
	if T71==0 {goto L17;}
	if T71==1 {goto L18;}
	if T71==2 {goto L19;}
	L17:
	fmt.Printf("%f,", (T75));
	goto L20;
	L18:
	fmt.Printf("%d,", int(T75));
	goto L20;
	L19:
	fmt.Printf("%f,", (T75));
	L20:
	L15:
	T72=T72-1; 
	T73=T73+1; 
	goto L12;
	L16:
	fmt.Printf("%c", int(8));
	fmt.Printf("%c", int(93));
	/* PARAMETRO 3 */
	T77=P-1; 
	T78=stack[int(T77)];
	T72=T78; 
	/* PARAMETRO 4 */
	T79=P-0; 
	T80=stack[int(T79)];
	T73=T80; 
	return;
}


func main(){
	T3=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=3;
	H = H + 1;
	T4=H; 
	heap[int(H)]=1;
	H = H + 1;
	T5=H; 
	H = H + 1;
	T6=H; 
	H = H + 1;
	T7=H; 
	H = H + 1;
	/* VALORES */
	T8=H; 
	heap[int(T8)]=21.0;
	H = H + 1;
	heap[int(T5)]=T8;
	T9=H; 
	heap[int(T9)]=3.0;
	H = H + 1;
	heap[int(T6)]=T9;
	T10=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=4;
	H = H + 1;
	T11=H; 
	heap[int(H)]=1;
	H = H + 1;
	T12=H; 
	H = H + 1;
	T13=H; 
	H = H + 1;
	T14=H; 
	H = H + 1;
	T15=H; 
	H = H + 1;
	/* VALORES */
	T16=H; 
	heap[int(T16)]=4.0;
	H = H + 1;
	heap[int(T12)]=T16;
	T17=H; 
	heap[int(T17)]=3.0;
	H = H + 1;
	heap[int(T13)]=T17;
	T18=H; 
	heap[int(T18)]=4.0;
	H = H + 1;
	heap[int(T14)]=T18;
	T19=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=12;
	H = H + 1;
	T20=H; 
	heap[int(H)]=1;
	H = H + 1;
	T21=H; 
	H = H + 1;
	T22=H; 
	H = H + 1;
	T23=H; 
	H = H + 1;
	T24=H; 
	H = H + 1;
	T25=H; 
	H = H + 1;
	T26=H; 
	H = H + 1;
	T27=H; 
	H = H + 1;
	T28=H; 
	H = H + 1;
	T29=H; 
	H = H + 1;
	T30=H; 
	H = H + 1;
	T31=H; 
	H = H + 1;
	T32=H; 
	H = H + 1;
	/* VALORES */
	T33=H; 
	heap[int(T33)]=55.0;
	H = H + 1;
	heap[int(T21)]=T33;
	T34=H; 
	heap[int(T34)]=234.0;
	H = H + 1;
	heap[int(T22)]=T34;
	T35=H; 
	heap[int(T35)]=1.0;
	H = H + 1;
	heap[int(T23)]=T35;
	T36=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=2;
	H = H + 1;
	T37=H; 
	heap[int(H)]=1;
	H = H + 1;
	T38=H; 
	H = H + 1;
	T39=H; 
	H = H + 1;
	/* VALORES */
	T40=H; 
	heap[int(T40)]=39394.0;
	H = H + 1;
	heap[int(T38)]=T40;
	T41=H; 
	heap[int(T41)]=4.0;
	H = H + 1;
	heap[int(T39)]=T41;
	/* INSERTAR TIPO */
	heap[int(T37)]=1;
	T42=H; 
	heap[int(T24)]=T36;
	T43=H; 
	heap[int(T43)]=1.0;
	H = H + 1;
	heap[int(T25)]=T43;
	T44=H; 
	heap[int(T44)]=1.0;
	H = H + 1;
	heap[int(T26)]=T44;
	T45=H; 
	heap[int(T45)]=1.0;
	H = H + 1;
	heap[int(T27)]=T45;
	T46=H; 
	heap[int(T46)]=1.0;
	H = H + 1;
	heap[int(T28)]=T46;
	T47=H; 
	heap[int(T47)]=1.0;
	H = H + 1;
	heap[int(T29)]=T47;
	T48=H; 
	heap[int(T48)]=1.0;
	H = H + 1;
	heap[int(T30)]=T48;
	T49=H; 
	heap[int(T49)]=3.0;
	H = H + 1;
	heap[int(T31)]=T49;
	T50=H; 
	heap[int(H)]=-2;
	H = H + 1;
	heap[int(H)]=2;
	H = H + 1;
	T51=H; 
	heap[int(H)]=1;
	H = H + 1;
	T52=H; 
	H = H + 1;
	T53=H; 
	H = H + 1;
	/* VALORES */
	T54=H; 
	heap[int(T54)]=4.0;
	H = H + 1;
	heap[int(T52)]=T54;
	T55=H; 
	heap[int(T55)]=4.0;
	H = H + 1;
	heap[int(T53)]=T55;
	/* INSERTAR TIPO */
	heap[int(T51)]=1;
	T56=H; 
	heap[int(T32)]=T50;
	/* INSERTAR TIPO */
	heap[int(T20)]=1;
	T57=H; 
	heap[int(T15)]=T19;
	/* INSERTAR TIPO */
	heap[int(T11)]=1;
	T58=H; 
	heap[int(T7)]=T10;
	/* INSERTAR TIPO */
	heap[int(T4)]=1;
	T59=P+1; 
	stack[int(T59)]=T3;
	/* ACCESO ARRAY */
	T60=stack[int(1)];
	T61=0; 
	/* ACCESO POS 3.0  */
	T62=T60; 
	T65=3.0; 
	T63=heap[int(T62)];
	if T63!=-2 {goto L4;}
	T62=T62+1; 
	T63=heap[int(T62)];
	T64=T63; 
	T62=T62+1; 
	if T65>T64 {goto L5;}
	T62=T62+T65; 
	T63=heap[int(T62)];
	T61=heap[int(T63)];
	if T61==-2 {goto L6;}
	goto L3;
	L6:
	T60=T63; 
	goto L3;
	L4:
	fmt.Printf("No es un array");
	goto L3;
	L5:
	fmt.Printf("%c", int(66));
	fmt.Printf("%c", int(111));
	fmt.Printf("%c", int(117));
	fmt.Printf("%c", int(110));
	fmt.Printf("%c", int(100));
	fmt.Printf("%c", int(115));
	fmt.Printf("%c", int(69));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(111));
	fmt.Printf("%c", int(114));
	L3:
	/* ACCESO POS 1.0  */
	T62=T60; 
	T66=1.0; 
	T63=heap[int(T62)];
	if T63!=-2 {goto L8;}
	T62=T62+1; 
	T63=heap[int(T62)];
	T64=T63; 
	T62=T62+1; 
	if T66>T64 {goto L9;}
	T62=T62+T66; 
	T63=heap[int(T62)];
	T61=heap[int(T63)];
	if T61==-2 {goto L10;}
	goto L7;
	L10:
	T60=T63; 
	goto L7;
	L8:
	fmt.Printf("No es un array");
	goto L7;
	L9:
	fmt.Printf("%c", int(66));
	fmt.Printf("%c", int(111));
	fmt.Printf("%c", int(117));
	fmt.Printf("%c", int(110));
	fmt.Printf("%c", int(100));
	fmt.Printf("%c", int(115));
	fmt.Printf("%c", int(69));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(114));
	fmt.Printf("%c", int(111));
	fmt.Printf("%c", int(114));
	L7:
	if T61!=-2 {goto L11;}
	T61=T63; 
	L11:
	/* PRINT */
	T67=P+3; 
	stack[int(T67)]=T61;
	P=P+2;
	printArrNative();
	T67=stack[int(P)];
	P=P-2;
	fmt.Printf("%c", int(10));
}