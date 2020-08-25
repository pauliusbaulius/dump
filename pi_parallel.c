#include <stdio.h>
#include <omp.h>
#include <time.h>
#include <stdlib.h>

int total_points;
int points_within_circle;

float approximate_pi(int points) {

	#pragma omp parallel for reduction(+:total_points) reduction(+:points_within_circle)
	for(int i = 0; i < points; i++) {
		float x = -1 + 2 *((float)rand())/RAND_MAX;
		float y = -1 + 2 *((float)rand())/RAND_MAX;
		if ((x * x + y * y) <= 1)
			points_within_circle += 1;
		total_points += 1;
		
	}
	
	printf("total_count = %d, within_circle = %d\n", total_points, points_within_circle);
	float pi = 4.0 * (points_within_circle / (float)total_points);
	return pi;
}

int main() {
	int a_lot = 10000000; // how many points for approximation
	float pi = approximate_pi(a_lot);
	printf("Approximated value of pi is %f\n", pi);
}
