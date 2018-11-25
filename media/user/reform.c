#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

//rand function (perhaps) goes up to only 2^15; depends from implementation to implementation. So I took mod 256 for safety.
unsigned int rand8(){
	return rand()%256;
}

unsigned int rand16(){
	return rand()%256 + 256*(rand()%256);
}

unsigned int rand32(){
	return rand16() + 65536*rand16();
}

unsigned long long int rand64(){
	return (unsigned long long int) rand32() + ((unsigned long long int) 4294967296)*((unsigned long long int) rand32());
}


int S0(unsigned int x, unsigned int y){ //actually just takes two 8-bit numbers
	unsigned int temp = ((x+y)&255)<<2;
	unsigned int end = temp/256;
	return end + temp&255;
}

int S1(unsigned int x, unsigned int y){ //actually just takes two 8-bit numbers
	unsigned int temp = ((x+y+1)&255)<<2;
	unsigned int end = temp/256;
	return end + temp&255;
}

unsigned int G(unsigned int a){
	unsigned int a3 = a&255;
	a >>= 8;
	unsigned int a2 = a&255;
	a >>= 8;
	unsigned int a1 = a&255;
	a >>= 8;
	unsigned int a0 = a&255;
	unsigned int d1 = a0 ^ a1;
	unsigned int d2 = a2 ^ a3;
	unsigned int c1 = S1(d1,d2);
	unsigned int c2 = S0(d2,c1);
	unsigned int c0 = S0(a0,c1);
	unsigned int c3 = S1(a3,c2);
	return c3 + 256*(c2 + 256*(c1 + 256*c0));
}

unsigned int fk(unsigned int a, unsigned int b){
	unsigned int a3 = a&255;
	a >>= 8;
	unsigned int a2 = a&255;
	a >>= 8;
	unsigned int a1 = a&255;
	a >>= 8;
	unsigned int a0 = a&255;
	unsigned int b3 = b&255;
	b >>= 8;
	unsigned int b2 = b&255;
	b >>= 8;
	unsigned int b1 = b&255;
	b >>= 8;
	unsigned int b0 = b&255;
	b >>= 8;
	unsigned int d1 = a0 ^ a1;
	unsigned int d2 = a2 ^ a3;
	unsigned int c1 = S1(d1, d2^b0);
	unsigned int c2 = S0(d2, c1^b1);
	unsigned int c0 = S0(a0, c1^b2);
	unsigned int c3 = S1(a3, c2^b3);
	return c3 + 256*(c2 + 256*(c1 + 256*c0));
}


//f(a,b) = G(a0, a1 ^ b1, a2 ^ b2, a3)
unsigned int f(unsigned int a, unsigned short b){ 
	unsigned int b2 = b&255;
	b >>= 8;
	unsigned int b1 = b&255;
	unsigned int a3 = a&255;
	a >>= 8;
	unsigned int a2 = a&255;
	a >>= 8;
	unsigned int a1 = a&255;
	a >>= 8;
	unsigned int a0 = a&255;
	unsigned int inp = a3 + 256*((a2 ^ b2) + 256*((a1 ^ b1) + 256*a0));
	return G(inp);
}

unsigned int theta_L(unsigned int a){
	unsigned int a3 = a&255;
	a >>= 8;
	unsigned int a2 = a&255;
	a >>= 8;
	unsigned int a1 = a&255;
	a >>= 8;
	unsigned int a0 = a&255;
	return 256*(a1 + 256*a0);
}

unsigned int theta_R(unsigned int a){
	unsigned int a3 = a&255;
	a >>= 8;
	unsigned int a2 = a&255;
	a >>= 8;
	unsigned int a1 = a&255;
	a >>= 8;
	unsigned int a0 = a&255;
	return 256*(a3 + 256*a2);
}

unsigned int* produce_keys(unsigned long long int K){
	unsigned int Kr = K&4294967295;
	K >>= 32;
	unsigned int Kl = K&4294967295;
	unsigned int * B = (unsigned int *) malloc(sizeof(unsigned int)*9);
	B[0] = 0;
	B[1] = Kl;
	B[2] = Kr;
	int i;
	for(i = 3; i<9; i++){
		B[i] = fk(B[i-2], B[i-1]^B[i-3]);
	}
	return &B[2];
}

