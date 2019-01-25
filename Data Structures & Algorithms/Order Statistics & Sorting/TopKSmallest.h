//
// Created by kavya on 5/3/2018.
//

#ifndef MENU_TOPKSMALLEST_H
#define MENU_TOPKSMALLEST_H
#include <iostream>
#include <fstream>
#include <chrono>
#include <time.h>
#include "GenerateInput.h"

using namespace std;
using get_time = chrono::steady_clock ;

class TopKSmallest {
public:
    static void swap(float array[],int i ,int j);
    static void max_heapify(float array[], int i, int n);
    static void print_and_write(float array[], int n);
    static double top_k_smallest_elements(float array[], int n, int k);
    static void write_runtime_to_file(int n, float runtime);
};


#endif //MENU_TOPKSMALLEST_H
