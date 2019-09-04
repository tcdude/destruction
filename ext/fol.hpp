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

#ifndef FOL_HPP
#define FOL_HPP

#include <vector>


class Species {
public:
	Species();
	void set_strength(const int s);
	void set_fertility(const int f);
	int get_strength();
	int get_fertility();
	int get_nutrition();
	int get_population();
	bool is_initialized();
private:
	void _update_stats();
	int _strength, _fertility, _nutrition, _population, _init;
};


class World {
public:
	World();
	void init(const int width, const int height, const int max_food, Species& s_a, Species& s_b);
	void simulate_step();
	std::vector<int> cells();
	std::vector<int> food();
private:
	int evaluate(const int x, const int y);

	int _width, _height, _max_food, _turn;
	std::vector<int> _cells, _food;
	Species _s_a, _s_b;
	bool _initialized;
};

#endif
