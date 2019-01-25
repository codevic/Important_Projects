//
// Created by kavya on 5/3/2018.
//
#include "Menu.h"

void Menu::input_file_menu(){
    int ch;
    cout << "\n Do you want to:\n\t 1. Run all sorts N times with n different input size \n\t 2. Run a code N times\n\t 3. Generate input file";
    cout << "\n Enter your choice : ";
    cin >> ch;
    if(ch == 1){
        int N, n, k = 0 ;
        cout << "\n Enter how many times you want to run the code : ";
        cin >> N;
        int num[] = {10000,100000,1000000,10000000,100000000};
        ofstream file2;
        int j = -1;
        string timestamp = GenerateInput::get_date();
        string path = GenerateInput::GetCurrentWorkingDir();
        path +="\\runtime\\";
        file2.open(path+"Sorts_N_runs_for_n_inputSizes_runtimes.txt", ios::app);
        string pgm[] ={"heap_sort","quick_sort-classical","quick_sort-randomized","quick_sort-median","quick_sort-hybrid","c++ inbuilt sort"};
        cout <<"\n";
        for(int i = 0 ; i < N; i ++) {
            if(j < 4)
                j++;
            else
                j = 0;
            n = num[j];
            cout<<"\n for n : "<<n;
            float array[n];
            cout<<"\n Generating Input...";
            string timestamp = GenerateInput::generate_input(n, k, 2, 1);

            cout<<"\ntimestamp : "<< timestamp;
            // read from input file:
            cout<<"\n Reading from Input file...";
            ReadInput::read_from_input(2, 1, array, n, k, timestamp);

            file2 << n << "," << pgm[0] << "," << HeapSort::heapSort(array, n) << "\n";
            file2 << n << "," << pgm[1] << "," << FirstQuickSort::quickSortfirst(array, 0, n - 1) << "\n";
            file2 << n << "," << pgm[2] << "," << RandomizedQuickSort::quickSortrandom(array, 0, n - 1) << "\n";
            file2 << n << "," << pgm[3] << "," << MedianofthreeQuickSort::quickSortmedian(array, 0, n - 1) << "\n";
            file2 << n << "," << pgm[4] << "," << optimizedquicksort::OptimizedQuickSort(array, 0, n - 1, k) << "\n";
            file2 << n << "," << pgm[5] << "," << cppSort::cpp_Sort(array, n) << "\n";
        }
        file2.close();
    }
    else if (ch == 2){
        int N, n, k = 0,ch1, choice_of_file;
        cout << "\n Enter how many times you want to run the code : ";
        cin >> N;
        cout<< "\n Choose the program you want to run:\n\t 1. Find kth smallest in an array \n\t 2. Find the top k elements in an array "
            << "\n\t 3. Heap Sort\n\t 4. Quick Sort - Classical\n\t 5. Quick Sort - Randomized\n\t 6. Quick Sort - Heuristic of 3 Medians"
            << "\n\t 7. Quick Sort with insertion sort\n\t 8. C++ built-in sort function\n\t 9. Run all 6 sorts for a file"
            <<"\n\t 10. Run a code N times";
        cout << "\n Enter your choice : ";
        cin >> ch1;
        cout << "\n Enter the value of n : ";
        cin >> n;
        if(ch1 == 1 or ch1 == 2) {
                choice_of_file = 1;
                cout << "\n Enter the value of k : ";
                cin >> k;
        } else {
            choice_of_file = 2;
        }
        float array[n];
        Menu::run_N_times( N, ch, array, n, k, 1, choice_of_file);
    }

    else if (ch == 3)
    {
        generate_input_menu();
    }
    else {
        cout << "\n Invalid input. Input must be 1 or 2. Try again!";
        input_file_menu();
    }
}

void Menu::generate_input_menu(){
    // file for kth smallest or sorting
    int ch, n;
    cout << "\n Do you want uniform or normal data? \n\t 1. Uniform data \n\t 2. Normal data";
    cout << "\n Enter your choice : ";
    cin >> ch;
    cout << "\n Enter the number of elements:";
    cin >> n;
    if(ch == 1) {
        program_menu(1, n);
    }
    else if(ch == 2) {
        program_menu(2, n);
    }
    else {
        cout << "\n Invalid input. Input must be 1 or 2. Try again!";
        generate_input_menu();
    }
}

