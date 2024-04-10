#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

int main() {
    CURL *curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (!curl) {
        fprintf(stderr, "Error initializing curl.\n");
        return 1;
    }

    char userInput[256];
    char postData[1024];
    char continueinput;
    char modelChoice[256];

    printf("Select translation model:\n");
    printf("EN_RU\n");
    printf("RU_EN\n");

    scanf("%s", modelChoice);

    if (strcmp(modelChoice, "EN_RU") != 0 && strcmp(modelChoice, "RU_EN") != 0) {
        fprintf(stderr, "Invalid choice. Please enter EN_RU or RU_EN.\n");
        return 1;
    }

    // Clear stdin buffer
    while (getchar() != '\n');
do{
    printf("Enter a sentence: ");
    fgets(userInput, sizeof(userInput), stdin);

    userInput[strcspn(userInput, "\n")] = '\0';

    snprintf(postData, sizeof(postData), "{\"text\":\"%s\",\"model\":\"%s\"}", userInput, modelChoice);
    
    curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:5000/translate");

    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData);
    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    // Perform the HTTP POST request
    res = curl_easy_perform(curl);

    if (res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    }

    printf("\nDo you want to continue? (y/n): ");
        scanf(" %c", &continueinput);
        getchar();

    if (continueinput != 'y' && continueinput != 'Y') {
            break;
        }
}while(1);
    curl_easy_cleanup(curl);
    curl_global_cleanup();

    return 0;
}