unsigned int* produce_M(unsigned int * B){
	unsigned int * M = (unsigned int *) malloc(sizeof(unsigned int)*4);
	M[1] = B[3] ^ theta_R(B[1]);
	//unsigned int N[1] = B[3] ^ B[4] ^ theta_L(B[1]);
	M[2] = theta_L(B[1]) ^ theta_L(B[2]);
	//unsigned int N[2] = theta_R(B[1]) ^ theta_R(B[2]);
	M[3] = B[5] ^ B[6] ^ theta_R(B[1]);
	//unsigned int N[3] = B[5] ^ theta_L(B[1]);
	return M;
}

unsigned int* produce_N(unsigned int * B){
	unsigned int * N = (unsigned int *) malloc(sizeof(unsigned int)*4);
	//unsigned int M[1] = B[3] ^ theta_R(B[1]);
	N[1] = B[3] ^ B[4] ^ theta_L(B[1]);
	//unsigned int M[2] = theta_L(B[1]) ^ theta_L(B[2]);
	N[2] = theta_R(B[1]) ^ theta_R(B[2]);
	//unsigned int M[3] = B[5] ^ B[6] ^ theta_R(B[1]);
	N[3] = B[5] ^ theta_L(B[1]);
	return N;
}

unsigned long long int encode_FEAL(unsigned long long int P, unsigned short* K, int n){
	unsigned int Pr = P&4294967295;
	P >>= 32;
	unsigned int Pl = P&4294967295;
	unsigned int L[n+1];
	unsigned int R[n+1];
	L[0] = Pl ^ ( (((unsigned int)(K[4]))<<16) + K[5]) ;
	R[0] = L[0] ^ Pr ^ ( (((unsigned int)(K[6]))<<16) + K[7]) ;
	int i;
	for(i = 1; i<= n ; i++){
		L[i] = R[i-1];
		R[i] = L[i-1] ^ f(R[i-1], K[i-1]);
	}
	unsigned long long int Cl = R[n]^( (((unsigned int)(K[8]))<<16) + K[9]) ;
	unsigned int Cr = R[n]^( (((unsigned int)(K[10]))<<16 )+ K[11])^L[n] ;
	unsigned long long int C = (Cl<<32) + Cr;
	return C;
}

unsigned long long int decode_FEAL(unsigned long long int C, unsigned short* K, int n){
	unsigned int Cr = C&4294967295;
	C >>= 32;
	unsigned int Cl = C&4294967295;
	unsigned int L[n+1];
	unsigned int R[n+1];
	R[n] = Cl ^( (((unsigned int)(K[8]))<<16) + K[9]) ;
	L[n] = Cr ^ R[n] ^ ( (((unsigned int)(K[10]))<<16) + K[11]);
	int i;
	for(i = n; i>= 1 ; i--){
		R[i - 1] = L[i];
		L[i - 1] = R[i] ^ f(R[i-1], K[i-1]);
	}
	unsigned long long int Pl = L[0]^( (((unsigned int)(K[4]))<<16) + K[5]) ;
	unsigned int Pr = R[0]^L[0]^( (((unsigned int)(K[6]))<<16) + K[7]) ;
	unsigned long long int P = (Pl<<32) + Pr;
	return P;
}


unsigned long long int encode_feal_4(unsigned long long int P, unsigned int* M, unsigned int* N){

	unsigned int PR = P&4294967295;
	P >>= 32;
	unsigned int PL = P&4294967295;

	unsigned int X0 = PL ^ M[1];
	unsigned int Y0 = PL ^ PR ^ N[1];
	unsigned int X1 = X0 ^ G(Y0);
	unsigned int Y1 = Y0 ^ G(X1);
	unsigned int X2 = X1 ^ G(Y1 ^ M[2]);
	unsigned int Y2 = Y1 ^ G(X2 ^ N[2]);
	unsigned int CL = Y2 ^ N[3];
	unsigned int CR = X2 ^ M[3] ^ CL;

	unsigned long long int C = ((unsigned long long int) CL << 32) + CR;
	return C;
}


