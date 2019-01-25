//
// Created by kavya on 5/4/2018.
//

#include "cppSort.h"

double cppSort::cpp_Sort(float array[], int n){
    auto start = get_time::now();
    sort(array, array+n);
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    float runtime = time/1000000;
    cout<<"\nElapsed time is :  "<< runtime <<" ms "<<endl;
    GenerateInput::write_runtime_to_file(n, runtime, "cpp_sort");
    cout << "\nSorted array: \n";
    for (int i = 0; i < n; ++i)
        cout << array[i] << " ";
    cppSort::print_and_write(array, n);
    return runtime;
}

void cppSort::print_and_write(float array[], int n){
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"cpp_sort_"+timestamp+".txt");
    cout <<"\n";
    for (int i = 0; i < n; i++) {
        file2 << array[i] << "\n";
        cout <<"\t" <<array[i];
    }
    cout << "\nOutput was written to file!!\n";
    file2.close();
}