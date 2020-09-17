// Fill out your copyright notice in the Description page of Project Settings.
#pragma once
#include <string>

using namespace std;
struct LogData {
	int seq;
	float px, py, pz;
	float ox, oy, oz;
	float eTime;
	int info;
};

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "LogManager.generated.h"

/**
 * 
 */
UCLASS()
class TESTLOG_API ULogManager : public UBlueprintFunctionLibrary
{
	GENERATED_BODY() public:

		UFUNCTION(BlueprintCallable, Category = "LHG", meta = (Keywords = "Save"))
			static bool Save(FString path);
	
		UFUNCTION(BlueprintCallable, Category = "LHG", meta = (Keywords = "AppendLog"))
			static int AppendLog(int seq, FVector look_dir, FVector obj_dir, int info);

		UFUNCTION(BlueprintCallable, Category = "LHG", meta = (Keywords = "ResetLog"))
			static int ResetLog();

		UFUNCTION(BlueprintCallable, Category = "LHG", meta = (Keywords = "Update"))
			static void Update(float eTime);

		UFUNCTION(BlueprintCallable, Category = "LHG", meta = (Keywords = "StartLogging"))
			static void StartLogging();

		UFUNCTION(BlueprintCallable, Category = "LHG", meta = (Keywords = "StopLogging"))
			static void StopLogging();
		
};
