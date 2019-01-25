//
// Created by Sanjana on 21-04-2018.
//

#include "RandomizedQuickSort.h"
#include <fstream>
#include <iostream>
#include <cmath>
using namespace std;


void RandomizedQuickSort::print_Array_random(float arr[], int size)
{
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"quicksort_randomized_"+timestamp+".txt");
    for (int i = 0; i < size; i++) {
        file2 << arr[i] << "\n";
        cout << arr[i]<<"\t";
    }
    cout << "\nOutput was written to file!!\n";
    file2.close();
}

// A utility function to swap two elements
void RandomizedQuickSort::swap(float *a, float *b)
{
    float t = *a;
    *a = *b;
    *b = t;
}

int RandomizedQuickSort::partition_r(float *arr, int low, int high) {
    srand(time(NULL));
    int random = low + rand() % (high - low);
    // Swap A[random] with A[high]
    swap(&arr[random], &arr[high]);
    return RandomizedQuickSort::partition(arr, low, high);
}

int RandomizedQuickSort::partition(float *arr, int low, int high) {
    float pivot = arr[high]; // pivot
    int i = (low - 1); // Index of smaller element
    for (int j = low; j <= high - 1; j++) {
        // If current element is smaller than or
        // equal to pivot
        if (arr[j] <= pivot) {
            i++; // increment index of smaller element
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void RandomizedQuickSort::quickSort_random(float *arr, int low, int high)
{
    if (low < high) {
        //pi is partitioning index, arr[p] is now at right place
        int pi = RandomizedQuickSort::partition_r(arr, low, high);
        // Separately sort elements before partition and after partition
        quickSort_random(arr, low, pi - 1);
        quickSort_random(arr, pi + 1, high);
    }
}

double RandomizedQuickSort::quickSortrandom(float arr[], int low, int high){
    int n = high + 1;
    auto start = get_time::now();
    RandomizedQuickSort::quickSort_random(arr, low, high);
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    printf("\nSorted array: \n");
    print_Array_random(arr,n);
    cout<<"Elapsed time is :  "<< time/1000000 <<" ms "<<endl;
    float runtime= time/1000000;
    GenerateInput::write_runtime_to_file(n, runtime, "quicksort_randomized");
    return runtime;
}