unsigned long long int encode_feal_4_another(unsigned long long int P, unsigned int M1, unsigned int M2, unsigned int M3, unsigned int N1, unsigned int N2, unsigned int N3){
	unsigned int PR = P&4294967295;
	P >>= 32;
	unsigned int PL = P&4294967295;

	unsigned int X0 = PL ^ M1;
	unsigned int Y0 = PL ^ PR ^ N1;
	unsigned int X1 = X0 ^ G(Y0);
	unsigned int Y1 = Y0 ^ G(X1);
	unsigned int X2 = X1 ^ G(Y1 ^ M2);
	unsigned int Y2 = Y1 ^ G(X2 ^ N2);
	unsigned int CL = Y2 ^ N3;
	unsigned int CR = X2 ^ M3 ^ CL;

	unsigned long long int C = ((unsigned long long int) CL << 32) + CR;
	return C;
}

unsigned long long int decode_feal_4(unsigned long long int C, unsigned int* M, unsigned int* N){
	
	unsigned int CR = C&4294967295;
	C >>= 32;
	unsigned int CL = C&4294967295;

	unsigned int Y2 = CL ^ N[3];
	unsigned int X2 = CR ^ CL ^ M[3];
	unsigned int Y1 = Y2 ^ G(X2 ^ N[2]);
	unsigned int X1 = X2 ^ G(Y1 ^ M[2]);
	unsigned int Y0 = Y1 ^ G(X1);
	unsigned int X0 = X1 ^ G(Y0);
	unsigned int PL = X0 ^ M[1];
	unsigned int PR = Y0 ^ PL ^ N[1];

	unsigned long long int P = ((unsigned long long int) PL << 32) + PR;
	return P;
}


// unsigned int solve1(unsigned int a, unsigned int b){ //find x for which G(x ^ a) = b;
// 	unsigned int a0 = a&255;
// 	a >>= 8;
// 	unsigned int a1 = a&255;
// 	a >>= 8;
// 	unsigned int a2 = a&255;
// 	a >>= 8;
// 	unsigned int a3 = a&255;
// 	unsigned int b0 = b&255;
// 	b >>= 8;
// 	unsigned int b1 = b&255;
// 	b >>= 8;
// 	unsigned int b2 = b&255;
// 	b >>= 8;
// 	unsigned int b3 = b&255;
// 	b >>= 8;


// 	unsigned int z1,z2, x0, x1, x2, x3;
// 	for(z1 = 0 ; z1 < 256 ; z1 ++){
// 		for(z2 = 0 ; z2 < 256 ; z2 ++){
// 			if(S1(z1 ^ a0 ^ a1 , z2 ^ a2 ^ a3) == b1){
// 				for(x0 = 0 ; x0 < 256 ; x0 ++){
// 					for(x3 = 0 ; x3 < 256 ; x3 ++){
// 						if(S0(b1, z2 ^ a2 ^ a3) == b2 && S0(b1 , x0 ^ a0) == b0 && S1(b2, x3 ^ a3) == b3){
// 							x1 = z1 ^ x0;
// 							x2 = z2 ^ x3;
// 							return x0 + 256*(x1 + 256*(x2 + 256*x3));
// 						}
// 					}
// 				}
// 			}
// 		}
// 	}
// 	printf("Nno sol1\n");
// 	return 0;
// }

// unsigned int solve2(unsigned int a, unsigned int b, unsigned int d){ // G(x ^ a) ^ G(x ^ b) = d
// 	unsigned int a0 = a&255;
// 	a >>= 8;
// 	unsigned int a1 = a&255;
// 	a >>= 8;
// 	unsigned int a2 = a&255;
// 	a >>= 8;
// 	unsigned int a3 = a&255;
// 	unsigned int b0 = b&255;
// 	b >>= 8;
// 	unsigned int b1 = b&255;
// 	b >>= 8;
// 	unsigned int b2 = b&255;
// 	b >>= 8;
// 	unsigned int b3 = b&255;
// 	b >>= 8;
// 	unsigned int d0 = d&255;
// 	d >>= 8;
// 	unsigned int d1 = d&255;
// 	d >>= 8;
// 	unsigned int d2 = d&255;
// 	d >>= 8;
// 	unsigned int d3 = d&255;
// 	d >>= 8;

