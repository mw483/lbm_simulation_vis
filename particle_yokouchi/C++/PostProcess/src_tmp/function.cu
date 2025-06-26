#include <iostream>
#include <cstdlib>

#include "stParticle.h"
#include "function.h"


/* ---------- Function sort 		---------- */

int sort_compare (const void* A, const void* B) {
	const Particle_Index* a = (const Particle_Index*)A;
	const Particle_Index* b = (const Particle_Index*)B;

	int diff = a->index - b->index;
	if (diff == 0) {
		std::cout << "Error!! index is incorrect." << std::endl;
		exit(EXIT_FAILURE);
	}

	return diff;
}

bool sort_index (const Particle_Index& A, const Particle_Index& B) {
	return A.index < B. index;
}
