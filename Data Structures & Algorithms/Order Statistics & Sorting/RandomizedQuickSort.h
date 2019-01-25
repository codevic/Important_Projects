//
// Created by Sanjana on 21-04-2018.
//

#ifndef UNTITLED_RANDOMIZEDQUICKSORT_H
#define UNTITLED_RANDOMIZEDQUICKSORT_H
#include <cstdlib>
#include <iostream>
#include <time.h>
#include <stdio.h>
#include <chrono>
#include "GenerateInput.h"
using namespace std;
using get_time = chrono::steady_clock ;

class RandomizedQuickSort {
public:
    static int partition_r(float arr[], int low, int high);
    static int partition(float arr[], int low, int high);
    static void swap(float* a, float* b);
    static void quickSort_random(float arr[], int low, int high);
    static void print_Array_random(float arr[], int size);
    static double quickSortrandom(float arr[], int low, int high);


};


#endif //UNTITLED_RANDOMIZEDQUICKSORT_H