// 	unsigned int z1,z2,x0,x1,x2,x3,p0,p1,p2,p3,q0,q1,q2,q3;
// 	for(z1 = 0 ; z1 < 256 ; z1++){
// 		for(z2 = 0 ; z2 < 256 ; z2++){
// 			p1 = S1(z1 ^ a0 ^ a1 , z2 ^ a2 ^ a3);
// 			q1 = S1(z1 ^ b0 ^ b1 , z2 ^ a2 ^ a3); 
// 			if(p1 ^ q1 == d1){
// 				p2 = S0(p1, z2 ^ a2 ^ a3);
// 				q2 = S0(q1, z2 ^ b2 ^ b3);
// 				if(p2 ^ q2 == d2){
// 					for(x0 = 0 ; x0 < 256 ; x0++){
// 						for(x3 = 0 ; x3 < 256 ; x3++){
// 							if(S0(x0 ^ a0, p1) ^ S0(x0 ^ b0, q1) == d0 && S1(x3 ^ a3, p2) ^ S1(x3 ^ b3, q3) == d3){
// 								return x0 + 256*(x1 + 256*(x2 + 256*x3));
// 							}
// 						}
// 					}
// 				}
// 			}
// 		}
// 	}
// 	printf("No sol2\n");
// 	return 0;
// }

// unsigned int solve3(unsigned int a, unsigned int b, unsigned int c, unsigned int d, unsigned int e){
// 	//naive; can be improved slightly
// 	for(unsigned int x = 0 ; x <= 4294967295 ; x++){
// 		if(G(x ^ a) ^ G(x ^ b) == d && G(x ^ a) ^ G(x ^ c) == e){
// 			return x;
// 		}
// 	}

// 	printf("No sol3\n");
// 	return 0;
// }

//I have not defined Qi and Di explicitly. I have also not defined them as a separate function, as it would take more time.
unsigned long long int * choose_plaintexts(){
	unsigned long long int * P = (unsigned long long int *) malloc(sizeof(unsigned long long int)*20);

	//In all 7*64 + 9*32 = 736 plaintexts at random.

	P[0] = rand64();
	P[12] = rand64();
	P[14] = rand64();
	P[16] = rand64();
	P[17] = rand64();
	P[18] = rand64();
	P[19] = rand64();

	P[5] = ((unsigned long long int) rand32()) << 32;
	P[6] = ((unsigned long long int) rand32()) << 32;
	P[7] = ((unsigned long long int) rand32()) << 32;
	P[8] = ((unsigned long long int) rand32()) << 32;
	P[9] = ((unsigned long long int) rand32()) << 32;
	P[10] = ((unsigned long long int) rand32()) << 32;
	P[11] = ((unsigned long long int) rand32()) << 32;
	P[13] = ((unsigned long long int) rand32()) << 32;
	P[15] = ((unsigned long long int) rand32()) << 32;

	P[1] = ((P[0] >> 32) ^ 0x80800000) << 32;
	P[2] = ((P[0] >> 32) ^ 0x00008080) << 32;
	P[3] = ((P[0] >> 32) ^ 0x40400000) << 32;
	P[4] = ((P[0] >> 32) ^ 0x00004040) << 32;


	for(int i = 1 ; i <= 11 ; i++){
		P[i] += (P[i] >> 32) ^ (P[0] >> 32) ^ (P[0] & 4294967295);
	}

	P[13] += (P[13] >> 32) ^ (P[12] >> 32) ^ (P[12] & 4294967295);
	P[15] += (P[15] >> 32) ^ (P[13] >> 32) ^ (P[13] & 4294967295);
	return P;
}

unsigned long long int* find_chosentexts(unsigned long long int * P, unsigned int * M, unsigned int * N){
	unsigned long long int* C = (unsigned long long int*) malloc (sizeof(unsigned long long int) * 20);
	for(int i = 0 ; i < 20 ; i++){
		C[i] = encode_feal_4(P[i] , M, N);
	}
	return C;
}


