//
// Created by kavya on 5/3/2018.
//

#ifndef MENU_READINPUT_H
#define MENU_READINPUT_H

#include <string>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <iterator>
#include "GenerateInput.h"
using namespace std;

class ReadInput {
    public:
        static void read_from_input(int choice_of_file, int choice_of_distribution, float array[], int n, int k, string timestamp);
};


#endif //MENU_READINPUT_H
