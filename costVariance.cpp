// costVariance.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>

float bcwp()
{
	std::cout << "Enter the cumalative BCWP: ";
	float bcwp;
	std::cin >> bcwp;
	return bcwp;
}


float acwp()
{
	std::cout << "Enter the cumalative ACWP: ";
	float acwp;
	std::cin >> acwp;
	return acwp;
}

void writeVariance(float result)
{
	std::cout << "The current project CPI is:" << result << std::endl;
}

float main()
{
	float cpi = bcwp() / acwp();
	writeVariance(cpi);
    return 0;
}