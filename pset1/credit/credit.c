#include <stdio.h>
#include <cs50.h>

long counter(long n);

int main(void)
{
    long num;
    do
    {
        num = get_long("Number: ");
    }
    while (num < 0);
    long count = counter(num);

    if (count < 13)
    {

    }

}

long counter(long n)
{
    long count = 0;
    while (n != 0)
    {
        n /= 10;
        count++;
    }
    return count;
}