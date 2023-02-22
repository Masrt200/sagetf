#include <stdio.h>
int main(){
	srand(time(NULL));
	int num1, num2;
	num1 = rand();
	num2 = rand();
	printf("%d %d", num1, num2);
	return 0;
}
