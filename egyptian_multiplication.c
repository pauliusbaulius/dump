#include <stdio.h>
#include <ctype.h>

static int multiplication(int a, int b);

int main() {

int a;
int b;
int product;

// User Input
printf("a:");
scanf("%i", &a);
printf("b:");
scanf("%i", &b);
printf("Given a: %i and b: %i \n", a, b);
product = multiplication(a,b);
printf("Output of multiplication a*b is %i \n", product);

return 0;
}

/* Implementation of ancient egyptian multiplication */
/* Without using "*","/","%" operators. */
/* Uses only "==","~","+","&",">>","<<" operators */ 
int multiplication(int a, int b) {

	int result = 0;
	int product;

	// dont bother calculating if b is 1, since the result is a.
	if(b == 1) {
		return a;
	}

	// dont bother calculating if a is 1, since the result is b.
	if(a == 1) {
		return b;
	}
	
	// if both numbers are negative, break and return 0
	if(b == 0 && a == 0) {
                return result;
        }

	// if b is negative, negate it using two's complement negation:
	// negation is done by inverting and adding +1 to the end.
	if (b < 0) {
        	b = ~b;
        	b = b + 1;
        	a = ~a;
		a = a + 1;
	}

	// if a is odd, add its value to the product.
	if ((a & 1) == 1) {
	        product = a;
	}

	// if b is even, dont need to initialize product with a. 
	if ((b & 1) == 0) {
	        product = 0;
	}

	// until b reaches 0, double a and halve b in each loop.
	// a value is added if b is odd.
	while (b != 1) {
        	a = a << 1;
        	b = b >> 1;
        	if ((b & 1) == 1) {
        	         product = product + a; 
        	}
	}

	result = product;
	return result;
}


