//
// Created by Sanjana on 21-04-2018.
//
#include "FirstQuickSort.h"
#include "GenerateInput.h"


//
// Created by Sanjana on 20-04-2018.
//

using namespace std;

int FirstQuickSort::partition1(float a[],int first,int last) {
//initializing the pivot as the first element and then putting it in rightful position
    int pivot=a[first],next=first+1,i,temp;
    for(i=first+1;i<=last;i++)
    {
        if(a[i]<pivot)
        {
            if(i!=next)
            {
                temp=a[next];
                a[next]=a[i];
                a[i]=temp;
            }    next++;
        }
    }
    a[first]=a[next-1];
    a[next-1]=pivot;
    return next-1;
}

/* Function to print an array */
void FirstQuickSort::print_Array(float arr[], int size)
{
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"quicksort_classical_"+timestamp+".txt");
    for (int i = 0; i < size; i++) {
        file2 << arr[i] << "\n";
        cout << arr[i]<<"\t";
    }
    cout << "\nOutput was written to file!!\n";
    file2.close();
}


void FirstQuickSort::quickSort_first(float *arr, int low, int high) {
    if (low < high) {

        int pi = FirstQuickSort::partition1(arr, low, high);
        quickSort_first(arr, low, pi - 1);
        quickSort_first(arr, pi + 1, high);
    }
}

double FirstQuickSort::quickSortfirst(float *arr, int low, int high) {
    int n = high + 1;
    auto start = get_time::now();
    FirstQuickSort::quickSort_first(arr,low,high);
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    //display the output in form of an array
    printf("\nSorted array: \n");
    print_Array(arr,n);
    cout<<"Elapsed time is :  "<< time/1000000 <<" ms "<<endl;
    float runtime= time/1000000;
    GenerateInput::write_runtime_to_file(n, runtime, "quicksort_classical");
    return runtime;
}





