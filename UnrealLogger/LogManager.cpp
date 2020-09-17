// Fill out your copyright notice in the Description page of Project Settings.

#include "LogManager.h"
#include <fstream>
#include <vector>
using namespace std;

static vector<LogData> logData;
static float time = 0.f;
static int isLogging = 0;

bool ULogManager::Save(FString path)
{
    string filepath = TCHAR_TO_UTF8(*(FPaths::ProjectIntermediateDir() + path + ".txt"));
    //string msg = "test";
    ofstream out(filepath);
    for (int i = 0; i < logData.size(); i++) {
        char buff[100];
        LogData& l = logData[i];
        sprintf_s(buff, "%d,%f,%f,%f,%f,%f,%f,%f,%d",
            l.seq, l.px, l.py, l.pz, l.ox, l.oy, l.oz, l.eTime, l.info);
        out << buff << endl;
    }
    out.close();
    return true;
    //C:\Users\hglim\Documents\Unreal Projects\testlog\Intermediate
    // return FFileHelper::SaveStringToFile(FString(msg.c_str()), *(FPaths::ProjectIntermediateDir() + path));
}

int ULogManager::AppendLog(int seq, FVector look_dir, FVector obj_dir, int info)
{
    if (isLogging == 0) return -1;
    logData.push_back({ seq, look_dir.X, look_dir.Y, look_dir.Z, obj_dir.X, obj_dir.Y, obj_dir.Z, time, info });
    return logData.size();
}

int ULogManager::ResetLog()
{
    logData.clear();
    time = 0.f;
    return logData.size();
}

void ULogManager::Update(float eTime)
{
    time += eTime;
}

void ULogManager::StartLogging()
{
    isLogging = 1;
}

void ULogManager::StopLogging()
{
    isLogging = 0;
}