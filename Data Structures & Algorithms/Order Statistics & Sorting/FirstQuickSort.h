//
// Created by Sanjana on 21-04-2018.
//

#ifndef UNTITLED_FIRSTQUICKSORT_H
#define UNTITLED_FIRSTQUICKSORT_H
#include <cstdlib>
#include <iostream>
#include <ctime>
#include <stdio.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <chrono>
#include "GenerateInput.h"
using namespace std;
using get_time = chrono::steady_clock ;


class FirstQuickSort {
public:
    static int partition1(float arr[], int first, int last);
    static void quickSort_first(float arr[], int low, int high);
/* Function to print an array */
    static void print_Array(float arr[], int size);
    static double quickSortfirst(float *arr, int low, int high);
};


#endif //UNTITLED_FIRSTQUICKSORT_H
