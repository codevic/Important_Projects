//
// Created by kavya on 5/3/2018.
//

#ifndef MENU_GENERATEINPUT_H
#define MENU_GENERATEINPUT_H
#include <string>
#include <iostream>
#include <random>
#include <chrono>
#include <string>
#include <fstream>



#include <stdio.h>  /* defines FILENAME_MAX */
#define WINDOWS  /* uncomment this line to use it for windows.*/
#ifdef WINDOWS
#include <direct.h>
#define GetCurrentDir _getcwd
#else
#include <unistd.h>
#define GetCurrentDir getcwd
#endif

using namespace std;
using get_time = chrono::steady_clock ;

class GenerateInput {

public:
    static string get_date(void);

    static string generate_input(int n, int k, int choice_of_file, int choice_of_distribution);

    static string generate_file1_uniform(int n, int k, string path, string timestamp);

    static string generate_file2_uniform(int n, string path, string timestamp);

    static string generate_file1_normal(int n, int k, string path, string timestamp);

    static string generate_file2_normal(int n, string path, string timestamp);

    static void write_runtime_to_file(int n, float runtime, string filename);

    static string GetCurrentWorkingDir() ;

};


#endif //MENU_GENERATEINPUT_H