void MandN(unsigned long long int* P, unsigned long long int* C){
	// for(int i = 0 ; i < 20 ; i++){
	// 	printf("%llu %d\n", P[i], i);
	// 	printf("%llu %d\n", C[i] , i);
	// }
	unsigned int * PL = (unsigned int *) malloc (sizeof(unsigned int)*20);
	unsigned int * PR = (unsigned int *) malloc (sizeof(unsigned int)*20);
	unsigned int * CL = (unsigned int *) malloc (sizeof(unsigned int)*20);
	unsigned int * CR = (unsigned int *) malloc (sizeof(unsigned int)*20);

	for(int i = 0 ; i < 20 ; i++){
		PR[i] = (unsigned int) (P[i]&4294967295);
		PL[i] = (unsigned int) (P[i] >> 32);
		CR[i] = (unsigned int) (C[i]&4294967295);
		CL[i] = (unsigned int) (C[i] >> 32);
	}

	// for(int i = 0 ; i < 20 ; i++){
	// 	printf("%d %u %u %u %u\n", i,  PR[i] , PL[i] , CR[i] , CL[i]);
	// }

	unsigned int W, V0, U0, U12, U13 , U14, U15, V12, V13, V14, V15, V16, N1, N2, N3, M1, M2, M3;
	unsigned int Y1_0 , Y1_17 , Y1_18 , X1_0 , X1_17 , X1_18 , X2_0 , X2_17, X2_18, Y2_0 , Y2_17 , Y2_18;

	//printf("%u\n", CL[0] ^ CR[0] ^ CL[1] ^ CR[1]);

	for(W = 0 ; W <= 4294967294 ; W++ ){
		
		//printf("%u %u %u %u\n", G(W ^ CL[0] ^ CR[0]) , G(W ^ CL[1] ^ CR[1]) , CL[0] , CL[1]);
		if( !(G(W ^ CL[0] ^ CR[0]) ^ G(W ^ CL[1] ^ CR[1]) ^ CL[0] ^ CL[1] ^ 0x02000000) && !(G(W ^ CL[0] ^ CR[0]) ^ G(W ^ CL[2] ^ CR[2]) ^ CL[0] ^ CL[2] ^ 0x00000002) ){ //solve3
			if( ( !(G(W ^ CL[0] ^ CR[0]) ^ G(W ^ CL[3] ^ CR[3]) ^ CL[0] ^ CL[3] ^ 0x01000000) || !(G(W ^ CL[0] ^ CR[0]) ^ G(W ^ CL[3] ^ CR[3]) ^ CL[0] ^ CL[3] ^ 0x03000000) ) && ( !(G(W ^ CL[0] ^ CR[0]) ^ G(W ^ CL[4] ^ CR[4]) ^ CL[0] ^ CL[4] ^ 0x00000001 ) || !( G(W ^ CL[0] ^ CR[0]) ^ G(W ^ CL[4] ^ CR[4]) ^ CL[0] ^ CL[4] ^ 0x00000003) ))
			{
				printf("W = %u\n", W);
				//printf("%u\n", W);
				//we have the valid values of W here.
				for(V0 = 0 ; V0 <= 4294967294 ; V0 ++){
					if( !(G(PL[0] ^ V0) ^ G(PL[5]^V0) ^ CL[0] ^ CL[5] ^ G(CL[0] ^ CR[0] ^ W) ^ G(CL[5] ^ CR[5] ^ W))  && !(G(PL[0] ^ V0) ^ G(PL[6]^V0) ^ CL[0] ^ CL[6] ^ G(CL[0] ^ CR[0] ^ W) ^ G(CL[6] ^ CR[6] ^ W)) )
					{
						U0 = CL[0] ^ G(PL[0] ^ V0) ^ G(CL[0] ^ CR[0] ^ W);
						printf("U0 = %u , V0 = %u\n", U0 , V0);
						if(!(CL[7] ^ U0 ^ G(PL[7] ^ V0) ^ G(CL[7] ^ CR[7] ^ W)) && !(CL[8] ^ U0 ^ G(PL[8] ^ V0) ^ G(CL[8] ^ CR[8] ^ W)) && !(CL[9] ^ U0 ^ G(PL[9] ^ V0) ^ G(CL[9] ^ CR[9] ^ W)) && !(CL[10] ^ U0 ^ G(PL[10] ^ V0) ^ G(CL[10] ^ CR[10] ^ W)) && !(CL[11] ^ U0 ^ G(PL[11] ^ V0) ^ G(CL[11] ^ CR[11] ^ W)))
						{
							U12 = U0 ^ PL[0] ^ PR[0] ^ PL[12] ^ PR[12];
							U13 = U12;
							U14 = U0 ^ PL[0] ^ PR[0] ^ PL[14] ^ PR[14];
							U15 = U14;
							//got all valid W,V0,U0
							for(V12 = 0 ; V12 <= 4294967294 ; V12 ++){
								if( !(G(PL[12] ^ V12) ^ G(CL[12] ^ CR[12] ^ W) ^ CL[12] ^ U12))
								{
									for(V14 = 0 ; V14 <= 4294967294 ; V14 ++ ){
										if( !(G(PL[14] ^ V14) ^ G(CL[14] ^ CR[14] ^ W) ^ CL[14] ^ U14))
										{
											V13 = V12;
											V15 = V14;

											//finally, we try to find the key constants
											for(N1 = 0 ; N1 <= 4294967294 ; N1 ++){
												if( !(G(PL[0] ^ PR[0] ^ N1) ^ G(PL[12] ^ PR[12] ^ N1) ^ V0 ^ V12) && !(G(PL[0] ^ PR[0] ^ N1) ^ G(PL[14] ^ PR[14] ^ N1) ^ V0 ^ V14))
												{
													printf("N1 = %u\n", N1);
													//Y[0] = PL ^ PR ^ N1;
													//Vi = M1 ^ G(Qi ^ N1);
													//Vi ^ Vj = G(Qi ^ N1) ^ G(Qj ^ N1);
													V16 = V0 ^ G(PL[0] ^ PR[0] ^ N1) ^ G(PL[16] ^ PR[16] ^ N1);
													M1 = V0 ^ G(PL[0] ^ PR[0] ^ N1);
													//N3 = U0 ^ PL ^ PR ^ N1
													N3 = U0 ^ PL[0] ^ PR[0] ^ N1;

													X1_0 = PL[0] ^ M1 ^ G(PL[0] ^ PR[0] ^ N1);
													X1_17 = PL[17] ^ M1 ^ G(PL[17] ^ PR[17] ^ N1);
													X1_18 = PL[18] ^ M1 ^ G(PL[18] ^ PR[18] ^ N1);
													Y1_0 = PL[0] ^ PR[0] ^ N1 ^ G(X1_0);
													Y1_17 = PL[17] ^ PR[17] ^ N1 ^ G(X1_17);
													Y1_18 = PL[18] ^ PR[18] ^ N1 ^ G(X1_18);


													for(M2 = 0 ; M2 <= 65535*256 ; M2 += 256){
														if( !(G(Y1_0 ^ M2) ^ G(Y1_17 ^ M2) ^ X1_0 ^ X1_17 ^ CL[0] ^ CR[0] ^ CL[17] ^ CR[17]) && !(G(Y1_0 ^ M2) ^ G(Y1_18 ^ M2) ^ X1_0 ^ X1_18 ^ CL[0] ^ CR[0] ^ CL[18] ^ CR[18]))
														{
															printf("M2 = %u\n", M2);

															X2_0 = X1_0 ^ G(Y1_0 ^ M2);
															X2_17 = X1_17 ^ G(Y1_17 ^ M2);
															X2_18 = X1_18 ^ G(Y1_18 ^ M2);
															M3 = CR[0] ^ CL[0] ^ X2_0;
															if( !(CR[17] ^ CL[17] ^ X2_17 ^ M3) && !(CR[18] ^ CL[18] ^ X2_18 ^ M3)){
																Y2_0 = CL[0] ^ N3;
																Y2_17 = CL[17] ^ N3;
																Y2_18 = CL[18] ^ N3;
																for(N2 = 0 ; N2 <= 65535*256 ; N2 += 256){
																	if( !(G(X2_0 ^ N2) ^ Y1_0 ^ Y2_0 ) &&  !(G(X2_17 ^ N2) ^ Y1_17 ^ Y2_17 ) && ! (G(X2_18 ^ N2) ^ Y1_18 ^ Y2_18 ))
																	{
																		int b = 1;
																		for(int i = 0 ; i < 20 ; i++){
																			if(C[i] != encode_feal_4_another(P[i] , M1, M2, M3, N1, N2, N3))
																				b = 0;
																		}
																		if(b){
																			printf("M1 = %u , M2 = %u , M3 = %u , N1 = %u , N2 = %u , N3 = %u \n", M1, M2, M3, N1, N2, N3);
																		}
																		
																	}
																}
															}
														}
													}
												}
											}
										}
									}
								}
							}
						}
						
					}
				}
			}
		}
	}
	return;
	//G(D[0]^W) ^ G(D[1] ^ W) = CL[0] ^ CL[1] ^ 02000000
	//G(D[0]^W) ^ G(D[2] ^ W) = CL[0] ^ CL[2] ^ 00000002

}

