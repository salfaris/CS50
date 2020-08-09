// includes
#include <stdio.h>
#include <cs50.h>

// function declarations
bool valid_triangle(float side1, float side2, float side3);

// main function
int main(void)
{
    // Prompts user for real numbers as side length
    float a = get_float("First side: ");
    float b = get_float("Second side: ");
    float c = get_float("Third side: ");

    // Apply valid_triangle
    bool result = valid_triangle(a, b, c);
    (result == true) ? printf("This is a valid triangle.\n") : printf("This is NOT a valid triangle.\n");
}

// function definitions
bool valid_triangle(float a, float b, float c)
{
    // Check if either of a, b or c is non-positive
    if (a <= 0 || b <= 0 || c <= 0)
    {
        return false;
    }
    // Check if the sum of any two is greater than the third
    else if ((a + b <= c) || (a + c <= b) || (b + c <= a))
    {
        return false;
    }
    else
    {
        return true;
    }
}