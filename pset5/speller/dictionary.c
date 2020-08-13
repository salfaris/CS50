// Implements a dictionary's functionality

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 180181;

// Hash table
node *table[N];

// Number of words in dictionary
unsigned int num_words = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash the word
    unsigned int hash_idx = hash(word);

    // Access linked list at table[hash_idx] and iterate from there
    for (node *tmp = table[hash_idx]; tmp != NULL; tmp = tmp->next)
    {
        // Compare case insensitively the two words
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Any two prime numbers or pseudoprimes
    int p_key = 1783;
    int q_key = 1249;
    int val = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        val += toupper(word[i]) * p_key * q_key;
    }

    int hash_idx = val % N;
    return hash_idx;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Create buffer
    char new_word[LENGTH + 1];

    // Read strings from file
    while (fscanf(file, "%s", new_word) != EOF)
    {
        // Create a new node
        node *n = malloc(sizeof(node));
        // Check if we have enough memory
        if (n == NULL)
        {
            free(n);
            return false;
        }
        // Set the node's attributes (word, next)
        strcpy(n->word, new_word);
        n->next = NULL;

        // Hash the word
        unsigned int hash_idx = hash(new_word);

        // Insert node into hash table
        if (table[hash_idx] == NULL)
        {
            // Points the table head to what n was pointing at
            table[hash_idx] = n;
        }
        else
        {
            // Points n's next to what table head was pointing to
            n->next = table[hash_idx];
            // Points table head to n
            table[hash_idx] = n;
        }
        // Add count to total number of words
        num_words++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return num_words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Iterate over each index of array
    for (int i = 0; i < N; i++)
    {
        // Trace the linked-list and freeing the head one-by-one
        while (table[i] != NULL)
        {
            // Point to what table[i] was pointing at
            node *tmp = table[i]->next;
            // Free table[i] itself
            free(table[i]);
            // Make table[i] point to what tmp is now pointing at
            table[i] = tmp;
        }
    }
    return true;
}
