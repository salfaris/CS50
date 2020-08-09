#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Access row
    for (int i = 0; i < height; i++)
    {
        // Access column
        for (int j = 0; j < width; j++)
        {
            // Compute the average color of pixel
            int avg_col = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            // Reassign values of RGB to the average color
            image[i][j].rgbtBlue = avg_col;
            image[i][j].rgbtGreen = avg_col;
            image[i][j].rgbtRed = avg_col;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Access row
    for (int i = 0; i < height; i++)
    {
        // Access column
        for (int j = 0; j < width; j++)
        {
            // Get original RGB of pixel
            int originalBlue = image[i][j].rgbtBlue;
            int originalGreen = image[i][j].rgbtGreen;
            int originalRed = image[i][j].rgbtRed;

            // Apply the sepia transformation
            int sepiaBlue = (int) round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
            int sepiaGreen = (int) round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaRed = (int) round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);

            // Checks if any of sepiaBlue, sepiaGreen or sepiaRed is beyond the 0-255 range
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            // Assign the sepia transformation
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Access row
    for (int i = 0; i < height; i++)
    {
        // Initialize starting and ending points
        int start = 0, end = width - 1;
        // Initialize temporary boxes to store RGB values
        int tempBlue, tempGreen, tempRed;

        // Reflection begins
        while (start < end)
        {
            // Store starting RGB into temporary boxes
            tempBlue = image[i][start].rgbtBlue;
            tempGreen = image[i][start].rgbtGreen;
            tempRed = image[i][start].rgbtRed;

            // Take end RGB values and store into start RGB values
            image[i][start].rgbtBlue = image[i][end].rgbtBlue;
            image[i][start].rgbtGreen = image[i][end].rgbtGreen;
            image[i][start].rgbtRed = image[i][end].rgbtRed;

            // Take temporary stored RGB values and store into end RGB values
            image[i][end].rgbtBlue = tempBlue;
            image[i][end].rgbtGreen = tempGreen;
            image[i][end].rgbtRed = tempRed;

            // Change starting point to +1 and ending point to -1
            start++;
            end--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];
    // Copies original image into temporary newImage
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            newImage[y][x] = image[y][x];
        }
    }

    // Access columns
    for (int y = 0; y < height; y++)
    {
        // Access rows
        for (int x = 0; x < width; x++)
        {
            // Initialize with default center pixel
            int redSum = newImage[y][x].rgbtRed;
            int greenSum = newImage[y][x].rgbtGreen;
            int blueSum = newImage[y][x].rgbtBlue;
            int count = 1;

            // Add left pixel
            if (x > 0)
            {
                redSum += newImage[y][x - 1].rgbtRed;
                greenSum += newImage[y][x - 1].rgbtGreen;
                blueSum += newImage[y][x - 1].rgbtBlue;
                count++;
            }

            // Add right pixel
            if (x < width - 1)
            {
                redSum += newImage[y][x + 1].rgbtRed;
                greenSum += newImage[y][x + 1].rgbtGreen;
                blueSum += newImage[y][x + 1].rgbtBlue;
                count++;
            }

            // Add top pixel
            if (y > 0)
            {
                redSum += newImage[y - 1][x].rgbtRed;
                greenSum += newImage[y - 1][x].rgbtGreen;
                blueSum += newImage[y - 1][x].rgbtBlue;
                count++;
            }

            // Add bottom pixel
            if (y < height - 1)
            {
                redSum += newImage[y + 1][x].rgbtRed;
                greenSum += newImage[y + 1][x].rgbtGreen;
                blueSum += newImage[y + 1][x].rgbtBlue;
                count++;
            }

            // Add top left pixel
            if (x > 0 && y > 0)
            {
                redSum += newImage[y - 1][x - 1].rgbtRed;
                greenSum += newImage[y - 1][x - 1].rgbtGreen;
                blueSum += newImage[y - 1][x - 1].rgbtBlue;
                count++;
            }

            // Add top right pixel
            if (x < (width - 1) && y > 0)
            {
                redSum += newImage[y - 1][x + 1].rgbtRed;
                greenSum += newImage[y - 1][x + 1].rgbtGreen;
                blueSum += newImage[y - 1][x + 1].rgbtBlue;
                count++;
            }

            // Add bottom left pixel
            if (x > 0 && y < (height - 1))
            {
                redSum += newImage[y + 1][x - 1].rgbtRed;
                greenSum += newImage[y + 1][x - 1].rgbtGreen;
                blueSum += newImage[y + 1][x - 1].rgbtBlue;
                count++;
            }

            // Add bottom right pixel
            if (x < (width - 1) && y < (height - 1))
            {
                redSum += newImage[y + 1][x + 1].rgbtRed;
                greenSum += newImage[y + 1][x + 1].rgbtGreen;
                blueSum += newImage[y + 1][x + 1].rgbtBlue;
                count++;
            }

            // Get average and round
            image[y][x].rgbtRed = round(redSum / (float) count);
            image[y][x].rgbtGreen = round(greenSum / (float) count);
            image[y][x].rgbtBlue = round(blueSum / (float) count);
        }
    }
    return;
}