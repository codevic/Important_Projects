//
// Created by kavya on 5/3/2018.
//

#ifndef MENU_MENU_H
#define MENU_MENU_H
#include <iostream>
#include "HeapSort.h"
#include "GenerateInput.h"
#include "TopKSmallest.h"
#include "ReadInput.h"
#include "kthsmallest.h"
#include "optimizedquicksort.h"
#include "FirstQuickSort.h"
#include "MedianofthreeQuickSort.h"
#include "RandomizedQuickSort.h"
#include "cppSort.h"

using namespace std;

class Menu{
public:
    static void input_file_menu();
    static void generate_input_menu();
    static void program_menu(int choice_of_distribution, int n);
    static void run_N_times(int N, int ch, float array[], int n, int k, int choice_of_distribution, int choice_of_file);
};


#endif //MENU_MENU_H