void Menu::program_menu(int choice_of_distribution, int n) {
    int ch, choice_of_file, k = 0;
    float array[n];
    string filename, timestamp;

    cout<< "\n Choose the program you want to run:\n\t 1. Find kth smallest in an array \n\t 2. Find the top k elements in an array "
        << "\n\t 3. Heap Sort\n\t 4. Quick Sort - Classical\n\t 5. Quick Sort - Randomized\n\t 6. Quick Sort - Heuristic of 3 Medians"
        << "\n\t 7. Quick Sort with insertion sort\n\t 8. C++ built-in sort function\n\t 9. Run all 6 sorts for a file"
           <<"\n\t 10. Run a code N times";
    cout << "\n Enter your choice : ";
    cin >> ch;

    if (ch == 1 or ch == 2) {
        choice_of_file = 1;
        cout << "\n Enter the value of k : ";
        cin >> k;
    } else {
        choice_of_file = 2;
    }
    cout<<"\n Generating Input...";
    timestamp = GenerateInput::generate_input(n, k, choice_of_file, choice_of_distribution);

    cout<<"\ntimestamp : "<< timestamp;
    // read from input file:
    cout<<"\n Reading from Input file...";
    ReadInput::read_from_input(choice_of_file, choice_of_distribution, array, n, k, timestamp);

    switch (ch) {
        case 1:
            cout<<"\nYou chose kth smallest elements..";
            kthSmallest::KthSmallest(array, 0, n-1, k);
            cout<<"\n Done...!!";
            break;
        case 2:
            cout<<"\nYou chose top k smallest elements..";
            TopKSmallest::top_k_smallest_elements(array, n, k);
            cout<<"\n Done...!!";
            break;
        case 3:
            // call heap sort
            cout<<"\nYou chose heap sort..";
            HeapSort::heapSort(array, n);
            cout<<"\n Done Sorting...";
            break;
        case 4:
            // call quick sort - classical
            cout<<"\nYou chose quick sort - classical..";
            FirstQuickSort::quickSortfirst(array,0,n-1);
            cout<<"\n Done Sorting...";
            break;
        case 5:
            // call quick sort - randomized
            cout<<"\nYou chose quick sort - randomized..";
            RandomizedQuickSort::quickSortrandom(array,0,n-1);
            cout<<"\n Done Sorting...";
            break;
        case 6:
            // call quick sort - heuristics of 3 medians
            cout<<"\nYou chose quick sort - heuristics of 3 medians..";
            MedianofthreeQuickSort::quickSortmedian(array, 0, n - 1);
            cout<<"\n Done Sorting...";
            break;
        case 7:
            // call quick sort - insertion sort
            cout<<"\nYou chose hybrid quick sort (insertion sort)...";
            optimizedquicksort::OptimizedQuickSort(array, 0, n-1, k);
            cout<<"\n Done Sorting...";
            break;
        case 8:
            // call c++ built-in sort function
            cout<<"\nYou chose cpp inbuilt sort...";
            cppSort::cpp_Sort(array, n);
            cout<<"\n Done Sorting...";
            break;
        case 9:
            // call input file on all sorts
            ofstream file2;
            string timestamp = GenerateInput::get_date();
            string path = GenerateInput::GetCurrentWorkingDir();
            path +="\\runtime\\";
            file2.open(path+"all_sort_runtime_"+to_string(n)+".txt");
            cout <<"\n";
            file2 << 1 <<","<< HeapSort::heapSort(array, n) << "\n";
            file2 << 2 <<","<< FirstQuickSort::quickSortfirst(array,0,n-1) << "\n";
            file2 << 3 <<","<< RandomizedQuickSort::quickSortrandom(array,0,n-1) << "\n";
            file2 << 4 <<","<< MedianofthreeQuickSort::quickSortmedian(array, 0, n - 1) << "\n";
            file2 << 5 <<","<< optimizedquicksort::OptimizedQuickSort(array, 0, n-1, k) << "\n";
            file2 << 6 <<","<< cppSort::cpp_Sort(array, n) << "\n";
            cout << "\nOutput was written to file!!\n";
            file2.close();
            break;
    }
}

void Menu::run_N_times(int N, int ch, float array[], int n, int k, int choice_of_distribution, int choice_of_file){
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\runtime\\";
    file2.open(path+"N_runs_runtimes.txt");
    string pgm[] ={"kth_smallest","top_k_smallest","heap_sort","quick_sort-classical","quick_sort-randomized","quick_sort-median","quick_sort-hybrid","c++ inbuilt sort"};
    file2 << pgm[ch-1] <<"\n";
    cout <<"\n";
    for(int i = 0 ; i < N; i ++) {
        cout<<"\n Generating Input...";
        string timestamp = GenerateInput::generate_input(n, k, choice_of_file, choice_of_distribution);

        cout<<"\ntimestamp : "<< timestamp;
        // read from input file:
        cout<<"\n Reading from Input file...";
        ReadInput::read_from_input(choice_of_file, choice_of_distribution, array, n, k, timestamp);
        switch (ch) {
            case 1:
                cout << "\nYou chose kth smallest elements..";

                file2 << kthSmallest::KthSmallest(array, 0, n - 1, k) << "\n";
                cout << "\n Done...!!";
                break;
            case 2:
                cout << "\nYou chose top k smallest elements..";
                file2 << TopKSmallest::top_k_smallest_elements(array, n, k) << "\n";
                cout << "\n Done...!!";
                break;
            case 3:
                // call heap sort
                cout << "\nYou chose heap sort..";
                file2 << HeapSort::heapSort(array, n) << "\n";
                cout << "\n Done Sorting...";
                break;
            case 4:
                // call quick sort - classical
                cout << "\nYou chose quick sort - classical..";
                file2 << FirstQuickSort::quickSortfirst(array, 0, n - 1) << "\n";
                cout << "\n Done Sorting...";
                break;
            case 5:
                // call quick sort - randomized
                cout << "\nYou chose quick sort - randomized..";
                file2 << RandomizedQuickSort::quickSortrandom(array, 0, n - 1) << "\n";
                cout << "\n Done Sorting...";
                break;
            case 6:
                // call quick sort - heuristics of 3 medians
                cout << "\nYou chose quick sort - heuristics of 3 medians..";
                file2 << MedianofthreeQuickSort::quickSortmedian(array, 0, n - 1) << "\n";
                cout << "\n Done Sorting...";
                break;
            case 7:
                // call quick sort - insertion sort
                cout << "\nYou chose hybrid quick sort (insertion sort)...";
                file2 << optimizedquicksort::OptimizedQuickSort(array, 0, n - 1, k) << "\n";
                cout << "\n Done Sorting...";
                break;
            case 8:
                // call c++ built-in sort function
                cout << "\nYou chose cpp inbuilt sort...";
                file2 << cppSort::cpp_Sort(array, n) << "\n";
                cout << "\n Done Sorting...";
                break;
        }
    }
    file2.close();
}
