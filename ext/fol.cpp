
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
#include <iostream>

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
	if (f > 0 && f < 4) {
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
	_nutrition = _strength * _strength * (5 - _fertility) * (4 - _fertility);
}

/**
 *
 */
World::
World() {
	_initialized = false;
}

/**
 * initialize the world.
 */
void World::
init(const int width, const int height, const int max_food, Species& s_a, Species& s_b) {
	_width = width;
	_height = height;
	_max_food = max_food;
	_s_a = s_a;
	_s_b = s_b;
	_cells.reserve(_width * _height);
	_food.reserve(_width * _height);
	_turn = 0;
	_count[0] = _width * _height;
	_count[1] = _count[2] = 0;
	for (int i = 0; i < _width * _height; ++i) {
		_cells.push_back(0);
		_food.push_back(_max_food);
	}
	_initialized = true;
}

/**
 * Toggle a cell for initial placement
 */
bool World::
toggle(const int species, const int x, const int y) {
	if (! _initialized) {
		return false;
	}
	const int pos = x + y * _width;
	if (_cells[pos] == 0 && species == 1 && _count[1] < _s_a.get_population()) {
		_cells[pos] = 1;
		++_count[1];
		--_count[0];
		return true;
	}
	else if (_cells[pos] == 0 && species == 2 && _count[2] < _s_b.get_population()) {
		_cells[pos] = 2;
		++_count[2];
		--_count[0];
		return true;
	}
	else if (_cells[pos] == species) {
		_cells[pos] = 0;
		--_count[species];
		++_count[0];
		return true;
	}
	return false;
}


/**
 */
void World::
simulate_step() {
	std::vector<int> tmp_cells;
	tmp_cells.reserve(_cells.size());
	tmp_cells.insert(tmp_cells.end(), _cells.begin(), _cells.end());
	for (int y=0; y < _height; ++y) {
		for (int x=0; x < _width; ++x) {
			tmp_cells[y * _width + x] = evaluate(x, y);
		}
	}
	_cells.clear();
	_cells.insert(_cells.begin(), tmp_cells.begin(), tmp_cells.end());
	_count[0] = _count[1] = _count[2] = 0;
	for (int y=0; y < _height; ++y) {
		for (int x=0; x < _width; ++x) {
			int eval_cell = x + y * _width;
			if (_cells[eval_cell] == 0 && _food[eval_cell]) {
				int f = _food[eval_cell];
				_food[eval_cell] = (f < _max_food) ? f + 1 : f;
			}
			else if (_cells[eval_cell] == 1) {
				int r = _food[eval_cell] - _s_a.get_nutrition();
				// ++r;
				if (r < 0) {
					_cells[eval_cell] = 0;
				}
				_food[eval_cell] = (r < 0) ? 0 : r;
			}
			else {
				int r = _food[eval_cell] - _s_b.get_nutrition();
				// ++r;
				if (r < 0) {
					_cells[eval_cell] = 0;
				}
				_food[eval_cell] = (r < 0) ? 0 : r;
			}
			++_count[_cells[eval_cell]];
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
	int count_a = 0, count_b = 0, count_e = 0;
	for (int xo=-1; xo < 2; ++xo) {
		for (int yo=-1; yo < 2; ++yo) {
			int xc = x + xo;
			int yc = y + yo;
			if (xc < 0 || xc >= _width || yc < 0 || yc >= _height) {
				continue;
			}
			switch (_cells[xc + yc * _width]) {
				case 0: {
					++count_e;
					break;
				}
				case 1: {
					++count_a;
					break;
				}
				case 2: {
					++count_b;
					break;
				}
			}
		}
	}

	int eval_cell = _cells[pos];
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
			if (count_a + count_b > 1 + fertility_a) {
				return 0;
			}
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
			if (count_a + count_b > 1 + fertility_b) {
				return 0;
			}
			if (count_a * strength_a <= count_b * strength_b) {
				return 2;
			}
			else {
				if (count_a - fertility_a > -1) {
					return 1;
				}
				else {
					return 0;
				}
			}
			break;
		}
	}	
	return 0;
}

/**
 *
 */
std::vector<int> World::
cells() {
	return _cells;
}

/**
 *
 */
std::vector<int> World::
food() {
	return _food;
}

/**
 *
 */
int World::
count_a() {
	return _count[1];
}

/**
 *
 */
int World::
count_b() {
	return _count[2];
}

