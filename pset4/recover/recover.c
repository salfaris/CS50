#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: recover [filename]\n");
        return 1;
    }

    // Open file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("%s cannot be opened for reading.\n", argv[1]);
        return 2;
    }

    // Creates a buffer to store 512 bytes
    BYTE buf[512];

    char filename[32];  // Filename for new JPEG file
    FILE *newImage;  // Pointer to new JPEG file to write onto
    int countJPEG = 0;  // Counts the num of JPEG
    bool notFirstJPEG = false;  // Checks whether a JPEG file was opened

    // Loop through file and read 512 bytes chunks into a buffer
    while (fread(buf, 1, sizeof(buf), file) == sizeof(buf))
    {
        // Checks if match JPEG header: 0xff 0xd8 0xff 0xe*
        if (buf[0] == 0xff && buf[1] == 0xd8 && buf[2] == 0xff && (buf[3] & 0xf0) == 0xe0)
        {
            // If a JPEG file was opened
            if (notFirstJPEG)
            {
                // Close the was opened file
                fclose(newImage);
            }

            // Create a new JPEG file and open it to write data into
            sprintf(filename, "%03i.jpg", countJPEG);
            newImage = fopen(filename, "w");

            // Declare that a file is opened
            notFirstJPEG = true;

            // Add to JPEG counter
            countJPEG++;

            // Write data to the new JPEG file
            fwrite(&buf, sizeof(buf), 1, newImage);
        }
        // If does not match JPEG header
        else
        {
            // If some JPEG file was opened
            if (notFirstJPEG)
            {
                // Keep writing data to opened JPEG file
                fwrite(&buf, sizeof(buf), 1, newImage);
            }
        }
    }
    // Close file and any still opened JPEG files
    fclose(file);
    fclose(newImage);
    return 0;
}