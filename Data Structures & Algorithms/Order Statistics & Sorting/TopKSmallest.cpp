//
// Created by kavya on 4/22/2018.
//

#include "TopKSmallest.h"

// this function swaps two elements in the array[]
// i and j being the position of the
// two elements that need to be swapped
// array[] : the array
// i : the position of one element
// j : the position of second element to be swapped with element at i
void TopKSmallest::swap(float array[], int i, int j)
{
    float temp = array[i];
    array[i] = array[j];
    array[j] = temp;
}

// this function performs heapify operation
// on the initial heap
// array[] : the array
// i : the position of the element
// n : size of the array[]
void TopKSmallest::max_heapify(float array[], int i, int n)
{
    // setting the left and right child of an element
    int left = 2*i+1;
    int right = 2*i+2;
    // set largest as the i
    int largest = i;
    // if left child is less than the node, then set largest to left child
    if(left < n){
        if(array[left] > array[i])
            largest = left;
    }
    // if right child is less than the node, then set largest to right child
    if(right < n){
        if(array[right] > array[largest])
            largest = right;
    }
    // if largest is not equal to i, then swap the largest with i and perform heapify
    if(largest != i){
        TopKSmallest::swap(array, i, largest);
        max_heapify(array, largest, n);
    }
}

// this function prints the array elements from 0 to nth position
// array[] : the array
// n : size of the array[]
void TopKSmallest::print_and_write(float array[], int n)
{
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"top_k_elements_"+timestamp+".txt");
    cout <<"\n";
    for (int i = 0; i < n; i++) {
        file2 << array[i] << "\n";
        cout <<"\t" <<array[i];
    }
    cout << "\nOutput was written to file!!\n";
    file2.close();
}

// this function finds the top k elements in the array[]
// array[] : size of the array[]
// n : size of the array[]
// k : number of top elements
double TopKSmallest::top_k_smallest_elements(float array[], int n, int k)
{
    int i;
    float temp_array[k];
    // add the first k elements from array[] to temp_array[]
    auto start = get_time::now();
    for( i = 0; i < k; i++) {
        temp_array[i] = array[i];
    }
    // heapify the temp_array from 0 to (k-2)/2
    for( i = (k-2)/2; i >= 0; i--){
        max_heapify(temp_array, i, k);
    }
    // for the elements from k to n
    // if root of the temp_array is greater than the ith element in array[],
    // then make array[i] as root of temp_array and perform heapify operation
    for( i = k; i < n; i++)
    {
        if(temp_array[0] > array[i]){
            temp_array[0] = array[i];
            max_heapify(temp_array, 0, k);
        }
    }
    // print the top k elements
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    float runtime = time/1000000;
    cout<<"\nElapsed time is :  "<< runtime <<" ms "<<endl;
    GenerateInput::write_runtime_to_file(n, runtime, "top_k_elements");
    print_and_write(temp_array, k);
    return runtime;
}