/*Y1 = Y0 ^ G(X1) = Y0 ^ G(X0 ^ G(Y0)) = Y0 ^ G(PL ^ M1 ^ G(Y0)) = Y2 ^ G(X2 ^ N2) = CL ^ N3 ^ G(D ^ M3 ^ N2)
Hence,

CL ^ (Y0 ^ N3) ^ G(PL ^ M1 ^ G(Y0)) ^ G(D ^ M3 ^ N2) = 0


DEFINITIONS
Qi = PL[i] ^ PR[i]
Di = CL[i] ^ CR[i]
Ui = Y0[i] ^ N3
Vi = M1 ^ G(Y0[i])
W = M3 ^ N2

Thus, 
CL[i] ^ U[i] ^ G(PL[i] ^ V[i]) ^ G(D[i] ^ W) = 0

for 0 <= i <= 11, we have Y0 = Q[i] ^ N1 and G(Y0) is constant, hence U[i] = U0 and V[i] = V0, so

CL[i] ^ U0 ^ G(PL[i] ^ V0) ^ G(D[i] ^ W) = 0 for all 0 <= i <= 11

So,
CL[i] ^ G(PL[i] ^ V0) ^ G(D[i] ^ W) ^ CL[0] ^ G(PL[0] ^ V0) ^ G(D[0] ^ W) = 0

if we knew G(PL[i] ^ V0) ^ G(PL[0] ^ V0), we would obtain an equation for W alone.

G(D[0]^W) ^ G(D[1] ^ W) = CL[0] ^ CL[1] ^ 02000000
G(D[0]^W) ^ G(D[2] ^ W) = CL[0] ^ CL[2] ^ 00000002

Use the solve3 function to obtain solutions for W. Check, for these W, whether
G(D[0]^W) ^ G(D[3] ^ W) ^ CL[0] ^ CL[3] = 01000000 , 03000000
G(D[0]^W) ^ G(D[4] ^ W) ^ CL[0] ^ CL[4] = 00000001 , 00000001

Typically, we get ~ 10 values of W. For each W, we can find values of V[0] and then U[0]. 
Usually, ~ 20 triples (W, U0 , V0).






*/



int main(){


	//printf("%d %d \n", 1123 == 1123 , 1421==2123);

	//printf("%d\n", 0x00002000);
	// printf("%d %d %d\n",rand(),rand(),rand());
	unsigned long long int K = (unsigned long long int) 22131856381	;
	unsigned long long int * P = choose_plaintexts();
	unsigned int* B = produce_keys(K);
	unsigned int* M = produce_M(B);
	unsigned int* N = produce_N(B);

	for(int i = 1 ; i <= 3 ; i++){
		printf("M%d  =  %u , N%d  =  %u \n", i, M[i] , i , N[i]);
	}

	unsigned long long int* C = find_chosentexts(P,M,N);

	MandN(P,C);

}