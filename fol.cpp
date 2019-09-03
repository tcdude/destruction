
/**
 *
 * MIT License
 * 
 * Copyright (c) 2019 tcdude
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

#include "fol.hpp"


/**
 * c-tor Species
 */
Species::
Species() {
	_strength = 1;
	_fertility = 3;
	_nutrition = 1;
	_population = 36;
	_init = 0;
}

/**
 */
void Species::
set_strength(const int s) {
	if (s > 0 && s < 4) {
		_strength = s;
		_update_stats();
		_init = _init | 1;
	}
}

/**
 */
void Species::
set_fertility(const int f) {
	if (f > 0 && s < 4) {
		_fertility = f;
		_update_stats();
		_init = _init | 2;
	}
}

/**
 *
 */
int Species::
get_strength() {
	return _strength;
}

/**
 *
 */
int Species::
get_fertility() {
	return _fertility;
}

/**
 *
 */
int Species::
get_nutrition() {
	return _nutrition;
}

/**
 *
 */
int Species::
get_population() {
	return _population;
}

/**
 *
 */
bool Species::
is_initialized() {
	return _init & 1 && _init & 2;
}

/**
 * Updates _nutrition and _population, based on the current value of _strength and _fertility.
 */
void Species::
_update_stats() {
	_population = 4 - _strength + _fertility;
	_population *= _population;
	_nutrition = _strength * _strength + (3 - _fertility);
}


/**
 * c-tor, reserve memory for world vector.
 */
World::
World(const int width, const int height, Species& s_a, Species& s_b, const int max_food) : _width(width), _height(height), _max_food(max_food), _s_a(s_a), _s_b(s_b) {
	_cells.reserve(_width * _height);
	_food.reserve(_width * _height);
	_turn = 0;
	for (int i = 0; i < _width * _height; ++i) {
		_cells[i] = 0;
		_food[i] = _max_food;
	}
}


/**
 */
void World::
simulate_step() {
	std::vector<int> tmp_cells = _cells;
	for (int y=0; y < _height; ++y) {
		for (int x=0; x < _width; ++x) {
			tmp_cells[y * _width + x] = evaluate(x, y);
		}
	}

	_cells = tmp_cells;
	for (int y=0; y < _height; ++y) {
		for (int x=0; x < _width; ++x) {
			int eval_cell = x + y * _width;
			if (_cells[eval_cell] == 0) {
				int f = _food[eval_cell];
				_food[eval_cell] = (f < _max_food) ? f + 1 : f;
			}
			else if (_cells[eval_cell] == 1) {
				int r = _food[eval_cell] - _s_a.get_nutrition();
				if (r < 0) {
					_cells[eval_cell] = 0;
				}
				_food[eval_cell] = (r < 0) ? 0 : r;
			}
		}
	}
	++_turn;
}

/**
 * Determine cell type with the current state.
 */
int World::
evaluate(const int x, const int y) {
	const int pos = x + y * _width;
	const int strength_a = _s_a.get_strength();
	const int strength_b = _s_b.get_strength();
	const int fertility_a = _s_a.get_fertility();
	const int fertility_b = _s_b.get_fertility();
	int count_a, count_b, count_e;

	for (int xo=-1; xo < 2; ++xo) {
		for (yo=-1; yo < 2; ++yo) {
			xc = x + xo;
			yc = y + yo;
			if (xc < 0 || xc >= _width || yc < 0 || yc >= _height) {
				continue;
			}
			switch (_cells[xc + yc * _width]) {
				case 0: {
					count_e++;
					break;
				}
				case 1: {
					count_a++;
					break;
				}
				case 2: {
					count_b++;
					break;
				}
				case default: break;

			}
		}
	}

	int eval_cell = _cells[x + y * _width];
	switch (eval_cell) {
		case 0:	{
			int diff_a = count_a - fertility_a;
			int diff_b = count_b - fertility_b;
			if (diff_a > diff_b && diff_a > -1) {
				return 1;
			}
			else if (diff_b > diff_a && diff_b > -1) {
				return 2;
			}
			else {
				return 0;
			}
			break;
		}
		case 1: {
			if (count_a * strength_a >= count_b * strength_b) {
				return 1;
			}
			else {
				if (count_b - fertility_b > -1) {
					return 2;
				}
				else {
					return 0;
				}
			}
			break;
		}
		case 2: {
			if (count_a * strength_a <= count_b * strength_b) {
				return 2;
			}
			else {
				return 0;
			}
			break;
		}
	}	
	return 0;
}

